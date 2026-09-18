import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please set it in the .env file.")

genai.configure(api_key=api_key)

# Model selection (stable and free-tier friendly)
model = genai.GenerativeModel("gemini-3.6-flash")

# Maximum number of messages to keep in memory (sliding window)
# Each turn = 1 user + 1 model message → keeping last 10 turns = 20 messages
MAX_HISTORY = 20


def get_user_input():
    """Get and validate user input. Returns None if user wants to exit."""
    try:
        user_input = input("\nYou: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting chatbot. Goodbye!")
        return None

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("\nChatbot: Goodbye! Have a great day.")
        return None

    if not user_input:
        print("Chatbot: Please type something. Empty messages are not allowed.")
        return ""

    return user_input


def trim_history(history):
    """
    Sliding window (FIFO): Keep only the most recent messages
    so we don't exceed the model's context limit.
    """
    if len(history) > MAX_HISTORY:
        # Remove oldest messages (from the beginning)
        history = history[-MAX_HISTORY:]
    return history


def main():
    print("=" * 60)
    print("  Custom AI Chatbot with Memory")
    print("  Project 1 | DecodeLabs Industrial Training")
    print("=" * 60)
    print("Type 'exit', 'quit' or 'bye' to end the conversation.\n")

    # This list is our "memory" — stores the full conversation
    chat_history = []

    while True:
        user_message = get_user_input()

        if user_message is None:
            break

        if user_message == "":
            continue

        # 1. Append user message to history
        chat_history.append({
            "role": "user",
            "parts": [user_message]
        })

        # 2. Apply sliding window
        chat_history = trim_history(chat_history)

        try:
            # 3. Send the entire history to Gemini
            response = model.generate_content(chat_history)

            model_reply = response.text

            # 4. Append model response to history
            chat_history.append({
                "role": "model",
                "parts": [model_reply]
            })

            print(f"\nChatbot: {model_reply}")

        except Exception as e:
            print(f"\nError: Something went wrong → {e}")
            # Remove the last user message if API failed
            if chat_history and chat_history[-1]["role"] == "user":
                chat_history.pop()


if __name__ == "__main__":
    main()
