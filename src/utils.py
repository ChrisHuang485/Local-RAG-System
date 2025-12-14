import os
import time
import subprocess
import urllib.request
from urllib.error import URLError

def setup_environment():
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['TRANSFORMERS_OFFLINE'] = '1'

def check_and_start_ollama(port=11434):
    ollama_url = "http://localhost:{port}"
    
    # try to connect Ollama
    try:
        with urllib.request.urlopen(ollama_url) as response:
            if response.status == 200:
                return
    except (URLError, ConnectionRefusedError):
        pass

    # 2. autorun ollama
    try:
        if os.name == 'nt':
            process = subprocess.Popen(
                ["ollama", "serve"], 
                creationflags=subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            process = subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            

        for _ in range(20):
            try:
                with urllib.request.urlopen(ollama_url) as response:
                    if response.status == 200:
                        return
            except:
                time.sleep(1)
                print(".", end="", flush=True)
        
        print("\nCan't launch Ollama, Please try opening the software manually.")
        exit(1)
        
    except FileNotFoundError:
        print("\nError: Command ‘ollama’ not found. Please ensure Ollama is installed and added to your system environment variable (PATH).")
        exit(1)