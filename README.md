# 🎬 AI Video Assistant
 
An intelligent meeting analysis tool that transcribes audio/video recordings, generates summaries, extracts action items and decisions, and lets you chat with your meeting transcript using RAG.
 
---
 
## ✨ Features
 
- **Transcription** — Converts audio/video to text using OpenAI Whisper (English) or Sarvam AI (Hinglish)
- **Summarisation** — Generates a concise bullet-point summary of the meeting
- **Action Item Extraction** — Pulls out tasks, owners, and deadlines
- **Key Decision Extraction** — Lists all decisions made in the meeting
- **Open Questions** — Identifies unresolved topics needing follow-up
- **RAG Chat** — Ask anything about your meeting and get cited answers powered by a vector store
---
 
## 🗂️ Project Structure
 
```
ai-video-assistant/
├── app.py                  # Streamlit UI
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── packages.txt            # System dependencies (ffmpeg)
├── runtime.txt             # Python version pin
├── core/
│   ├── transcriber.py      # Whisper + Sarvam AI transcription
│   ├── summarizer.py       # Map-reduce summarisation
│   ├── extractor.py        # Action items, decisions, questions
│   ├── rag_engine.py       # RAG chain with Mistral
│   └── vector_store.py     # Chroma vector store + HuggingFace embeddings
└── utils/
    └── audio_processor.py  # Audio download, conversion, chunking
```

## 🧠 How It Works
 
```
Upload Audio/Video
       ↓
Audio Processing (pydub → WAV → chunks)
       ↓
Transcription (Whisper / Sarvam AI)
       ↓
  ┌────┴────────────────────────┐
  ↓                             ↓
LLM Analysis (Mistral)     Vector Store (Chroma)
  - Title                   - HuggingFace Embeddings
  - Summary                 - Similarity Search
  - Action Items                 ↓
  - Decisions              RAG Chat (Mistral)
  - Questions
```
 
---
 
## 🛠️ Tech Stack
 
| Layer | Technology |
|---|---|
| UI | Streamlit |
| Transcription | OpenAI Whisper, Sarvam AI |
| LLM | Mistral (via LangChain) |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Vector Store | Chroma |
| Audio Processing | pydub, ffmpeg |
| Orchestration | LangChain LCEL |
 
---

## ☁️ Deploying to Streamlit Cloud
[Live Demo] : https://ai-video-assistant-7lpwqtueqlujwlbeyzf5s5.streamlit.app/
