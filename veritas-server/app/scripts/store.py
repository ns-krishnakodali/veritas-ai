import faiss
import logging
import numpy as np
import os
import pickle
import re

logger = logging.getLogger(__name__)

EMBEDDINGS_PATH = os.path.join("app", "data", "embeddings")
EMBEDDING_DIMENSION = 1536
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "for",
    "from",
    "has",
    "he",
    "his",
    "in",
    "is",
    "it",
    "krishna",
    "of",
    "on",
    "or",
    "tell",
    "the",
    "to",
    "what",
    "which",
    "who",
    "with",
}


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
    query_embedding: np.ndarray,
    query: str = "",
    k: int = 8,
    fetch_k: int = 24,
    similarity_threshold: float = 0.12,
):
    """
    Searches for top-k most similar context chunks based on the query embedding.
    """
    faiss_index, context_list = load_context()
    if faiss_index is None or context_list is None:
        logger.error("Failed to load FAISS index or context.")
        return []
    if faiss_index.ntotal == 0:
        logger.warning("FAISS index is empty.")
        return []

    query_embedding = normalize_embeddings(query_embedding)
    candidate_count = min(fetch_k, faiss_index.ntotal)
    similarities, indices = faiss_index.search(query_embedding, candidate_count)

    results = []
    for similarity, idx in zip(similarities[0], indices[0]):
        if idx == -1:
            continue
        if idx >= len(context_list):
            break

        if similarity >= similarity_threshold:
            context = context_list[idx].copy()
            lexical_score = calculate_lexical_score(query, context)
            context["_score"] = float((0.82 * similarity) + (0.18 * lexical_score))
            context["_vector_score"] = float(similarity)
            context["_lexical_score"] = float(lexical_score)
            results.append(context)

    results.sort(key=lambda context: context["_score"], reverse=True)
    results = results[:k]
    logger.info(f"Found {len(results)} ranked contexts above similarity threshold")

    return results


def normalize_embeddings(embeddings: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    return embeddings / np.maximum(norms, 1e-12)


def calculate_lexical_score(query: str, context: dict) -> float:
    query_terms = tokenize_for_search(query)
    if not query_terms:
        return 0.0

    metadata = get_context_metadata(context)
    searchable_parts = [context.get("text", "")]
    for value in metadata.values():
        if isinstance(value, list):
            searchable_parts.extend(str(item) for item in value)
        else:
            searchable_parts.append(str(value))

    context_terms = tokenize_for_search(" ".join(searchable_parts))
    if not context_terms:
        return 0.0

    return len(query_terms.intersection(context_terms)) / len(query_terms)


def get_context_metadata(context: dict) -> dict:
    metadata = context.get("metadata") or {}
    flattened_metadata = {
        key: value
        for key, value in context.items()
        if key not in {"text", "metadata"} and not key.startswith("_")
    }
    return {**metadata, **flattened_metadata}


def tokenize_for_search(text: str) -> set[str]:
    terms = set(re.findall(r"[a-z0-9+#.]+", text.lower()))
    return {term for term in terms if len(term) > 1 and term not in STOPWORDS}
