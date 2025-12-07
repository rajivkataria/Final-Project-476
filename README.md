# Final-Project-476

This project implements a simple inference-time reasoning agent that answers the final test dataset using only the ASU-provided LLM API.

What the Agent Does:

1. Wraps the API through call_model_chat_completions.

2. Classifies each prompt into basic categories (Math, Logical Reasoning, Common Sense).

3. Produces a final answer using a single or minimal set of model calls depending on the prompt.

4. Ensures all outputs follow the required format for grading.

Repository Structure
/src
   agent.py            main agent  
   strategies.py       problem classification & strategies  
   apiClient.py        API wrapper

/data
   cse_476_final_project_test_data.json

generate_answer_template.py   → script to produce final answers JSON  
README.md