# Custom AI Chatbot with Memory

Project 1 — DecodeLabs Generative AI Internship (Batch 2026)

A terminal-based chatbot that remembers earlier messages in a conversation, instead of treating every message as a fresh, unrelated question. It also saves the conversation to disk, so it survives closing and reopening the program.

## Features

- Connects to a local LLM (Ollama) — no API key, no billing, no rate limits
- In-memory conversation history using structured role/content objects
- Every user message and model reply is appended to the session history
- Input validation — empty/blank messages are rejected before reaching the model
- Sliding window (FIFO) — trims old messages once the conversation gets long, so the model's token limit is never exceeded
- Local JSON persistence — conversation is saved after every turn and reloaded automatically on the next run

## Demo

**Chatbot running and holding a conversation:**

![Chatbot running](running_chatbot_screenshot.PNG)

**Before exiting — conversation in progress:**

![Before exit](before_exit.PNG)

**After restarting — the bot still remembers the name from before:**

![Memory persists after restart](after_exit_chatbot_know_my_name.PNG)

## Setup

### 1. Install Ollama (runs the AI model locally, 100% free)
Download: https://ollama.com/download
Run the installer and restart your computer afterward.

### 2. Download a small AI model
```
ollama pull llama3.2:1b
```

### 3. Install the Python dependency
```
pip install -r requirements.txt
```

### 4. Run the chatbot
```
python chatbot_with_memory.py
```

Type your message after `Ask anything:`. Type `exit` to stop.

### Try the memory test
1. `my name is Rehan`
2. Ask any unrelated question
3. `what is my name?` — the bot should answer correctly

## Project Structure

```
├── chatbot_with_memory.py   # Main chatbot script
├── requirements.txt         # Python dependencies
├── Project1_Report.docx     # Full project report
└── README.md
```

## How the Code Maps to the Task Requirements

| Requirement | Implementation |
|---|---|
| In-memory history array | `conversation_history = []` |
| Role/Content schema | `{"role": "user", "content": ...}` |
| Append every message | user message appended → model called → reply appended |
| Reject empty input | `is_valid_input()` |
| Prevent token overflow | `apply_sliding_window()` (FIFO) |
| Persistence (bonus) | `save_history()` / `load_history()` — local JSON file |

## Built With

- Python 3
- [Ollama](https://ollama.com/) (llama3.2:1b, running locally)

---
Part of the DecodeLabs Generative AI Internship — Batch 2026.
