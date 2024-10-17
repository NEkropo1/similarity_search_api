import os

from loguru import logger

from config import CONFIG
from utils.etl import execute_etl_pipeline
from utils.files import get_docs
from vector_db.storages import TokenizedVectorDB


def init(db_instance: TokenizedVectorDB):
    """Run the ETL pipeline for all PDFs in ./input during cold start."""
    input_dir = CONFIG["INPUT_PATH"]
    pdf_files = get_docs(input_dir)
    # TODO: make not only for pdf files, redundant for test task
    #  Also should implement normal state to track already converted files

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        logger.info(f"Processing PDF: {pdf_path}")

        try:
            execute_etl_pipeline(pdf_path, db_instance)  # type: ignore

            logger.info(f"Successfully processed {pdf_file}.")
        except Exception as e:
            logger.error(f"Failed to process {pdf_file}: {e}")
