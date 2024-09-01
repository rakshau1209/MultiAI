import streamlit as st
import requests
import json

api_key = st.secrets['groq_api_key']
url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

# Get the JSON response
data = response.json()

# Define the file path
file_path = 'models/models.json'

# Write the JSON data to a file
with open(file_path, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f"JSON data has been written to {file_path}")
