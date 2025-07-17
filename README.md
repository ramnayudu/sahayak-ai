# Sahayak AI 🧠📚

**An AI-powered co-teacher for rural multi-grade classrooms**  
Built for Google Cloud Agentic AI Day 2025 – Finalist Sprint 🏁

---

## 🌐 Project Overview

**Project Sahayak** is an agentic AI assistant that helps teachers in low-resource, multi-grade classrooms generate:
- Lesson plans
- Visual aids
- Age-appropriate stories
- Differentiated worksheets

With two deployment modes:

- 🔹 **Sahayak Setu (Online)** — Powered by Gemini + Gemma via Vertex AI  
- 🔸 **Sahayak Nivaas (Offline)** — Runs locally using quantized Gemma via Ollama

---

## 🧠 Tech Stack

| Layer          | Tech Used                            |
|----------------|--------------------------------------|
| Frontend       | React PWA, Firebase Hosting          |
| Backend        | Python, FastAPI, Google ADK          |
| AI Models      | Gemini Pro, Gemma 13B/7B (fine-tuned)|
| Offline Engine | Ollama / llama.cpp + Quantized LoRA  |
| Database       | Firebase Firestore / SQLite (offline)|
| Auth           | Firebase Authentication              |

---

## 🚀 Local Setup

1. Clone the repo  
   `git clone https://github.com/your-org/sahayak-ai.git`

2. Install frontend  
3. Run backend 
4. (Optional) Run Ollama 
