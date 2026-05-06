import logging
import os
import json

from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


def chunk_text(
    text_data: str,
    chunk_size: int = 900,
    chunk_overlap: int = 150,
    metadata: dict | None = None,
) -> list[dict]:
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
    raw_metadata = metadata or {}
    return [
        {
            "text": " ".join(chunk.splitlines()).strip(),
            "metadata": {**raw_metadata, "chunk_id": idx},
        }
        for idx, chunk in enumerate(text_splitter.split_text(text_data))
        if chunk.strip()
    ]


def chunk_json(
    json_data: list[dict],
    chunk_size: int = 900,
    chunk_overlap: int = 150,
    source_file: str | None = None,
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
        if source_file:
            raw_metadata = {**raw_metadata, "source": source_file}

        chunks = text_splitter.split_text(text)
        for idx, chunk in enumerate(chunks):
            data_chunks.append(
                {
                    "text": " ".join(chunk.splitlines()).strip(),
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
        file_path = os.path.join(data_path, file_name)
        if file_extension == ".json":
            with open(file_path, "r", encoding="utf-8") as am_file:
                file_content = json.load(am_file)
            chunks.extend(chunk_json(file_content, source_file=file_name))
        else:
            with open(file_path, "r", encoding="utf-8") as am_file:
                file_content = am_file.read()
            chunks.extend(chunk_text(file_content, metadata={"source": file_name}))

    return chunks
