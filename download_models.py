import os
from huggingface_hub import snapshot_download
import config

def download():
    os.makedirs(config.LOCAL_MODELS_PATH, exist_ok=True)

    print("Downloading Embedding model {config.EMBEDDING_MODEL_PATH}...")
    snapshot_download(
        repo_id=config.EMBEDDING_MODEL_NAME,
        local_dir=config.EMBEDDING_MODEL_PATH,
        local_dir_use_symlinks=False
    )

    print("Downloading Re-ranking model {config.RERANKER_MODEL_PATH}...")
    snapshot_download(
        repo_id=config.RERANKER_MODEL_NAME,
        local_dir=config.RERANKER_MODEL_PATH,
        local_dir_use_symlinks=False
    )

    print("\nDownload complete. Saved in the folder '{config.LOCAL_MODELS_PATH}}'")

if __name__ == "__main__":
    download()