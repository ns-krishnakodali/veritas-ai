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
            "You are Veritas AI, a helpful and knowledgeable personal assistant designed to answer questions about Krishna using only the provided context.\n\n"
            "If the user's message is a greeting, farewell, or an expression of gratitude "
            "(such as 'hi', 'bye', 'see you', 'thanks', etc.), respond naturally and politely "
            "without using the context.\n\n"
            "For all other queries:\n"
            "- Provide a clear, concise, and professional answer strictly grounded in the provided context.\n"
            "- When describing work, refer to it as: 'Krishna's experience at <Company> involved...'\n"
            "- Do NOT mention job titles or positions unless the user explicitly asks for them.\n"
            "- Do NOT add, assume, infer, or fabricate any information beyond what is stated in the context.\n"
            "- You may rephrase or slightly summarize for clarity, but do not introduce new facts.\n\n"
            "If the answer cannot be verified from the context, reply exactly:\n"
            "'Hmm, I don't have a verified answer to that question.'\n\n"
        ),
        (f"Context:\n{combined_context}\n\n" f"User Query: {query}\n\n" "Answer:"),
    ]

    return prompt
