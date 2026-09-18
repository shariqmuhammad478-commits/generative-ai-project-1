# Generative AI Project 1 – Custom AI Chatbot with Memory

**Industrial Training Kit | Batch 2026 | DecodeLabs**

## Project Overview

This project implements a **stateful conversational chatbot** using Google Gemini.  
Unlike a basic one-shot API call, this chatbot maintains an active in-memory conversation history so that the model remembers previous messages within a session.

## Key Features

- In-memory conversation history (list of role-content objects)
- Automatic appending of every user and model message
- Input validation (blocks empty messages)
- Sliding Window (FIFO) to prevent token limit overflow
- Clean terminal interface
- Secure API key handling using `.env`

## How Memory Works

1. User message is validated and appended to history
2. Full history is sent to Gemini on every turn
3. Model response is appended back to the same history
4. When history grows too long, oldest messages are removed (sliding window)

## Tech Stack

- Python 3.10+
- `google-generativeai` (official Gemini SDK)
- `python-dotenv`

## Setup Instructions

1. Clone the repository
2. Create a virtual environment (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_key_here
   ```
5. Run the chatbot
   ```bash
   python main.py
   ```

## Memory Test (System Audit)

To verify that memory is working correctly:

1. Say: `My name is Vipin`
2. Ask it to write a long poem
3. Ask: `What is my name?`

The chatbot should correctly reply with **Vipin**.

## Project Structure

```
generative-ai-project-1/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Learnings

- Difference between stateless and stateful LLM calls
- Managing conversation history manually
- Handling context window limits with sliding window
- Input validation before sending requests to the API
