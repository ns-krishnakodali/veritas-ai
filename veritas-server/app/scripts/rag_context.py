import logging
import numpy as np
import os

from app.openai.openai_client import OpenAIClient
from app.scripts.chunking import chunk_data_from_path
from app.scripts.store import store_context

logger = logging.getLogger(__name__)


def prepare_context_embeddings():
    """
    Generates embeddings from raw data chunks and saves them into a FAISS index along with context.
    """
    texts, context = list(), list()
    openai_client = OpenAIClient()

    raw_data_chunks = chunk_data_from_path(os.path.join("app", "data", "raw"))
    for chunk in raw_data_chunks:
        text = str()
        text_context = {}

        if isinstance(chunk, str):
            text = chunk
        elif isinstance(chunk, dict):
            text = chunk.get("text", "")
            text_context = chunk.get("metadata", {})
        else:
            logger.warning(f"Unknown chunk type: {type(chunk)}. Skipping.")
            continue

        if not text.strip():
            logger.warning("Empty text, skipping chunk.")
            continue

        texts.append(text)
        text_context["text"] = text
        context.append(text_context)

    embeddings = openai_client.get_embeddings(texts)
    if not embeddings:
        logger.error("No embeddings generated, exiting.")
        return

    embeddings_np = np.array(embeddings).astype("float32")
    store_context(embeddings_np, context)
