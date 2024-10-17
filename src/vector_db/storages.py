import os
from typing import Any

import faiss
import numpy as np
from loguru import logger
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer

from config import CONFIG


class TokenizedVectorDB:
    def __init__(self, embedding_model: str, db_path: str):
        self.model = SentenceTransformer(embedding_model)
        self.tokenizer = AutoTokenizer.from_pretrained(embedding_model)
        self.embedding_size = self.model.get_sentence_embedding_dimension()
        self.db_path = db_path
        self.index = self.init_db(db_path)
        self.chunks: list[str] = list()

    def init_db(self, db_path: str) -> faiss.IndexFlatL2:
        """Initialize the FAISS index, either by loading or creating a new one."""
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        if os.path.exists(db_path) and os.path.getsize(db_path) > 0:
            logger.info(f"Loading FAISS index from {db_path}")
            return faiss.read_index(db_path)

        logger.info("Creating a new FAISS index")
        index = faiss.IndexFlatL2(self.embedding_size)
        faiss.write_index(index, db_path)
        return index

    def create_sentence_chunks(self, sentences: list[str], chunk_size=3, overlap=1) -> list[str]:
        """Create chunks with overlapping sentences."""
        return [
            " ".join(sentences[i:i + chunk_size])
            for i in range(0, len(sentences), chunk_size - overlap)
        ]

    def add_chunks(self, chunks: list[str]) -> None:
        """Generate embeddings and add them to the FAISS index."""
        valid_chunks = []
        maximum_chunk_size = CONFIG["CHUNK_SIZE"]

        for chunk in chunks:
            tokens = self.tokenizer.tokenize(chunk)

            if len(tokens) > maximum_chunk_size:
                split_chunks = [
                    self.tokenizer.convert_tokens_to_string(tokens[i:i + maximum_chunk_size])
                    for i in range(0, len(tokens), maximum_chunk_size)
                ]
                valid_chunks.extend(split_chunks)
            else:
                valid_chunks.append(chunk)

        embeddings = self.model.encode(valid_chunks, convert_to_numpy=True).astype(np.float32)
        self.index.add(embeddings)
        self.chunks.extend(valid_chunks)
        self.save_index()

    def save_index(self):
        """Save the FAISS index to disk."""
        try:
            logger.info(f"Saving FAISS index to {self.db_path}")
            faiss.write_index(self.index, self.db_path)
        except Exception as e:
            logger.error(f"Failed to save FAISS index: {e}")

    def search(self, query: str, top_k: int = 3) -> list[tuple[list, Any]]:
        """Search for the top-k most similar chunks, returning as many as available."""
        query_embedding = self.model.encode([query], convert_to_numpy=True).astype(np.float32)
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)
        faiss.normalize_L2(query_embedding)

        # Perform the search; return all matches if fewer than top_k exist
        total_chunks = len(self.chunks)
        top_k = min(top_k, total_chunks)

        distances, indices = self.index.search(query_embedding, top_k)

        results = [
            (self.chunks[i], distances[0][j])
            for j, i in enumerate(indices[0])
            if i < total_chunks
        ]

        if not results:
            logger.warning("No relevant results found.")
            return []

        return results
