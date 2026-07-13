"""
============================================================
  PROJECT 1: Custom AI Chatbot with Memory
  DecodeLabs - Generative AI Internship (Batch 2026)
  (Using Ollama - runs LOCALLY on your PC, 100% FREE,
   no API key, no billing, no quota limits, no region issues)
============================================================

This script follows every requirement given in the PDF:

1. Connect to a frontier LLM (Ollama local model via official SDK)
2. Keep an in-memory list/array that stores conversation history
3. Append every user message and model response to that history
4. Structural Validation Gate: block empty/whitespace messages
5. Sliding Window Algorithm (FIFO): trim old history so the
   token limit does not overflow (PDF Slide 11)
6. Persistence: save the conversation to a local file so it is
   not lost when the program closes (PDF Slide 14 warns that
   local RAM-only memory is "fatally flawed" once the program
   restarts - a real database like Firestore/PostgreSQL is the
   enterprise solution, but a local JSON file gives us the same
   basic idea for free, with no extra setup)
============================================================
"""

import ollama
import json
import os

# ------------------------------------------------------------------
# STEP 0: MODEL SETUP
# (PDF Slide: "Key Requirements - Connect to a frontier LLM using
#  an official SDK API key")
# With Ollama we don't need an API key, because the model runs
# locally on your own computer. We just need the model's name.
# ------------------------------------------------------------------
MODEL_NAME = "llama3.2:1b"   # Small, fast, low-resource model

# ------------------------------------------------------------------
# STEP 1: IN-MEMORY HISTORY ARRAY
# (PDF Slide: "Maintain an active in-memory list array to store
#  the conversation history")
# ------------------------------------------------------------------
# Each entry looks like: {"role": "user" or "assistant", "content": "text"}
# (PDF Slide 7 "Anatomy of a Chat Session Schema")
conversation_history = []

# ------------------------------------------------------------------
# STEP 1b: PERSISTENCE (SAVE / LOAD TO A LOCAL FILE)
# (PDF Slide 14: "The Ephemeral Nature of Local RAM" - RAM-only
#  memory is lost if the program restarts. Real products save
#  conversations to a database. Here we use a simple JSON file
#  on your own computer, which is the free/local equivalent.)
# ------------------------------------------------------------------
HISTORY_FILE = "conversation_history.json"


def load_history():
    """Load past conversation from disk, if it exists."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_history(history):
    """Save the current conversation to disk so it survives a restart."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


# ------------------------------------------------------------------
# STEP 2: SLIDING WINDOW CONFIG
# (PDF Slide: "The Sliding Window Algorithm" - FIFO pruning)
# ------------------------------------------------------------------
MAX_HISTORY_MESSAGES = 20


def apply_sliding_window(history):
    """
    PDF Slide 11: remove the oldest messages (FIFO = First In,
    First Out) once history grows too large, so we don't hit
    the model's token limit.
    """
    if len(history) > MAX_HISTORY_MESSAGES:
        overflow = len(history) - MAX_HISTORY_MESSAGES
        del history[0:overflow]
    return history


def is_valid_input(user_text):
    """
    PDF Slide 8: 'The Structural Validation Gate'
    Don't let an empty string or whitespace-only message reach
    the API - it would cause a crash/error.
    """
    return bool(user_text and user_text.strip())


def get_model_response(history):
    """
    STEP 3: TRANSMIT & RECORD
    (PDF Slide 9: the entire history is sent as the payload,
    not just the newest message)
    This calls the local Ollama server - completely free, no
    internet or billing needed after the model is downloaded.
    """
    response = ollama.chat(model=MODEL_NAME, messages=history)
    return response["message"]["content"]


def run_chatbot():
    global conversation_history

    # Load any saved conversation from a previous run
    conversation_history = load_history()

    print("=" * 60)
    print(" Custom AI Chatbot with Memory  (DecodeLabs Project 1)")
    print(" Type your message to chat with the bot.")
    print(" Type 'exit' or 'quit' to stop.")
    print("=" * 60)

    if conversation_history:
        print(f"\n(Loaded {len(conversation_history)} earlier messages from {HISTORY_FILE})")

    while True:
        user_input = input("\nAsk anything: ")

        if user_input.strip().lower() in ("exit", "quit"):
            print("Bot: Goodbye! Your conversation has been saved.")
            break

        # STEP: Validation Gate
        if not is_valid_input(user_input):
            print("Bot: That message is empty - please type something.")
            continue

        # STEP: Ingest & Append the user's message
        conversation_history.append({"role": "user", "content": user_input})

        # STEP: Apply the sliding window
        apply_sliding_window(conversation_history)

        try:
            reply = get_model_response(conversation_history)
        except Exception as e:
            print(f"Bot: An error happened: {e}")
            print("     (Make sure Ollama is running - try 'ollama serve')")
            conversation_history.pop()
            continue

        # STEP: Append the model's reply to history (this is the memory!)
        conversation_history.append({"role": "assistant", "content": reply})

        # STEP: Persist to disk after every turn
        save_history(conversation_history)

        print(f"Bot: {reply}")


if __name__ == "__main__":
    run_chatbot()
