FROM python:3.11-slim-bookworm

# Install pip requirements
COPY requirements.txt /
RUN python -m pip install -r /requirements.txt

#C Copy app
COPY . /app
RUN ls -al /app/

# Run application
WORKDIR "/app"
CMD ["streamlit", "run", "peeringdb_agent.py"]
 