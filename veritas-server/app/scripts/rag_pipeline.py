import os

from app.scripts.chunking import chunk_data

DATA_PATH = os.path.join("app", "data", "raw")

for file_name in os.listdir(DATA_PATH):
    chunk_data(DATA_PATH, file_name)
