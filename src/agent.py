import os, json, textwrap, re, time
import requests
from src.apiClient import call_model_chat_completions
import src.strategies as strategies

def first_call(prompt: str) -> dict:
    response = call_model_chat_completions(prompt)
    response = response.get("text", "").strip() if response.get("ok") else ""
    return {"response": response}

def run_agent(prompt: str) -> dict:
    dic = first_call(prompt)
    response = dic.get("response", "")
    return {"response": response}