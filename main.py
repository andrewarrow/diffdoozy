#!/usr/bin/env python3

import json
import re
import requests
import subprocess
import sys

# test
# amore

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


def get_git_diff():
    """Get git diff output"""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return ""

def get_first_300_words(text):
    """Extract first 300 words from text"""
    words = text.split()
    return " ".join(words[:300])

def main():
    # Get git diff output
    diff_output = get_git_diff()
    
    if not diff_output:
        print("No git diff output found", file=sys.stderr)
        sys.exit(1)
    
    # Get first 300 words
    first_300_words = get_first_300_words(diff_output)
    
    # Create prompt for ollama
    prompt = f"Please summarize the following git diff in 80 chars max but do not start your reply with A diff showing changes to etc. Just start with the actual summary. Here is the diff:\n\n{first_300_words}"
    
    # Send to ollama
    result = run_ollama(prompt)
    if result:
        # Enforce 80 character limit by truncating if needed
        truncated_result = result[:80]
        print(truncated_result)


if __name__ == "__main__":
    main()
