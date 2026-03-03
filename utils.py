import os
from dotenv import load_dotenv

load_dotenv()  # 🔥 This loads .env file

API_KEY = os.getenv("GOOGLE_API_KEY")


from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from youtube_transcript_api import YouTubeTranscriptApi
import re

# ==============================
# 🔐 LOAD ENVIRONMENT VARIABLES
# ==============================

load_dotenv()

# Local (.env) + Streamlit Cloud support (safe version)
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        api_key = None


# ==============================
# 🤖 MODEL SETUP
# ==============================

def setup_model():
    """Initialize Gemini model safely"""

    if not api_key:
        st.error("❌ API key not found. Add it in .env (local) or Streamlit Secrets (cloud).")
        return None

    try:
        genai.configure(api_key=api_key)

        models = genai.list_models()
        available_models = [
            m.name for m in models
            if "generateContent" in m.supported_generation_methods
        ]

        preferred_models = [
            "models/gemini-1.5-flash",
            "models/gemini-1.5-pro",
            "models/gemini-pro",
        ]

        for model_name in preferred_models:
            if model_name in available_models:
                return genai.GenerativeModel(model_name)

        if available_models:
            return genai.GenerativeModel(available_models[0])

        st.error("❌ No compatible Gemini model found.")
        return None

    except Exception as e:
        st.error(f"🚨 AI Setup Error: {e}")
        return None


# ==============================
# 🎥 YOUTUBE TRANSCRIPT
# ==============================

def get_yt_transcript(url):
    """Extract transcript from YouTube"""

    try:
        video_id_match = re.search(r"(?:v=|\/|be\/)([0-9A-Za-z_-]{11})", url)

        if not video_id_match:
            return "❌ Invalid YouTube URL."

        video_id = video_id_match.group(1)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        return " ".join([t["text"] for t in transcript])

    except Exception:
        return "⚠ Transcript not available. Subtitles may be disabled."


# ==============================
# 🧠 MAIN AI EXPLANATION
# ==============================

def get_alchemist_explanation(model, data):
    """Main AI transformation logic"""

    if not model:
        return "⚠ AI model not initialized."

    prompt = f"""
    You are a Media Alchemist.

    1. Explain this topic in 8-10 simple sentences using a powerful real-world metaphor.
    2. Then list 3 surprising 'Aha!' insights.
    3. Create a 4-line acronym for memory retention.

    CONTENT:
    {data[:4000]}
    """

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"❌ AI Error: Could not generate explanation. ({e})"


# ==============================
# 🔎 YOUTUBE LEARNING RADAR
# ==============================

def get_yt_suggestions(model, topic):
    """Generate YouTube search phrases"""

    if not model:
        return "⚠ AI model not initialized."

    prompt = f"""
    Give 5 high-quality YouTube search phrases 
    for learning about: {topic[:100]}.
    One per line.
    """

    try:
        result = model.generate_content(prompt)
        phrases = result.text.strip().split("\n")

        links = "".join([
            f"<li><a href='https://www.youtube.com/results?search_query={p.strip().replace(' ','+')}' target='_blank'>▶️ {p.strip()}</a></li>"
            for p in phrases[:5]
            if p.strip()
        ])

        return f"<ul>{links}</ul>"

    except Exception:
        return "⚠ Radar offline. Could not generate resource links."


# ==============================
# 💬 SIDEBAR DOUBT SOLVER
# ==============================

def solve_doubt(model, doubt, context):
    """Sidebar chatbot logic"""

    if not model:
        return "⚠ AI model not initialized."

    prompt = f"""
    Context:
    {context[:2000]}

    Doubt:
    {doubt}

    Answer strictly in 3 simple sentences.
    """

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception:
        return "🤔 Sage is thinking deeply... Please try again."


# ==============================
# 📄 PDF TEXT EXTRACTION
# ==============================

def extract_pdf(file):
    """Extract text from PDF"""

    try:
        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content

        if not text.strip():
            return "⚠ No readable text found in PDF."

        return text

    except Exception as e:
        return f"❌ PDF Error: Could not read file. ({e})"