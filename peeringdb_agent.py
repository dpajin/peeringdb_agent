import os
import re
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import requests
import json
import logging
import logging.config

import app.settings as settings
import app.utils as utils
from datetime import datetime

import peeringdb_utils.peeringdb_utils as peeringdb_utils

load_dotenv(override=True)

logging.config.dictConfig(settings.LOGGING_CONFIG)
log = logging.getLogger(settings.APP_NAME)

st.set_page_config(layout="wide")
st.title("PeeringDB AI Agent")


#################################
# Agent
#################################

# LLM
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Get system prompt 
current_time = datetime.now()
SYSTEM_PROMPT = f"""Current time is: {current_time}

"""



class Agent:
    def __init__(self, client, model, system=""):
        self.system = system
        self.client = client
        self.model = model
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = self.client.chat.completions.create(
                        model=self.model,
                        messages=self.messages)
        return completion.choices[0].message.content

# Tools

known_tools = {
    "get_peeringdb_api": peeringdb_utils.get_peeringdb_api
}


def user_query_process(question, agent, st_mp, max_turns=5):
    action_re = re.compile('^Action: ([a-z_0-9]+): (.*)$')   # python regular expression to selection action
    thought_re = re.compile('^Thought: (.*)$')
    i = 0
    next_prompt = question
    while i < max_turns:
        i += 1
        result = agent(next_prompt)
        log.info(f"Agent turn {i}:\n{result}")
        actions = [
            action_re.match(line) 
            for line in result.split('\n') 
            if action_re.match(line)
        ]
        thought = [
            thought_re.match(line) 
            for line in result.split('\n') 
            if thought_re.match(line)
        ]
        if thought:
            st_mp.markdown(thought[0].groups()[0])
        if actions:
            next_prompt = ""
            for n, a in enumerate(actions):
                # There is an action to run
                action, action_input = a.groups()
                if action not in known_tools:
                    raise Exception("Unknown action: {}: {}".format(action, action_input))
                log.info(" -- running {} {}".format(action, action_input))
                observation = known_tools[action](action_input)
                log.info(f"Observation {n}:\n{observation}")
                next_prompt += f"Observation {n}: {observation}"
        else:
            return result

#################################
# STREAMLIT APP
#################################

# Init OpenAI client and model
if "openai_client" not in st.session_state:
    st.session_state.openai_client = OpenAI(api_key=OPENAI_API_KEY)
    st.session_state.system_prompt = SYSTEM_PROMPT + peeringdb_utils.get_peeringdb_prompt()
    st.session_state.agent = Agent(client=st.session_state.openai_client, model=OPENAI_MODEL, system=st.session_state.system_prompt)
    st.session_state.messages = []
    st.session_state.user_messages = []


# Display chat messages
for message in st.session_state.messages:
    avatar = settings.USER_AVATAR if message["role"] == "user" else settings.BOT_AVATAR
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])




# Main chat 
user_question = st.chat_input("Ask about PeeringDB data")
if user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user", avatar=settings.USER_AVATAR):
        st.markdown(user_question)
        log.info(f"Question: {user_question}")

    with st.chat_message("assistant", avatar=settings.BOT_AVATAR):
                
        message_placeholder = st.empty()
        message_placeholder.markdown("Working on it, please wait...")
        
        # Invoke the agent with the user input and current chat history
        try:
            user_response = user_query_process(user_question, st.session_state.agent, st_mp=message_placeholder, max_turns=5)
            log.info(f"Final response:\n{user_response}")

            # Add the response to the conversation history
            st.session_state.messages.append({"role": "assistant", "content": user_response})

            # Send message back to ST
            message_placeholder.markdown(user_response)
        except Exception as e:
            log.error(f"An error occured in processing agent: {str(e)}")
            st.error(f"An error occurred: {str(e)}")
        




