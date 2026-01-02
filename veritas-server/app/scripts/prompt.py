import logging
import numpy as np

from app.openai.openai_client import OpenAIClient
from app.scripts.store import search_similar_contexts

logger = logging.getLogger(__name__)


def build_prompt(query: str, openai_client: OpenAIClient) -> list[str]:
    """
    Construct the prompt using contexts retrieved from relevant embeddings.
    """
    logger.info(f"Building prompt for: {query}")

    embedding = openai_client.get_embedding(query)
    embeddings_np = np.array(embedding).astype("float32")
    query_embedding = embeddings_np.reshape(1, -1)

    # Fetch contexts from vector store
    contexts = search_similar_contexts(query_embedding)
    context_texts = [ctx.get("text", "") for ctx in contexts if ctx.get("text")]
    combined_context = "\n---\n".join(context_texts)

    prompt = [
        (
            "You are Veritas AI, a helpful and knowledgeable personal assistant designed to answer questions about Krishna using the provided context.\n\n"
            "If the user's message is a greeting (e.g., 'hi', 'hello', or similar), respond with a brief welcome and introduction such as: "
            "'Hi, I'm Veritas AI - here to help you learn more about Krishna.'\n\n"
            "For all other queries, provide a clear, well-polished, and professional answer grounded strictly in the provided context. "
            "You may rephrase, summarize, or improve clarity, but you must not add, infer, or assume any information beyond the context.\n\n"
            "Be accurate, concise, and factual.\n"
            "If the answer cannot be determined from the context, respond exactly with: "
            "'Hmm, I don't have a verified answer to that question.'\n\n"
        ),
        (f"Context:\n{combined_context}\n\n" f"User Query: {query}\n\n" "Answer:"),
    ]

    return prompt
