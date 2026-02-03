import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
SRC_DIR = BASE_DIR / "src"
RESEARCH_DIR = BASE_DIR / "research"
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"

# # Model configuration
MODEL_NAME = "microsoft/phi-3-mini-4k-instruct"
LOCAL_MODEL_PATH = MODELS_DIR / "phi-3"

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# OCR paths (Windows)
# POPPLER_PATH = r"C:/poppler-25.12.0/Library/bin"
# TESSERACT_PATH = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
POPPLER_PATH = r"C:/poppler-25.12.0/Library/bin"
TESSERACT_PATH = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
# Neptune AI
NEPTUNE_PROJECT = "ruffi-22/doc-intelli-rag"


# Adaptive chunking defaults
MIN_CHUNK_SIZE = 100
MAX_CHUNK_SIZE = 1000
DEFAULT_CHUNK_SIZE = 300

# File size thresholds (in bytes)
SMALL_FILE = 100_000    # 100KB
MEDIUM_FILE = 1_000_000  # 1MB
LARGE_FILE = 10_000_000  # 10MB

# Create directories
for dir_path in [MODELS_DIR, DATA_DIR]:
    dir_path.mkdir(exist_ok=True)