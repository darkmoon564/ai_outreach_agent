import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from agents.email_writer import write_email_llm_openrouter
from agents.sender import EmailSender
from agents.researcher import research_person

load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

st.set_page_config(page_title="AI Outreach Agent 💌")
st.title("AI Outreach Agent (Demo Mode)")
st.markdown("Upload a CSV and your resume to generate personalized cold emails. This demo runs in preview mode — no real API usage.")

tone = st.selectbox("🎨 Choose email tone", ["Friendly", "Professional", "Casual", "Funny"])
strict_mode = st.checkbox("🔒 Strict anti-hallucination mode", value=True)
preview_mode = True  # 🔒 LOCKED PREVIEW MODE
auto_research = st.checkbox("🌐 Auto-research summary using Serper (ignore Summary column)", value=True)

uploaded_file = st.file_uploader("📤 Upload CSV (Name, LinkedIn, Email)", type=["csv"])
resume_file = st.file_uploader("📎 Upload Resume (PDF)", type=["pdf"])

def generate_preview_email(name, summary, tone):
    return f"""Subject: Quick note from Ashit

Hi {name},

Really appreciated your background in: {summary[:80]}...
Just thought it would be cool to connect — always great meeting folks exploring similar paths.

Cheers,  
Ashit Vijay
""" 

if uploaded_file and resume_file:
    df = pd.read_csv(uploaded_file)
    required_cols = {"Name", "LinkedIn", "Email"}
    st.subheader("📧 Preview & Edit Emails (No Sending)")
    results = []

    if required_cols.issubset(df.columns):
        st.success("✅ CSV looks good!")
        st.dataframe(df.head())

        resume_bytes = resume_file.read()
        resume_name = resume_file.name

        for idx, row in df.iterrows():
            name = row["Name"]
            email = row["Email"]
            summary = research_person(name) if auto_research else row.get("Summary", "")

            with st.expander(f"✉️ {name} ({email})", expanded=True):
                email_text = generate_preview_email(name, summary, tone)

                # Editable text
                email_input = st.text_area("Generated Email", value=email_text, height=250, key=f"email_{idx}")
                st.caption("📌 This is a demo — emails are not being sent.")
    else:
        st.error("❌ CSV must include: Name, LinkedIn, Email")
