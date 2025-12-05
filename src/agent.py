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
    
    # We use extra checks (5 specifically) for accuracy in math problems
    if problem_type == "Math":
        answer = strategies.extra_check_math(prompt, iterations=5)
        return {"response": answer, "problem_type": problem_type}
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
        result = strategies.produce_best_answer(answers, prompt)
        return {"response": result, "problem_type": problem_type}
    else:
        answer = first_call(prompt)
        return {"response": answer, "problem_type": problem_type}

def main():
    prompt = "Explain why does the sun come up every day?"
    result = run_agent(prompt)
    print("Agent Response:", result["response"], "\nProblem Type:", result["problem_type"])
if __name__ == "__main__":
    main()