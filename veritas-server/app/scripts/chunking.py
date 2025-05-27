import logging
import os
import json

from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


def chunk_text(
    text_data: str, chunk_size: int = 500, chunk_overlap: int = 100
) -> list[str]:
    """
    Splits raw text into smaller overlapping chunks using recursive character splitting.
    """
    logging.debug(f"Chunking text: {text_data}")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ".", "?", " ", ""],
    )
    return text_splitter.split_text(text_data)


def chunk_json(
    json_data: list[dict], chunk_size: int = 500, chunk_overlap: int = 100
) -> list[dict]:
    """
    Splits a list of JSON entries into smaller overlapping chunks, preserving and updating metadata.
    """
    logging.debug(f"Chunking JSON: {json_data}")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    data_chunks = []
    for entry in json_data:
        text = entry.get("text", "")
        raw_metadata = entry.get("metadata", {})

        chunks = text_splitter.split_text(text)
        for idx, chunk in enumerate(chunks):
            data_chunks.append(
                {
                    "text": " ".join(chunk.splitlines()),
                    "metadata": {**raw_metadata, "chunk_id": idx},
                }
            )

    return data_chunks


def chunk_data_from_path(data_path):
    """
    Scan and chunk all the raw data from files in the `data_path`.
    """
    logger.info(f"Chunking data from path: {data_path}")

    chunks = list()
    for file_name in os.listdir(data_path):
        file_content = str()
        file_extension = os.path.splitext(file_name)[1].lower()
        if file_extension == ".json":
            with open(
                os.path.join(data_path, file_name), "r", encoding="utf-8"
            ) as am_file:
                file_content = json.load(am_file)
            chunks.extend(chunk_json(file_content))
        else:
            with open(
                os.path.join(data_path, file_name), "r", encoding="utf-8"
            ) as am_file:
                file_content = am_file.read()
            chunks.extend(chunk_text(file_content))

    return chunks
