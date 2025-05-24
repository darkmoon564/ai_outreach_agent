import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def build_prompt_style_5(name, summary, tone):
    return f"""You're writing a short, honest outreach email to {name}.

Their background:
{summary}

Write in a {tone} tone.

DO:
- Start with a soft compliment or mention of their work
- Sound natural — like a human, not a sales bot
- Be clear there's no agenda or product being pitched
- Ask one light, conversational question if it fits
- Keep it under 5 sentences

DO NOT:
- Use buzzwords (e.g. "game-changing", "pushing boundaries", "explore opportunities")
- Pretend you've read their papers
- Fabricate job titles, projects, or research papers
- Assume they're a senior researcher unless said
- Mention fake papers or teams like "IBM AI Lab"

End with a calm sign-off as Ashit Vijay.
Start with a real subject line.
""" 

def build_random_prompt(name, summary, tone):
    return build_prompt_style_5(name, summary, tone)  # Force most realistic only

def write_email_llm_openrouter(name, summary, tone="Friendly", strict=True):
    prompt = build_random_prompt(name, summary, tone)

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-3.3-8b-instruct:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)

    if response.status_code == 200:
        email_text = response.json()["choices"][0]["message"]["content"]
        email_text = email_text.strip()

        
        if email_text.lower().startswith("here is") or "here's a cold email" in email_text.lower():
            email_text = "\n".join(email_text.split("\n")[1:]).strip()

        
        if strict:
            ban_phrases = [
                "i read your paper", "i came across your research",
                "as a senior researcher", "your team at ibm",
                "your work on ibm’s ai research team",
                "hybrid architectures for large-scale ai"
            ]
            for phrase in ban_phrases:
                if phrase.lower() in email_text.lower():
                    return "ERROR: Hallucination detected. Try again or adjust the prompt."

        if "[Your Name]" in email_text:
            email_text = email_text.replace("[Your Name]", "Ashit Vijay")

        return email_text
    else:
        return f"Error: {response.status_code} | {response.text}"
