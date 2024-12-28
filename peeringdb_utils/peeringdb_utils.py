import os
import sys
import json
import requests
import csv


PROMPT_FILE = "prompt_peeringdb_api.md"
PEERINGDB_URL = "https://peeringdb.com"

def get_peeringdb_prompt() -> str:
    prompt = ""
    with open(f'./peeringdb_utils/prompt_peeringdb_agent.md', 'r') as file:
        prompt = prompt + file.read() + "\n"
    with open(f'./peeringdb_utils/prompt_peeringdb_api.md', 'r') as file:
        prompt = prompt + file.read() + "\n"
    return prompt


def get_peeringdb_api(endpoint):
    url = PEERINGDB_URL.strip().strip("/") + endpoint
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return str(response.json())