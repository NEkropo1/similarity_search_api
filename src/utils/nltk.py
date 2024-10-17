import nltk
from loguru import logger


def ensure_nltk_resource(resource_name: str) -> None:
    """Check if an NLTK resource exists; download if missing."""
    try:
        nltk.data.find(f"tokenizers/{resource_name}")
        logger.info(f"'{resource_name}' is already available.")
    except LookupError:
        logger.info(f"Downloading '{resource_name}'...")
        nltk.download(resource_name)


def split_text_into_sentences(text: str) -> list[str]:
    """Split text into a list of sentences."""
    return nltk.sent_tokenize(text)
