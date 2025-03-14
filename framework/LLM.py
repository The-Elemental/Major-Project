from transformers import AutoModelForCausalLM, AutoTokenizer
import os

class LLM:
    def __init__(self):
        parent_directory = os.path.abspath(os.path.join(os.getcwd(), '..'))
        print("Language Models not found, Downloading...")
            
        # Specify the model name you want to download
        model_name_7b = "deepseek-ai/deepseek-llm-7b-chat"

        # Download the model and tokenizer to your local cabinet
        self.tokenizer7b = AutoTokenizer.from_pretrained(model_name_7b, cache_dir=parent_directory + '\\LLM\\7B')
        self.model7b = AutoModelForCausalLM.from_pretrained(model_name_7b, cache_dir=parent_directory + '\\LLM\\7B', device_map="auto")

        print("✅ Model (7B) downloaded and/or loaded to:", parent_directory + '\\LLM\\7B')

        # Specify the model name you want to download
        model_name_67b = "deepseek-ai/deepseek-llm-67b-chat"

        # Download the model and tokenizer to your local cabinet
        self.tokenizer67b = AutoTokenizer.from_pretrained(model_name_67b, cache_dir=parent_directory + '\\LLM\\67B')
        self.model67b = AutoModelForCausalLM.from_pretrained(model_name_67b, cache_dir=parent_directory + '\\LLM\\67B', device_map="auto")

        print("✅ Model (67B) downloaded and/or loaded to:", parent_directory + '\\LLM\\67B')