import re
from apiClient import call_model_chat_completions

# Method to classify the problem into Math or Non-Math
# Classifying a problem will help in selecting strategies like how many calls to make and whether to use other stategies like self-reflection or self-consistency

def get_math_output(question: str):
    result = call_model_chat_completions(question)
    if result.get("ok"):
        text = result.get("text", "")
        match = re.search(r"-?\d+(\.\d+)?", text)
        if match:
            return match.group(0)
    return ""

def extra_check_math(problem: str, iterations:int = 5) -> str:
    results = []
    for i in range(iterations):
        response = get_math_output(problem)
        results.append(response)
    if results:
        return max(set(results), key=results.count)
    return ""

def produce_best_answer(answers: list, prompt: str) -> str:
    curr_prompt = "From the following answers to the given prompt, provide  the most a ccurate and comprehesive answer, taking in as my details from all answers. The answers are also below:\n\n"
    curr_prompt += "Prompt: " + prompt + "\n\n"
    curr_prompt += "\n".join(f"Answer {i+1}: {ans}" for i, ans in enumerate(answers))
    result = call_model_chat_completions(curr_prompt)
    return result.get("text", "").strip() if result.get("ok") else ""

# def handle_logic_reasoning(question:str) -> str:
#     results = []
#     # Call and get the model's output first on the original question
#     result = call_model_chat_completions(question)
#     results.append(result.get("text", ""))
#     # Rephrase it and call again several times
#     prompt = "Rephrase the question below in a different way while keeping the same logic and meaning:\n\n" + question
#     for _ in range(3):
#         rephrased_prompt = call_model_chat_completions(prompt)
#         result = call_model_chat_completions(rephrased_prompt.get("text", ""))
#         results.append(result.get("text", ""))

#     # Produce a final intelligent answer based on all collected responses
    
def classify_problem_type(problem: str) -> str:
    problem = problem.lower()
    
    math_keywords = ['find', 'calculate', 'compute', 'evaluate', 'plus', 'minus','divided by',
                     'sum', 'difference', 'product', 'quotient', 'equation', 'algebra', 'geometry', 'integral', 'derivative', 'area', 'perimeter',
                     'function', 'graph', 'plot', 'matrix', 'vector', 'coordinate', 'axis', 'fraction', 'decimal', 'percentage',
                     'ratio', 'proportion', 'exponent', 'logarithm', 'sequence', 'series',
                     '+', '-', '*', '/', '=', '<', '>', '^',
                     '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    if any(keyword in problem for keyword in math_keywords):
        return "Math"
    
    critical_thinking_keywords = ['explain', 'describe', 'discuss', 'analyze', 'compare', 'contrast', 'evaluate', 'interpret',
                                  'what if', 'implications', 'consequences', 'significance', 'perspective', 'opinion', 'argument', 'debate',
                                  'reason', 'evidence', 'justification', 'rationale', 'theory', 'hypothesis', 'concept', 'idea',
                                 'in detail', 'in depth', 'thoroughly', 'comprehensively',
                                  'critically', 'reflect', 'insight', 'understand', 'meaning', 'deeper', 'broader', 'context',
                                  'convince', 'persuade', 'influence', 'motivate', 'engage', 'challenge', 'question', 'explore',
                                  'curious', 'investigate', 'research', 'study', 'examine', 'probe', 'scrutinize', 'delve',
                                  'debate', 'dispute', 'argue', 'contend', 'assert', 'claim', 'maintain', 'hold', 'believe',
                                  'defend', 'support', 'oppose', 'reject', 'refute', 'counter', 'challenge']
    
    if any(keyword in problem for keyword in critical_thinking_keywords):
        return "Logical Reasoning"


    return "Common Sense"

def rephrase_question(question: str) -> str:
    prompt = (
        "Rewrite the following question in a totally different way, preserving the exact meaning. "
        "Keep it simple and do NOT change the logic:\n\n"
        f"{question}"
    )
    response = call_model_chat_completions(prompt)
    if response.get("ok"):
        return response.get("text", "").strip()
    return ""