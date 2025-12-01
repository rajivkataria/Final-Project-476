from src.apiClient import call_model_chat_completions

if __name__ == "__main__":
    result = call_model_chat_completions("What is 2+2?")
    print(result)