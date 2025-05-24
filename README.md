# AI Outreach Agent 💌

A tool to generate personalized cold emails using LLMs and real-time Google-based summaries.

## 🔍 Features
- Upload a CSV with names, emails, LinkedIn
- Auto-generate summaries (or use custom)
- Choose tone and strictness
- Preview and edit emails manually
- Runs in **demo mode** — no real emails sent

## 🚀 Live Demo
Try it here (Streamlit Cloud): [YOUR_DEPLOYMENT_URL]

## 🧠 Stack
- Streamlit
- Python (requests, dotenv)
- OpenRouter (LLM backend)
- Serper.dev (real-time summary)

## 🛠️ Run Locally

```bash
pip install -r requirements.txt
cp .env.example .env
streamlit run main_public_demo.py
```

## 📄 Environment (.env) Required Keys

```
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
OPENROUTER_API_KEY=your_openrouter_key
SERPER_API_KEY=your_serper_key
```

**These are not used in demo mode.**
