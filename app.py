import streamlit as st
import requests
from bs4 import BeautifulSoup

def extract_text(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        paragraphs = soup.find_all('p')
        return " ".join([p.get_text() for p in paragraphs])
    except:
        return ""

def rewrite_article(content):
    api_key = st.secrets["GROQ_API_KEY"]

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a professional news editor.

Rewrite the article into a completely original news piece.

Rules:
- Do NOT paraphrase line-by-line
- Completely restructure
- Keep facts accurate
- Add headline
- Add SEO Title
- Add Meta Description
- Add keywords
- Use subheadings
- Make it plagiarism free

Article:
{content}
"""

    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)
   def rewrite_article(content):
    api_key = st.secrets.get("GROQ_API_KEY")

    if not api_key:
        return "❌ API Key missing. Check Streamlit Secrets."

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a professional news editor.

Rewrite the article into a completely original news piece.

Rules:
- Do NOT paraphrase line-by-line
- Completely restructure
- Keep facts accurate
- Add headline
- Add SEO Title
- Add Meta Description
- Add keywords
- Use subheadings
- Make it plagiarism free

Article:
{content}
"""

    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        res_json = response.json()

        if "choices" in res_json:
            return res_json['choices'][0]['message']['content']
        else:
            return f"❌ API Error: {res_json}"

    except Exception as e:
        return f"❌ Unexpected Error: {str(e)}"

st.title("AI Article Rewriter")

url_input = st.text_input("Enter URL")
manual_text = st.text_area("Or paste content")

if st.button("Rewrite"):
    content = extract_text(url_input) if url_input else manual_text

    if not content:
        st.warning("Provide input")
    else:
        with st.spinner("Rewriting..."):
            result = rewrite_article(content)
            st.write(result)
