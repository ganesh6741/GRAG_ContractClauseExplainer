import requests
import os

# Optional: If used within Streamlit
try:
    import streamlit as st
except ImportError:
    st = None  # Handles non-Streamlit environments

# 🔐 Secure API Key Handling
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
if not PERPLEXITY_API_KEY and st:
    PERPLEXITY_API_KEY = st.secrets.get("PERPLEXITY_API_KEY", "")

PERPLEXITY_ENDPOINT = "https://api.perplexity.ai/chat/completions"

# 💬 Query LLM Endpoint
def query_llm(prompt):
    if not PERPLEXITY_API_KEY:
        error_msg = "🚫 No API key found. Please set PERPLEXITY_API_KEY in environment or Streamlit secrets."
        if st:
            st.error(error_msg)
        else:
            print(error_msg)
        return "⚠️ Missing API credentials"

    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sonar-pro",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(PERPLEXITY_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        error_msg = f"❌ API Error: {e}"
        if st:
            st.warning(error_msg)
        else:
            print(error_msg)
        return "⚠️ LLM response error"

# ✍️ Simplify Clause
def rewrite_clause(clause_text):
    prompt = f"Simplify the following legal clause in plain English:\n\"{clause_text}\""
    return query_llm(prompt)

# 🤝 Suggest Negotiation Tip
def generate_negotiation_tip(clause_text):
    prompt = f"What should someone consider negotiating in the following legal clause?\n\"{clause_text}\""
    return query_llm(prompt)