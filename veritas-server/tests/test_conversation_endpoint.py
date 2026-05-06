import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from main import app


class ConversationEndpointTests(unittest.TestCase):
    def test_conversation_endpoint_streams_rag_response(self):
        openai_client = MagicMock()
        openai_client.count_tokens.return_value = 2
        openai_client.chat_completion_stream.return_value = iter(["data: answer\n\n"])

        with patch(
            "app.api.conversation.OpenAIClient", return_value=openai_client
        ) as openai_client_class:
            with patch(
                "app.api.conversation.build_prompt", return_value=["system", "user"]
            ) as build_prompt:
                response = TestClient(app).post(
                    "/api/conversation", json={"query": "Who is Krishna?"}
                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["content-type"], "text/event-stream; charset=utf-8"
        )
        self.assertIn("data: answer", response.text)
        self.assertIn("event: done\ndata: [DONE]", response.text)
        openai_client_class.assert_called_once_with()
        build_prompt.assert_called_once_with("Who is Krishna?", openai_client)
        openai_client.chat_completion_stream.assert_called_once_with(["system", "user"])


if __name__ == "__main__":
    unittest.main()
