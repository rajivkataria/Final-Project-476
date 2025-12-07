import os, json, sys, textwrap, re, time
import requests
from apiClient import call_model_chat_completions
import strategies as strategies

def first_call(prompt: str) -> dict:
    response = call_model_chat_completions(prompt)
    response = response.get("text", "").strip() if response.get("ok") else ""
    return {"response": response}

# def run_agent(prompt: str) -> dict:
#     result = call_model_chat_completions(prompt)
#     text = result.get("text", "").strip() if result.get("ok") else ""
#     return {"response": text}
#     # problem_type = strategies.classify_problem_type(prompt)
    
#     # # We use extra checks (5 specifically) for accuracy in math problems
#     #  # Temporary return to avoid incomplete code error
#     # # result = call_model_chat_completions(prompt)

#     # # if result.get("ok"):
#     # #     text = result.get("text", "").strip()
#     # # else:
#     # #     text = ""

#     # # return {"response": text}
#     # if problem_type == "Math":
#     #     answer = strategies.extra_check_math(prompt, iterations=3)
#     #     return {"response": answer}
#     # elif problem_type == "Logical Reasoning":
#     #     answers = []
#     #     result = call_model_chat_completions(prompt)
#     #     if result.get("ok"):
#     #         answers.append(result.get("text", "").strip())
#     #     rephrased_prompt = strategies.rephrase_question(prompt)
#     #     for i in range(3):
#     #         result = call_model_chat_completions(rephrased_prompt)
#     #         if result.get("ok"):
#     #             answers.append(result.get("text", "").strip())
#     #         rephrased_prompt = strategies.rephrase_question(rephrased_prompt)
#     #     result = strategies.produce_best_answer(answers, prompt)
#     #     return {"response": result}
#     # else:
#     #     answer = call_model_chat_completions(prompt)
#     #     answer = answer.get("text", "").strip() if answer.get("ok") else ""
#     #     return {"response": answer}

def run_agent(prompt: str) -> dict:

    ptype = strategies.classify_problem_type(prompt)

    # --- Fast Math Strategy (2 calls + majority vote) ---
    if ptype == "Math":
        a1 = call_model_chat_completions(prompt)
        a2 = call_model_chat_completions(prompt)
        t1 = strategies.extract_number(a1.get("text", "")) if a1.get("ok") else ""
        t2 = strategies.extract_number(a2.get("text", "")) if a2.get("ok") else ""

        final = t1 if t1 == t2 else (t1 or t2)
        return {"response": final}

    # --- Fast Logic Strategy (1 rephrase, 1 aggregate) ---
    if ptype == "Logical Reasoning":

        a1 = call_model_chat_completions(prompt)
        r1 = a1.get("text", "").strip() if a1.get("ok") else ""

        rp = strategies.rephrase_question(prompt)
        a2 = call_model_chat_completions(rp)
        r2 = a2.get("text", "").strip() if a2.get("ok") else ""

        best = strategies.combine_answers([r1, r2], prompt)
        return {"response": best}

    # --- Common Sense (fast single call) ---
    out = call_model_chat_completions(prompt)
    return {"response": out.get("text", "").strip() if out.get("ok") else ""}

def main():
    prompt = "Explain why does the sun come up every day?"
    result = run_agent(prompt)
    print("Agent Response:", result["response"], "\nProblem Type:", result["problem_type"])
if __name__ == "__main__":
    main()