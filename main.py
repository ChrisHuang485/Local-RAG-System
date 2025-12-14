import os
import time
import config
from src import utils, loader, cleaner, engine


def main():
    utils.setup_environment()
    print("-"*50)
    print("   Local RAG System   ")
    print("   Model: {config.LLM_MODEL_NAME} | Offline Mode: ON")
    print("-"*50)
    utils.check_and_start_ollama()


    while True:
        default_path = config.DEFAULT_KNOWLEDGE_BASE
        user_path = input("\nPlease input file/folder path (Default: '{default_path}'): ").strip()
        if not user_path:
            user_path = default_path
        
        if os.path.exists(user_path):
            break
        else:
            print("Path doesn't exist., please enter again.")

    documents = loader.load_documents_from_path(user_path)
    if not documents:
        print("No valid documents found. Exiting.")
        return


    # PII Scrubbing
    documents = cleaner.process_documents_pii(documents)

    print("\n" + "-"*50)
    print("Custom Prompt Configuration")
    print("-"*50)
    
    user_instructions = input("\nAdditional Prompt Request? (e.g., 'Answer in a list format', 'Keep replies under 50 characters') [Press Enter to skip]: ").strip()
    if not user_instructions:
        user_instructions = "None."

    rag_system = engine.RAGPipeline()
    rag_system.initialize_models()
    qa_chain = rag_system.build_chain(documents, user_prompt_req=user_instructions)

    print("\nSystem Ready. (Type 'exit', 'quit', or 'q' to quit)")
    print("-" * 50)


# Interactive Loop
    while True:
        query = input("\nAsk any question: ").strip()
        
        if query.lower() in ['exit', 'quit', 'q']:
            print("Bye!")
            break
        
        if not query:
            continue

        start_time = time.time()
        print("thinking...", end="\r")

        try:
            result = qa_chain.invoke({"query": query})
            end_time = time.time()
            print(" " * 20, end="\r")

            print(f"Answer: {result['result']}")
            
            # source
            if result.get('source_documents'):
                source = result['source_documents'][0]
                file_name = os.path.basename(source.metadata['source'])
                print(f"\nSource document: {file_name}")
                # document preview
                snippet = source.page_content.replace('\n', ' ')[:100]
                print(f"Preview: ...{snippet}...")
            else:
                print("\nDidn't find in document")
            
            print(f"Time: {end_time - start_time:.2f}s")
            print("-" * 50)

        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
            