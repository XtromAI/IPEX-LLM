from typing import Optional

import requests

from src.config import InferenceConfig


class InferenceEngine:
    """Thin wrapper around the local Ollama REST API.

    This engine does not hold the model in-process; it simply forwards
    prompts to the Ollama server running from the portable binary.
    """

    def __init__(self, config: Optional[InferenceConfig] = None) -> None:
        self.config = config or InferenceConfig()

    def _url(self, path: str) -> str:
        base = self.config.host.rstrip("/")
        return f"{base}{path}"

    def load_model(self) -> None:
        """Optional warm-up that verifies the Ollama server is reachable.

        Ollama loads models on demand. This method simply performs a cheap
        request to detect connectivity issues early.
        """

        try:
            response = requests.get(self._url("/"), timeout=5)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError("Failed to reach Ollama server. Is it running?") from exc

    def generate(self, prompt: str) -> str:
        """Generate text via Ollama's /api/generate endpoint.

        The engine expects non-streaming responses and returns the
        consolidated `response` field from Ollama's JSON payload.
        """

        payload = {
            "model": self.config.model,
            "prompt": prompt,
            "stream": self.config.stream,
        }

        if self.config.options:
            payload["options"] = self.config.options

        try:
            response = requests.post(
                self._url("/api/generate"),
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError("Failed to call Ollama generate API.") from exc

        data = response.json()
        return data.get("response", "")

