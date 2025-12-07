import os, json, sys, textwrap, re, time
import requests
from apiClient import call_model_chat_completions
import strategies as strategies

def first_call(prompt: str) -> dict:
    response = call_model_chat_completions(prompt)
    response = response.get("text", "").strip() if response.get("ok") else ""
    return {"response": response}

def run_agent(prompt: str) -> str:
    problem_type = strategies.classify_problem_type(prompt)
    
    # We use extra checks (5 specifically) for accuracy in math problems
     # Temporary return to avoid incomplete code error
    # result = call_model_chat_completions(prompt)

    # if result.get("ok"):
    #     text = result.get("text", "").strip()
    # else:
    #     text = ""

    # return {"response": text}
    if problem_type == "Math":
        return strategies.extra_check_math(prompt, iterations=3)

    elif problem_type == "Logical Reasoning":
        answers = []
        result = call_model_chat_completions(prompt)
        if result.get("ok"):
            answers.append(result.get("text", "").strip())
        rephrased_prompt = strategies.rephrase_question(prompt)
        for i in range(3):
            result = call_model_chat_completions(rephrased_prompt)
            if result.get("ok"):
                answers.append(result.get("text", "").strip())
            rephrased_prompt = strategies.rephrase_question(rephrased_prompt)
        return strategies.produce_best_answer(answers, prompt)
    else:
        result = call_model_chat_completions(prompt)
        return result.get("text", "").strip() if result.get("ok") else ""

def main():
    prompt = "A marketing company pays its employees on a commission-based salary system. If you sell goods worth $1000, you earn a 30% commission. Sales over $1000 get you an additional 10% commission. Calculate the amount of money Antonella earned if she sold goods worth $2500."
    result = run_agent(prompt)
    print(result)

if __name__ == "__main__":
    main()