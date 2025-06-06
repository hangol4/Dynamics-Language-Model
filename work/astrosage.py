from llama_cpp import Llama 
from huggingface_hub import hf_hub_download 
import os 
import sys 
import contextlib

# Suppress warnings
@contextlib.contextmanager 
def suppress_stderr(): 
    stderr = sys.stderr 
    with open(os.devnull, 'w') as devnull: 
        sys.stderr = devnull 
        try: 
            yield 
        finally: 
            sys.stderr = stderr 

# or change the filename to AstroSage-8B-BF16.gguf for BF16 quantization
def download_model(repo_id="AstroMLab/AstroSage-8B-GGUF", filename="AstroSage-8B-Q8_0.gguf"): 
    try: 
        os.makedirs("models", exist_ok=True) 
        local_path = os.path.join("models", filename) 
        if not os.path.exists(local_path): 
            print(f"Downloading {filename}...") 
            with suppress_stderr(): 
                local_path = hf_hub_download( 
                    repo_id=repo_id, 
                    filename=filename, 
                    local_dir="models", 
                    local_dir_use_symlinks=False 
                ) 
            print("Download complete!") 
        return local_path 
    except Exception as e: 
        print(f"Error downloading model: {e}") 
        raise 

def initialize_llm(): 
    model_path = download_model() 
    with suppress_stderr(): 
        return Llama( 
            model_path=model_path, 
            n_ctx=2048, 
            n_threads=4 
        ) 

def get_response(llm, prompt, max_tokens=128): 
    response = llm( 
        prompt, 
        max_tokens=max_tokens, 
        temperature=0.7, 
        top_p=0.9, 
        top_k=40, 
        repeat_penalty=1.1, 
        stop=["User:", "\n\n"] 
    ) 
    return response['choices'][0]['text'] 

def main(): 
    llm = initialize_llm()
    
    # Example question about galaxy formation
    first_question = "How does a galaxy form?"
    print("\nQuestion:", first_question)
    print("\nAI:", get_response(llm, first_question).strip(), "\n")
    
    print("\nYou can now ask more questions! Type 'quit' or 'exit' to end the conversation.\n")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ['quit', 'exit']:
                print("\nGoodbye!")
                break
                
            print("\nAI:", get_response(llm, user_input).strip(), "\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__": 
    main()
