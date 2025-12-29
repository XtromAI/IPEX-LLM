"""
Interactive chat using OpenVINO GenAI on Intel Arc GPU
Usage: conda activate openvino-genai && python chat_openvino.py
"""
import openvino_genai as ov_genai
import sys

def main():
    model_path = "TinyLlama-1.1B-ov"
    
    print("=" * 60)
    print("OpenVINO GenAI Chat")
    print("=" * 60)
    print(f"Model: {model_path}")
    print(f"Device: Intel Arc 140V GPU")
    print("Commands: 'exit' or 'quit' to end, 'clear' to start new conversation")
    print("=" * 60)
    
    # Initialize pipeline
    print("\nLoading model...")
    pipe = ov_genai.LLMPipeline(model_path, "GPU")
    print("Model loaded! Ready to chat.\n")
    
    # Chat loop
    conversation_history = []
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['exit', 'quit']:
                print("\nGoodbye!")
                break
            
            if user_input.lower() == 'clear':
                conversation_history = []
                print("\n[Conversation cleared]")
                continue
            
            # Build prompt with conversation history
            if conversation_history:
                prompt = "\n".join(conversation_history)
                prompt += f"\nUser: {user_input}\nAssistant:"
            else:
                prompt = f"User: {user_input}\nAssistant:"
            
            # Generate response
            response = pipe.generate(prompt, max_new_tokens=512)
            
            # Clean up response (remove the prompt echo if present)
            if "Assistant:" in response:
                response = response.split("Assistant:")[-1].strip()
            
            # Stop at next "User:" if model continues the conversation
            if "User:" in response:
                response = response.split("User:")[0].strip()
            
            print(f"\nAssistant: {response}")
            
            # Update conversation history
            conversation_history.append(f"User: {user_input}")
            conversation_history.append(f"Assistant: {response}")
            
            # Keep only last 6 exchanges (12 entries) to avoid context overflow
            if len(conversation_history) > 12:
                conversation_history = conversation_history[-12:]
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Continuing chat...")

if __name__ == "__main__":
    main()
