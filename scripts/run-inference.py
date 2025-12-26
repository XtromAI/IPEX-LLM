import argparse
import sys
import os

# Add project root to path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.engine import InferenceEngine
from src.config import InferenceConfig

def main():
    parser = argparse.ArgumentParser(description="Run inference on Intel Arc 140V")
    parser.add_argument("--prompt", type=str, default="Hello, world!", help="Input prompt")
    parser.add_argument("--model", type=str, help="Model ID (optional, overrides config)")
    
    args = parser.parse_args()
    
    config = InferenceConfig()
    if args.model:
        config.model_id = args.model
        
    print(f"Initializing Inference Engine for device: {config.device}")
    engine = InferenceEngine(config)
    
    try:
        engine.load_model()
        output = engine.generate(args.prompt)
        print("\n--- Output ---")
        print(output)
        print("--------------\n")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
