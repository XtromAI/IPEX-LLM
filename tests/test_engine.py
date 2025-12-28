import unittest
from unittest.mock import MagicMock, patch

from src.engine import InferenceEngine
from src.config import InferenceConfig


class TestInferenceEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.config = InferenceConfig(
            model="test-model",
            host="http://localhost:11434",
            stream=False,
            options={"temperature": 0.0},
        )

    @patch("src.engine.requests.get")
    def test_load_model_performs_health_check(self, mock_get: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        engine = InferenceEngine(self.config)
        engine.load_model()

        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertTrue(args[0].startswith("http://localhost:11434"))

    @patch("src.engine.requests.post")
    def test_generate_calls_ollama_and_returns_response(self, mock_post: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"response": "Generated text"}
        mock_post.return_value = mock_response

        engine = InferenceEngine(self.config)
        result = engine.generate("Test prompt")

        self.assertEqual(result, "Generated text")

        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].endswith("/api/generate"))
        payload = kwargs["json"]
        self.assertEqual(payload["model"], "test-model")
        self.assertEqual(payload["prompt"], "Test prompt")
        self.assertEqual(payload["stream"], False)


if __name__ == "__main__":
    unittest.main()

