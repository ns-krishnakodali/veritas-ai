import unittest
from unittest.mock import MagicMock, patch

import numpy as np

from app.scripts.chunking import chunk_text
from app.scripts.prompt import build_prompt, format_contexts
from app.scripts.store import calculate_lexical_score, normalize_embeddings


class RAGPipelineTests(unittest.TestCase):
    def test_chunk_text_preserves_source_metadata(self):
        chunks = chunk_text(
            "Krishna builds AI platforms.\n\nHe also builds distributed systems.",
            metadata={"source": "about-me.txt"},
        )

        self.assertGreater(len(chunks), 0)
        self.assertEqual(chunks[0]["metadata"]["source"], "about-me.txt")
        self.assertIn("text", chunks[0])

    def test_lexical_score_uses_metadata_for_reranking(self):
        context = {
            "text": "Built a secure file sharing platform.",
            "title": "Q File Share",
            "techstack": ["FastAPI", "Post-Quantum Cryptography"],
        }

        score = calculate_lexical_score("Which project used post quantum crypto?", context)

        self.assertGreater(score, 0)

    def test_normalize_embeddings_handles_zero_vectors(self):
        normalized = normalize_embeddings(np.array([[0.0, 0.0], [3.0, 4.0]]))

        self.assertTrue(np.all(np.isfinite(normalized)))
        self.assertEqual(normalized[0].tolist(), [0.0, 0.0])
        self.assertAlmostEqual(np.linalg.norm(normalized[1]), 1.0)

    def test_build_prompt_passes_query_to_retrieval_and_formats_context(self):
        openai_client = MagicMock()
        openai_client.get_embedding.return_value = [0.1, 0.2]

        with patch("app.scripts.prompt.search_similar_contexts") as search_mock:
            search_mock.return_value = [
                {
                    "text": "Krishna's experience at Hartree involved AI agents.",
                    "source": "about-me.txt",
                    "_score": 0.91,
                }
            ]

            prompt = build_prompt("What did Krishna do at Hartree?", openai_client)

        search_mock.assert_called_once()
        self.assertEqual(
            search_mock.call_args.kwargs["query"], "What did Krishna do at Hartree?"
        )
        self.assertIn("[Snippet 1 | about-me.txt | relevance=0.910]", prompt[1])
        self.assertIn("AI agents", prompt[1])

    def test_format_contexts_skips_empty_text(self):
        formatted = format_contexts(
            [
                {"text": "", "source": "empty.txt"},
                {"text": "Useful context", "title": "Useful", "_score": 0.8},
            ]
        )

        self.assertNotIn("empty.txt", formatted)
        self.assertIn("[Snippet 1 | Useful | relevance=0.800]", formatted)


if __name__ == "__main__":
    unittest.main()
