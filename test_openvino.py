"""
Quick test script for OpenVINO GenAI on Intel Arc GPU
"""
import openvino_genai as ov_genai
import time

def main():
    model_path = "TinyLlama-1.1B-ov"
    
    print("=" * 60)
    print("OpenVINO GenAI Test on Intel Arc 140V")
    print("=" * 60)
    print(f"\nModel: {model_path}")
    print(f"Device: GPU (Intel Arc 140V iGPU)")
    
    # Initialize pipeline
    print("\nLoading model...")
    start_load = time.time()
    pipe = ov_genai.LLMPipeline(model_path, "GPU")
    load_time = time.time() - start_load
    print(f"Model loaded in {load_time:.2f}s")
    
    # Warm-up run
    print("\nWarming up...")
    pipe.generate("Hi", max_new_tokens=5)
    
    # Test prompt
    prompt = "Explain the benefits of unified memory architecture in 3 sentences."
    print(f"\nPrompt: {prompt}")
    print("\nGenerating response...")
    
    start_gen = time.time()
    response = pipe.generate(prompt, max_new_tokens=256)
    gen_time = time.time() - start_gen
    
    print("\n" + "-" * 60)
    print("Response:")
    print("-" * 60)
    print(response)
    print("-" * 60)
    
    # Calculate stats
    word_count = len(response.split())
    tokens_per_sec = word_count / gen_time
    
    print(f"\nPerformance:")
    print(f"  Generation time: {gen_time:.2f}s")
    print(f"  Words generated: {word_count}")
    print(f"  Speed: ~{tokens_per_sec:.1f} words/s")
    print("\n✓ OpenVINO GenAI is working on Intel Arc GPU!")
    print("=" * 60)

if __name__ == "__main__":
    main()
