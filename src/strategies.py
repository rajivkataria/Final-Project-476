import re


# Method to classify the problem into Math or Non-Math
# Classifying a problem will help in selecting strategies like how many calls to make and whether to use other stategies like self-reflection or self-consistency

def get_math_output(s: str):
    if s is None:
        return ""
    out = re.search(r"-?\d+(\.\d+)?", s)
    
    if out:
        return out.group(0)
    return ""

def extra_check_math(problem: str, iterations:int) -> str:
    results = []
    for i in range(iterations):
        response = get_math_output(problem)
        results.append(response)
    
    

def classify_problem_type(problem: str) -> str:
    problem = problem.lower()
    
    math_keywords = ['solve', 'find', 'calculate', 'compute', 'determine', 'evaluate','how many', 'plus', 'minus','divided by',
                     'sum', 'difference', 'product', 'quotient', 'equation', 'algebra', 'geometry', 'integral', 'derivative', 'area', 'perimeter',
                     'length', 'width', 'height', 'radius', 'circumference', 'angle', 'triangle', 'circle', 'square', 'rectangle',
                     'probability', 'statistics', 'mean', 'median',
                     'function', 'graph', 'plot', 'matrix', 'vector', 'coordinate', 'axis', 'fraction', 'decimal', 'percentage',
                     'ratio', 'proportion', 'exponent', 'logarithm', 'sequence', 'series', 'inequality',
                     'weight', 'mass', 'volume', 'density', 'force', 'energy', 'power',
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
        return "Critical Thinking"


    return "Common Sense"