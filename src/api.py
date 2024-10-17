from fastapi import FastAPI, File, HTTPException, UploadFile
from loguru import logger

import coldstart
from config import CONFIG
from vector_db.storages import TokenizedVectorDB

vector_db = TokenizedVectorDB(
    embedding_model=CONFIG["EMBEDDING_MODEL"],
    db_path=CONFIG["VECTOR_DB_PATH"]
)
if CONFIG["COLD_START"]:
    coldstart.init(vector_db)


app = FastAPI()


@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF, process it, and store embeddings."""
    file_path = f"{CONFIG['INPUT_PATH']}/{file.filename}"
    try:
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        logger.info(f"Uploaded and saved file: {file_path}")
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail="Failed to save file.")

    return {"status": "Embeddings stored"}


@app.post("/search/")
async def search(query: str, top_k: int = CONFIG["BEST_K_ELEMENTS"]):
    """Search the vector database for the top-k most similar sentences."""
    results = vector_db.search(query, top_k=top_k)
    if not results:
        raise HTTPException(status_code=404, detail="No relevant results found.")
    # TODO: here could be more complicated problems, different types of numpy etc
    #  so each should be properly handled
    len_results = len(results)
    if len_results < top_k:
        logger.warning(f"For query: {query}, top_k: {top_k} only {len_results} found.")

    # TODO: format return x integers after coma
    return {"results": [[result[0], float(result[1])] for result in results]}
