import os
from langchain_community.document_loaders import (
    TextLoader, 
    PyPDFLoader, 
    Docx2txtLoader, 
    UnstructuredPowerPointLoader
)

LOADER_MAPPING = {
    ".txt": (TextLoader, {"encoding": "utf-8"}),
    ".pdf": (PyPDFLoader, {}),
    ".docx": (Docx2txtLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
}

def load_documents_from_path(user_path: str):
    documents = []
    
    if os.path.isfile(user_path):
        files_to_load = [user_path]
        root_dir = os.path.dirname(user_path)
    elif os.path.isdir(user_path):
        files_to_load = []
        for root, dirs, files in os.walk(user_path):
            for file in files:
                files_to_load.append(os.path.join(root, file))
    else:
        print(f"Error, can't find '{user_path}'")
        return []

    # Traverse directory
    for file_path in files_to_load:
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in LOADER_MAPPING:
            loader_class, loader_args = LOADER_MAPPING[ext]
            try:
                print(f"Loading: {os.path.basename(file_path)}")
                loader = loader_class(file_path, **loader_args)
                docs = loader.load()
                documents.extend(docs)
            except Exception as e:
                print(f"Can't loading {file}: {e}")

    return documents