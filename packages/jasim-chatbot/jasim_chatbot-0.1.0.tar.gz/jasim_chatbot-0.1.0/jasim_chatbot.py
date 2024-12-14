from transformers import pipeline

# Load the Hugging Face chatbot model (GPT-2 or any other suitable model)
chatbot = pipeline("text-generation", model="gpt2")

# Chatbot logic function
def main():
    print("Welcome to the jasim chatbot!")
    print("Ask me anything or type 'exit' to end.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        # Generate response using Hugging Face model
        response = chatbot(user_input, max_length=50, num_return_sequences=1)
        print(f"Chatbot: {response[0]['generated_text']}")

# Entry point for the script
if __name__ == "__main__":
    main()
