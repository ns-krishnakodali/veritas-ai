import faiss
import logging
import numpy as np
import os
import pickle

logger = logging.getLogger(__name__)

EMBEDDINGS_PATH = os.path.join("app", "data", "embeddings")
EMBEDDING_DIMENSION = 1536


def store_context(embeddings_np: np.ndarray, context: list[dict]):
    """
    Creates a FAISS index from embeddings and saves it along with context.
    """
    try:
        faiss_index = faiss.IndexFlatL2(EMBEDDING_DIMENSION)
        faiss_index.add(embeddings_np)

        os.makedirs(EMBEDDINGS_PATH, exist_ok=True)

        index_path = os.path.join(EMBEDDINGS_PATH, "embeddings.index")
        faiss.write_index(faiss_index, index_path)
        logger.info(f"FAISS index stored at {index_path}")

        context_path = os.path.join(EMBEDDINGS_PATH, "context.pkl")
        with open(context_path, "wb") as f:
            pickle.dump(context, f)
        logger.info(f"Context stored at {context_path}")

    except Exception as e:
        logger.error(f"Error while storing context: {e}")


def load_context():
    """
    Loads the FAISS index and associated context from disk.
    """
    index_path = os.path.join(EMBEDDINGS_PATH, "embeddings.index")
    context_path = os.path.join(EMBEDDINGS_PATH, "context.pkl")

    try:
        faiss_index = faiss.read_index(index_path)
        with open(context_path, "rb") as f:
            context = pickle.load(f)
        logger.info("Successfully loaded FAISS index and context.")
        return faiss_index, context
    except Exception as e:
        logger.error(f"Error while loading context: {e}")
        return None, None
