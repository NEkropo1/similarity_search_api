import os
from pathlib import Path

from dotenv import load_dotenv

from utils import text

BASE_DIR = Path(__file__).resolve().parent


def load_config() -> dict:
    """Load and return configuration settings."""
    environment = os.getenv("ENVIRONMENT", "LOCAL").upper()

    if environment == "LOCAL":
        load_dotenv(BASE_DIR / ".env")
        local_coldstart = True
    else:
        local_coldstart = False

    cold_start = text.parse_bool(os.getenv("COLD_START"), local_coldstart)
    vector_db_path = os.getenv(
        "VECTOR_DB_PATH",
        BASE_DIR / "vector_db/index.faiss"
    )
    embedding_model = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    best_k_elements = int(os.getenv(
        "BEST_K_ELEMENTS", "3"
    ))
    chunk_size = int(os.getenv(
        "CHUNK_SIZE", "320"
    ))
    input_files_dir = (BASE_DIR / "./input")

    return {
        "ENVIRONMENT": environment,
        "COLD_START": cold_start,
        "VECTOR_DB_PATH": str(vector_db_path),
        "EMBEDDING_MODEL": embedding_model,
        "BEST_K_ELEMENTS": best_k_elements,
        "CHUNK_SIZE": chunk_size,
        "INPUT_PATH": input_files_dir
    }


CONFIG = load_config()
