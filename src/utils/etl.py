import utils
from vector_db.storages import TokenizedVectorDB


def execute_etl_pipeline(file_path: str, vector_db: TokenizedVectorDB) -> int:
    """Executes loading transformation and saving db state"""
    text = utils.documents.load_pdf_to_text(file_path)
    sentences = utils.nltk.split_text_into_sentences(text)
    chunks = vector_db.create_sentence_chunks(sentences, chunk_size=4, overlap=2)
    vector_db.add_chunks(chunks)
    return len(chunks)
