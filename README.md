## Overview
This service allows users to upload PDF files, convert them to embeddings, and store them in a vector database. Users can then perform similarity searches on the embeddings through FastAPI endpoints. The service can be run both locally or within Docker containers, and it offers flexibility for customization via environment variables. 

The system supports cold-start functionality to load input data during startup and uses a configurable sentence-transformer model for embedding generation.

## Features
- **PDF Upload:** Upload PDF files and convert their contents to embeddings.
- **Search API:** Perform similarity searches on stored embeddings.
- **Cold Start:** Automatically load embeddings from the input directory on startup.
- **Docker and Local Support:** The service can run either locally or via Docker.

---

## Installation

### Local Setup
1. **Clone the repository:**
   ```bash
   git clone git@github.com:NEkropo1/similarity_search_api.git
   cd similarity_search_api
   ```

2. **Install Python 3.11 (if not already installed):**
- On Ubuntu:
   ```bash
   sudo apt update
   sudo apt install -y python3.11 python3.11-venv
   ```
- On MacOS:
   ```bash
   brew install python@3.11
   ```
- On Windows, download and install from [Python.org](https://www.python.org/downloads/release/python-31110/)

3. **Set up a Python 3.11 environment (optional but recommended):**  
   Ensure python3.11 is available and create a virtual environment with it:
   ```bash
   python3.11 -m venv venv  # or python3.11/python3@11, depends on your packaging tool
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies:**
   ```bash
   make install
   ```
   
5. **Create and configure the .env file (or set environment variables directly):**
   ```bash
   cp .env.example ./src/.env  # for docker use: cp .env.example .env
   ```
   Although you can configure everything in config.py, it's not recommended.  

6. **Run the service locally:**
   ```bash
   make run
   ```

   This command will start the service on http://localhost:8003.

### Docker Setup
Docker must be installed. Follow the official guide for your system:
https://www.docker.com/get-started
1. **Build and run the service using Docker Compose:**

    ```bash

   make service_run
   ```  
   
2. **Stop the service:**

    ```bash

   make service_stop
   ```  

3. **Clear containers and volumes**:

    ```bash

   make service_clear
   ```  

### Usage
### 1. API Endpoints

#### Upload PDF
- **Endpoint:** `POST /upload_pdf/`
- **Description:** Upload a PDF file and store its embeddings.
- **Request:**
   ```bash
   curl -F "file=@<path_to_pdf>" http://localhost:8003/upload_pdf/
   ```

### Notes

#### Cold Start Behavior
If `COLD_START` is set to `True`, the service will process all files in the `input/` directory during startup and store their embeddings.

#### Docker Volumes and Paths
Ensure that paths in the `.env` file are correctly mapped to Docker volumes if running in a container.

#### File Handling
Uploaded files are saved to the `input/` directory defined in `CONFIG['INPUT_PATH']`.



```markdown
### Configuration Options

| Environment Variable | Default Value                                   | Description                                              |
|----------------------|-------------------------------------------------|----------------------------------------------------------|
| `ENVIRONMENT`        | `LOCAL`                                         | Set to `LOCAL` for local setup or `PRODUCTION` for Docker |
| `COLD_START`         | `True`                                          | Whether to initialize vector DB with files at startup    |
| `VECTOR_DB_PATH`     | `vector_db/index.faiss`                         | Path to the vector database                              |
| `EMBEDDING_MODEL`    | `sentence-transformers/all-MiniLM-L6-v2`        | Model for embedding generation                           |
| `BEST_K_ELEMENTS`    | `3`                                             | Number of top results to return for search queries       |
| `CHUNK_SIZE`         | `320`                                           | Size of chunks for embedding input                      |
```
