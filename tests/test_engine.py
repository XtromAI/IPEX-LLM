import unittest
from unittest.mock import MagicMock, patch
import sys

# Mock modules before importing src.engine to avoid ImportError if dependencies are missing
# and to allow mocking the classes
sys.modules["intel_extension_for_pytorch"] = MagicMock()
sys.modules["ipex_llm"] = MagicMock()
sys.modules["ipex_llm.transformers"] = MagicMock()

# We need to ensure AutoModelForCausalLM is available in the mocked module
mock_ipex_transformers = sys.modules["ipex_llm.transformers"]
mock_ipex_transformers.AutoModelForCausalLM = MagicMock()

from src.engine import InferenceEngine
from src.config import InferenceConfig

class TestInferenceEngine(unittest.TestCase):
    def setUp(self):
        # Use cpu to avoid xpu checks in the engine code that might fail with mocks
        self.config = InferenceConfig(model_id="test-model", device="cpu") 
        
    @patch("src.engine.AutoTokenizer")
    def test_load_model(self, mock_tokenizer_cls):
        # Setup mocks
        mock_model_cls = mock_ipex_transformers.AutoModelForCausalLM
        mock_model = MagicMock()
        mock_model_cls.from_pretrained.return_value = mock_model
        
        mock_tokenizer = MagicMock()
        mock_tokenizer_cls.from_pretrained.return_value = mock_tokenizer
        
        # Init engine
        engine = InferenceEngine(self.config)
        
        # Call load_model
        engine.load_model()
        
        # Verify calls
        mock_tokenizer_cls.from_pretrained.assert_called_with("test-model", trust_remote_code=True)
        mock_model_cls.from_pretrained.assert_called_with(
            "test-model", 
            load_in_4bit=True, 
            trust_remote_code=True, 
            use_cache=True
        )
        
        self.assertEqual(engine.model, mock_model)
        self.assertEqual(engine.tokenizer, mock_tokenizer)

    @patch("src.engine.AutoTokenizer")
    def test_generate(self, mock_tokenizer_cls):
        # Setup mocks
        mock_model_cls = mock_ipex_transformers.AutoModelForCausalLM
        mock_model = MagicMock()
        mock_model_cls.from_pretrained.return_value = mock_model
        
        mock_tokenizer = MagicMock()
        mock_tokenizer_cls.from_pretrained.return_value = mock_tokenizer
        
        # Mock encode/decode
        mock_tokenizer.encode.return_value = MagicMock() # tensor
        mock_tokenizer.decode.return_value = "Generated text"
        
        mock_model.generate.return_value = [MagicMock()] # output ids
        
        engine = InferenceEngine(self.config)
        engine.load_model()
        
        output = engine.generate("Test prompt")
        
        self.assertEqual(output, "Generated text")
        mock_model.generate.assert_called_once()

if __name__ == "__main__":
    unittest.main()
