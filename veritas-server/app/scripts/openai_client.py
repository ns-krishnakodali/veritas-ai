import logging
import os
import tiktoken

from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class OpenAIClient:
    def __init__(self, model_name: str = "text-embedding-3-small"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")

        self.model_name = model_name
        self.client = OpenAI(
            api_key=self.api_key, organization=os.getenv("OPENAI_ORGANIZATION")
        )
        self.token_limit = 8192
        self.encoding = tiktoken.encoding_for_model(model_name)

        self._check_connection()

    def _check_connection(self):
        try:
            self.client.models.list()
            logger.info("Successfully connected to OpenAI.")
        except AuthenticationError:
            logger.error("Invalid OpenAI API key.")
        except RateLimitError as e:
            logger.error(f"Insufficient quota for OpenAI API: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")

    def get_embedding(self, text: str) -> list[float]:
        """
        Generates an embedding for the input text using the specified OpenAI embedding model.
        """
        try:
            embd_response = self.client.embeddings.create(
                input=text, model=self.model_name
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
                    input=batch, model=self.model_name
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
            token_count = len(self.encoding.encode(text))
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

        logger.info(f"Total tokens recordes: {total_tokens}")
        return batches
