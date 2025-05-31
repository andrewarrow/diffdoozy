#!/usr/bin/env python3

import json
import re
import requests
import sys

def run_ollama(text):
    """Call Ollama API with the given text"""
    payload = {
        "model": "hf.co/unsloth/DeepSeek-R1-Distill-Llama-8B-GGUF:Q4_K_M",
        "prompt": text,
        "stream": False
    }
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        
        result = response.json()
        response_text = result.get("response", "")
        
        if not response_text:
            return ""
        
        think_end_index = response_text.rfind("</think>")
        if think_end_index == -1:
            print(response_text, end='')
            return response_text
        else:
            final_output = response_text[think_end_index + 8:].strip() 
            if final_output:
                return final_output
        
        return ""
        
    except requests.exceptions.RequestException:
        return ""
    except json.JSONDecodeError:
        return ""


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <text>", file=sys.stderr)
        sys.exit(1)
    
    text = sys.argv[1]
    result = run_ollama(text)
    if result:
        print(result)


if __name__ == "__main__":
    main()
