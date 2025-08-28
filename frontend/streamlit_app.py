import os
import requests
import streamlit as st
from dotenv import load_dotenv


load_dotenv()
API_URL = os.getenv("BACKEND_URL", "http://localhost:8000/query")


st.set_page_config(page_title="Human-in-the-loop", layout="wide")
st.title("Human-in-the-loop — frontend")


if "messages" not in st.session_state:
st.session_state.messages = []


query = st.chat_input("Ask me anything:")


if query:
st.session_state.messages.append({"role": "user", "content": query})
with st.spinner("Thinking..."):
try:
resp = requests.post(API_URL, json={"query": query}, timeout=60)
resp.raise_for_status()
data = resp.json()
answer = data.get("answer")
used_tool = data.get("used_tool")
logs = data.get("logs")
content = f"**Used tool →** {used_tool}\n\n{answer}"
except Exception as e:
content = f"Error: {e}"
st.session_state.messages.append({"role": "assistant", "content": content})


for msg in st.session_state.messages:
with st.chat_message(msg["role"]):
st.markdown(msg["content"])