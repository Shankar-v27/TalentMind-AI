# TalentMind-AI 🌉

> AI-powered candidate ranking system that understands who fits a role — Not just who matches keywords.

![Python 3.11](https://img.shields.io/badge/python-3.11-blue)

---

## 📌 Overview

Recruiters go through hundreds of profiles and still often miss the right person. Not because the talent isn't there — but because keyword filters can't see what actually matters.

**TalentMind-AI** ranks candidates the way a great recruiter would — by actually understanding who fits the role, using semantic understanding, multi-dimensional scoring, and behavioral signals.

Built for the **India Runs Data & AI Challenge** by Redrob.

---

## 📉 Architecture

```
Job Description           Candidate Pool (100K)
        \                         /
     [Stage 1] Deep Semantic Understanding
      JD Parser | Candidate Encoder | Signal Extractor
                        |
    [Stage 2] Multi-Dimensional Scoring
     Skills | Career Arc | Experience | Education
     Intent | Reliability | Activity | Logistics
                        |
    [Stage 3] Weighted Fusion Engine
                        |
    [Stage 4] LLM Reasoning Layer (Groq / Claude)
                        |
              submission.csv + React Dashboard
```

---

## 📙 Stages

| Stage | Name | Description |
|---|---|---|
| 1 | Deep Understanding | Semantic JD parsing + candidate embeddings via `sentence-transformers` + FAISS ANN |
| 2 | Multi-Dim Scoring | 8 dimensions: Skills, Career Arc, Experience, Education, Intent, Reliability, Activity, Logistics |
| 3 | Weighted Fusion Engine | Custom scoring logic with reliability and trust multipliers for anti-honeypot checks |
| 4 | LLM Reasoning Layer | Natural language explanations (reasoning) generated via Groq/Claude for final candidates |
| 5 | Output Generation | Outputs final candidate ranks, scores, and explanation parameters to `submission.csv` |

---

## 🚀 Setup & Execution

### Prerequisites
- Python 3.11+
- Node.js (for frontend)

### Installation
1. Clone the repository and navigate to the folder:
   ```bash
   cd TalentMind-AI
   ```
2. Install Python dependencies:
   ```bash
   pip install -r Requirements.txt
   ```
3. Set your environment variables in a `.env` file:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Running the Backend
To start the FastAPI server:
```bash
python api_server.py
```
By default, the server runs on `http://127.0.0.1:8001`.

### Running the Frontend
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install Node packages:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

### Pre-building Candidate Embeddings Cache
To generate candidate embeddings and FAISS index cache before running the app:
```bash
python build_cache.py
```