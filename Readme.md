# Local RAG System

> A privacy-focused, modular, and high-precision Retrieval-Augmented Generation (RAG) system.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangChain](https://img.shields.io/badge/Framework-LangChain-green)
![Ollama](https://img.shields.io/badge/Model-Qwen_14B-purple)
![Architecture](https://img.shields.io/badge/Architecture-Modular-orange)

## Overview

This project is a **fully localized, privacy-focused RAG system**. It employs a layered architecture design to address pain points in enterprise knowledge base retrieval: data privacy leaks, low search accuracy, and difficulties in parsing diverse formats.

System based on **Ollama (LLM)** and **HuggingFace (Embedding/Rerank)**, supports fully offline operation after deployment.

## Features

* Modular architecture, easy to expand and maintain.
* Automatically mask sensitive information such as phone numbers and email addresses.
* Hybrid Search. Significantly increase recall rates.
* Support '.pdf', '.docx', '.pptx', '.txt'.

## Directory Structure

```text
project_root/
├── config.py             
├── download_models.py    
├── main.py               
├── requirements.txt      
└── src/                  
    ├── __init__.py
    ├── utils.py          
    ├── cleaner.py        
    ├── loader.py         
    └── engine.py
```       

## Prerequisites

1. Install and configure Ollama
This project relies on Ollama to run LLM locally.
   
    1. Download and install [Ollama](https://ollama.com).
    2. Open your terminal/command prompt.
    3. Pull the specific model used in config.py (default is Qwen 3 14B):
        ```
        ollama pull qwen3:14b
        ```
        (Note: You can change the model name in config.py if your hardware requires a smaller model like qwen2.5:7b)

3. Install Python Dependencies:
   ```
    pip install -r requirements.txt
   ```

4. Download Embedding Models: Run this script once to cache the BGE-M3 and Re-ranker models locally
   ```
   python download_models.py
   ```

## Usage
1. Run the main application:
   ```
    python main.py
   ```

3. Input the path to your knowledge base (folder or file). Press Enter to use the default path 'my_knowledge_base'.

4. Input any specific instructions for the model (optional). Press Enter to skip.

5. Ask questions based on your knowledge base. Type 'exit', 'quit', or 'q' to terminate the program.

## Configuration
You can modify settings in `config.py` to customize model choices, chunk sizes, and other parameters.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
