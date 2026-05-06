import os
import unittest

from types import SimpleNamespace
from unittest.mock import patch

from app.openai.openai_client import OpenAIClient


class OpenAIClientModelTests(unittest.TestCase):
    def build_client(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False):
            with patch.object(OpenAIClient, "_check_connection", return_value=None):
                with patch("app.openai.openai_client.OpenAI") as openai_mock:
                    client = OpenAIClient()
                    api_client = openai_mock.return_value
        return client, api_client

    def test_default_models_keep_embeddings_and_generation_separate(self):
        client, _ = self.build_client()

        self.assertEqual(client.embedding_model, "text-embedding-3-small")
        self.assertEqual(client.model, "gpt-5.4-nano")

    def test_embedding_request_uses_embedding_model(self):
        client, api_client = self.build_client()
        api_client.embeddings.create.return_value = SimpleNamespace(
            data=[SimpleNamespace(embedding=[0.1, 0.2])]
        )

        self.assertEqual(client.get_embedding("hello"), [0.1, 0.2])
        api_client.embeddings.create.assert_called_once_with(
            input="hello", model="text-embedding-3-small"
        )

    def test_chat_completion_uses_generation_model(self):
        client, api_client = self.build_client()
        chunk = SimpleNamespace(
            choices=[SimpleNamespace(delta=SimpleNamespace(content="hello"))]
        )
        api_client.chat.completions.create.return_value = iter([chunk])

        chunks = list(client.chat_completion_stream(["system", "user"]))

        self.assertEqual(chunks, ["data: hello\n\n"])
        api_client.chat.completions.create.assert_called_once()
        call_kwargs = api_client.chat.completions.create.call_args.kwargs
        self.assertEqual(call_kwargs["model"], "gpt-5.4-nano")
        self.assertEqual(call_kwargs["max_completion_tokens"], 450)
        self.assertEqual(call_kwargs["reasoning_effort"], "low")
        self.assertNotIn("temperature", call_kwargs)
        self.assertEqual(call_kwargs["messages"][0]["role"], "developer")
        self.assertTrue(call_kwargs["stream"])


if __name__ == "__main__":
    unittest.main()
