"""
Basic LLM Example with Ollama
Run: python main.py
"""
import requests

def query_ollama(prompt, model="llama2"):
    """Query Ollama API"""
    url = "http://127.0.0.1:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()["response"]
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("Basic LLM Example")
    print("Make sure Ollama is running: ollama serve")
    print()
    
    prompt = "Explain artificial intelligence in simple terms"
    print(f"Question: {prompt}")
    print("Thinking...")
    
    response = query_ollama(prompt, model="phi:2.7b")
    #response = query_ollama(prompt, model="gpt-oss:20b")
    
    print(f"AI Response: {response}")
