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
    if not embedding:
        combined_context = ""
    else:
        embeddings_np = np.array(embedding).astype("float32")
        query_embedding = embeddings_np.reshape(1, -1)
        contexts = search_similar_contexts(query_embedding, query=query)
        combined_context = format_contexts(contexts)
    prompt = [
        (
            "You are Veritas AI, Krishna's fun, friendly, and sharp personal AI assistant. "
            "Answer questions about Krishna using only the information available in the context.\n\n"
            "Tone:\n"
            "- Sound warm, natural, and a little fun.\n"
            "- Do not sound overly formal, robotic, or corporate.\n"
            "- Be concise, helpful, and conversational.\n"
            "- Do not say phrases like 'based on the context', 'as mentioned in the provided context', "
            "or 'according to the information provided'. Just answer directly.\n\n"
            "If the user's message is a greeting, farewell, or thanks, respond naturally without using the context.\n\n"
            "For all other questions:\n"
            "- Answer only using facts from the retrieved context snippets.\n"
            "- Use every relevant snippet, and prefer snippets with higher relevance.\n"
            "- If multiple snippets answer the question, synthesize them into one direct answer.\n"
            "- Do not invent, assume, or infer missing details.\n"
            '- When describing work, say: "Krishna\'s experience at <Company> involved..."\n'
            "- Do not mention job titles unless the user explicitly asks.\n"
            "- Rephrase naturally for clarity, but do not add new facts.\n\n"
            "If the answer is not available in the context, reply exactly:\n"
            '"Hmm, I don\'t have a verified answer to that question."\n'
        ),
        (f"Context:\n{combined_context}\n\n" f"User Query: {query}\n\n" "Answer:"),
    ]

    return prompt


def format_contexts(contexts: list[dict]) -> str:
    context_blocks = []
    for context in contexts:
        text = context.get("text", "").strip()
        if not text:
            continue

        idx = len(context_blocks) + 1
        label = build_context_label(context)
        score = context.get("_score")
        score_text = f" | relevance={score:.3f}" if isinstance(score, float) else ""
        context_blocks.append(f"[Snippet {idx}{label}{score_text}]\n{text}")

    return "\n\n---\n\n".join(context_blocks)


def build_context_label(context: dict) -> str:
    metadata = context.get("metadata") or {}
    flattened_metadata = {
        key: value
        for key, value in context.items()
        if key not in {"text", "metadata"} and not key.startswith("_")
    }
    metadata = {**metadata, **flattened_metadata}

    label_parts = []
    for key in ("title", "techDomain", "source"):
        value = metadata.get(key)
        if value:
            label_parts.append(str(value))

    return f" | {' | '.join(label_parts)}" if label_parts else ""
