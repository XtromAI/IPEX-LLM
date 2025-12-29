"""
Test client for OpenVINO GenAI REST API Server
Demonstrates how to interact with the server from other applications
"""
import requests
import json

SERVER_URL = "http://127.0.0.1:8000"

def test_health():
    """Test server health check"""
    print("\n" + "="*60)
    print("1. Health Check")
    print("="*60)
    
    response = requests.get(f"{SERVER_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_list_models():
    """Test list models endpoint"""
    print("\n" + "="*60)
    print("2. List Available Models")
    print("="*60)
    
    response = requests.get(f"{SERVER_URL}/api/tags")
    print(f"Status: {response.status_code}")
    models = response.json()
    for model in models["models"]:
        print(f"  - {model['name']} ({model['details']['quantization_level']})")

def test_generate():
    """Test text generation endpoint"""
    print("\n" + "="*60)
    print("3. Generate Text (Non-streaming)")
    print("="*60)
    
    prompt = "Explain what unified memory architecture means in one sentence."
    print(f"Prompt: {prompt}\n")
    
    data = {
        "model": "TinyLlama-1.1B-ov",
        "prompt": prompt,
        "stream": False,
        "max_new_tokens": 128
    }
    
    response = requests.post(f"{SERVER_URL}/api/generate", json=data)
    print(f"Status: {response.status_code}")
    
    result = response.json()
    print(f"\nResponse: {result['response']}")
    print(f"\nStats:")
    print(f"  - Generation time: {result['total_duration'] / 1e9:.2f}s")
    print(f"  - Words generated: {result['eval_count']}")

def test_chat():
    """Test chat endpoint"""
    print("\n" + "="*60)
    print("4. Chat Completion")
    print("="*60)
    
    data = {
        "model": "TinyLlama-1.1B-ov",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What are the benefits of Intel Arc GPUs?"}
        ],
        "stream": False,
        "max_new_tokens": 256
    }
    
    print("Messages:")
    for msg in data["messages"]:
        print(f"  {msg['role']}: {msg['content']}")
    
    response = requests.post(f"{SERVER_URL}/api/chat", json=data)
    print(f"\nStatus: {response.status_code}")
    
    result = response.json()
    print(f"\nAssistant: {result['message']['content']}")
    print(f"\nGeneration time: {result['total_duration'] / 1e9:.2f}s")

def test_powershell_example():
    """Show PowerShell usage example"""
    print("\n" + "="*60)
    print("5. PowerShell Usage Example")
    print("="*60)
    
    powershell_code = '''
# PowerShell example - test from another terminal
$body = @{
    model = "TinyLlama-1.1B-ov"
    prompt = "What is artificial intelligence?"
    stream = $false
    max_new_tokens = 256
} | ConvertTo-Json

$response = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/generate" -Body $body -ContentType "application/json"

Write-Host "Response: $($response.response)"
'''
    
    print(powershell_code)

def main():
    print("\n" + "="*60)
    print("OpenVINO GenAI REST API Client Test")
    print("="*60)
    print("\nMake sure the server is running in another terminal:")
    print("  conda activate openvino-genai")
    print("  python serve_openvino.py\n")
    
    input("Press Enter to start tests...")
    
    try:
        test_health()
        test_list_models()
        test_generate()
        test_chat()
        test_powershell_example()
        
        print("\n" + "="*60)
        print("✓ All tests completed successfully!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server!")
        print("Make sure serve_openvino.py is running in another terminal.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
