import streamlit as st
import requests
from bs4 import BeautifulSoup

# ---- Extract content from URL ----
def extract_text(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        paragraphs = soup.find_all('p')
        return " ".join([p.get_text() for p in paragraphs])
    except Exception as e:
        return ""

# ---- Rewrite using AI ----
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

Strict rules:
- Do NOT paraphrase line-by-line
- Completely restructure the article
- Keep facts accurate
- Use a journalistic tone
- Add a strong headline
- Add SEO Title (max 60 chars)
- Add Meta Description (150 chars)
- Add 3-5 SEO keywords
- Use subheadings
- Make it same length or longer than original
- Ensure it's plagiarism-free

Article:
{content}
"""

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        res_json = response.json()

        if "choices" in res_json:
            return res_json["choices"][0]["message"]["content"]
        else:
            return f"❌ API Error: {res_json}"

    except Exception as e:
        return f"❌ Request failed: {str(e)}"


# ---- Streamlit UI ----
st.title("📰 AI Article Rewriter")

url_input = st.text_input("Enter Article URL")
manual_text = st.text_area("Or Paste Article Content")

if st.button("Rewrite Article"):
    if url_input:
        content = extract_text(url_input)
    else:
        content = manual_text

    if not content.strip():
        st.warning("Please provide URL or content")
    else:
        with st.spinner("Rewriting..."):
            result = rewrite_article(content)
            st.success("Done!")
            st.write(result)
