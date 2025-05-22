import logging
import os
import tiktoken

from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError

from typing import Iterator

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class OpenAIClient:
    def __init__(
        self,
        embedding_model_name: str = "text-embedding-3-small",
        model_name: str = "gpt-4.1-mini",
    ):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")

        self.client = OpenAI(
            api_key=self.api_key, organization=os.getenv("OPENAI_ORGANIZATION")
        )

        self.embedding_model = embedding_model_name
        self.model = model_name
        self.token_limit = 8192
        self.encoding = tiktoken.encoding_for_model(embedding_model_name)

        self._check_connection()

    def _check_connection(self):
        try:
            self.client.models.list()
            logger.info("Successfully connected to OpenAI.")
        except AuthenticationError as e:
            logger.error("Invalid OpenAI API key.")
            raise RuntimeError("Invalid OpenAI API key.") from e
        except RateLimitError as e:
            logger.error(f"Insufficient quota for OpenAI API: {e}")
            raise RuntimeError("Insufficient quota for OpenAI API.") from e
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise RuntimeError(
                "OpenAI connection failed due to an unexpected error."
            ) from e

    def chat_completion_stream(
        self, prompt: str, max_tokens: int = 100
    ) -> Iterator[str]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt[0]},
                    {"role": "user", "content": prompt[1]},
                ],
                max_tokens=max_tokens,
                temperature=0.7,
                stream=True,
            )

            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    yield f"data: {content}\n\n"
        except Exception as e:
            logger.error(f"Error in chat completion: {e}")
            yield f"event: error\ndata: Sorry, I couldn't process your request.\n\n"

    def get_embedding(self, text: str) -> list[float]:
        """
        Generates an embedding for the input text using the specified OpenAI embedding model.
        """
        try:
            embd_response = self.client.embeddings.create(
                input=text, model=self.embedding_model
            )
            return embd_response.data[0].embedding
        except Exception as e:
            logger.error(f"Error while embedding text: {e}")
            return []

    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Generates embeddings for multiple input texts using the OpenAI embedding model.
        """
        try:
            batches = self.batch_texts(texts)
            embeddings = []
            for batch in batches:
                embd_response = self.client.embeddings.create(
                    input=batch, model=self.embedding_model
                )
                embeddings.extend([item.embedding for item in embd_response.data])
            return embeddings
        except Exception as e:
            logger.error(f"Error while generating embeddings: {e}")
            return []

    def batch_texts(self, texts: list[str]) -> list[list[str]]:
        """
        Batches texts such that each batch stays within the token limit for embedding requests.
        """
        batches = []
        current_batch = []
        current_tokens, total_tokens = 0, 0

        for text in texts:
            token_count = self.count_tokens(text)
            if current_tokens + token_count > self.token_limit:
                if current_batch:
                    batches.append(current_batch)
                current_batch = [text]
                total_tokens += current_tokens
                current_tokens = token_count
            else:
                current_batch.append(text)
                current_tokens += token_count

        if current_batch:
            batches.append(current_batch)
            total_tokens += current_tokens

        logger.info(f"Total tokens recorded: {total_tokens}")
        return batches

    def count_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))
