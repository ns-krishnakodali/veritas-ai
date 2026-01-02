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
        normalized_embeddings = normalize_embeddings(embeddings_np)
        faiss_index = faiss.IndexFlatIP(EMBEDDING_DIMENSION)
        faiss_index.add(normalized_embeddings)

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


def search_similar_contexts(
    query_embedding: np.ndarray, k: int = 5, similarity_threshold: float = 0.1
):
    """
    Searches for top-k most similar context chunks based on the query embedding.
    """
    faiss_index, context_list = load_context()
    if faiss_index is None or context_list is None:
        logger.error("Failed to load FAISS index or context.")
        return []

    query_embedding = query_embedding / np.linalg.norm(
        query_embedding, axis=1, keepdims=True
    )
    similarities, indices = faiss_index.search(query_embedding, k)

    results = []
    for similarity, idx in zip(similarities[0], indices[0]):
        if idx == -1:
            continue
        if idx >= len(context_list):
            break

        if similarity >= similarity_threshold:
            results.append(context_list[idx])

    logger.info(f"Found {len(results)} contexts above similarity threshold")

    return results


def normalize_embeddings(embeddings: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    return embeddings / norms
