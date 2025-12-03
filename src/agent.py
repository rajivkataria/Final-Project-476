import os, json, sys, textwrap, re, time
import requests
from apiClient import call_model_chat_completions
import strategies as strategies

def first_call(prompt: str) -> dict:
    response = call_model_chat_completions(prompt)
    response = response.get("text", "").strip() if response.get("ok") else ""
    return {"response": response}

def run_agent(prompt: str) -> dict:
    problem_type = strategies.classify_problem_type(prompt)
    dic = first_call(prompt)
    response = dic.get("response", "")
    return {"response": response, "problem_type": problem_type}

def main():
    prompt = "Why is 10 + 9800 = 9810?"
    result = run_agent(prompt)
    print("Agent Response:", result.get("response", ""))
    print("Problem Type:", result.get("problem_type", ""))

if __name__ == "__main__":
    main()