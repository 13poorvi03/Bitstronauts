import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from youtube_transcript_api import YouTubeTranscriptApi
import re

def setup_model():
    """Dynamically finds the best available Gemini model to prevent 404 errors"""
    try:
        # Teri Real API Key (Integrated)
        api_key = "AIzaSyB5__D4UBdDYxPwNlZE_7CGg0AG2dAa7Bc"
        genai.configure(api_key=api_key)
        
        # Available models ki list nikalna jo generateContent support karte hain
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Priority: 1.5 Flash -> 1.5 Pro -> Legacy Pro
        target_models = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
        
        for target in target_models:
            if target in available_models:
                return genai.GenerativeModel(target)
        
        if available_models:
            return genai.GenerativeModel(available_models[0])
        return None
    except Exception as e:
        st.error(f"AI Setup Error: {e}")
        return None

def get_yt_transcript(url):
    """YouTube video se text nikalne ke liye"""
    try:
        # URL se Video ID nikalne ka foolproof tareeka
        video_id_match = re.search(r"(?:v=|\/|be\/)([0-9A-Za-z_-]{11})", url)
        if not video_id_match:
            return "Error: Invalid YouTube URL."
        
        video_id = video_id_match.group(1)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t['text'] for t in transcript])
    except Exception as e:
        return "Error: Transcript available nahi hai. Shayad video mein subtitles disabled hain."

def get_alchemist_explanation(model, data):
    """Main AI Transformation Logic"""
    prompt = f"""
    You are a Media Alchemist. 
    1. Explain this topic in 8-10 simple sentences using a real-world metaphor.
    2. Then, list 3 'Aha!' facts (surprising facts).
    3. Finally, give a 4-line acronym for easy memory.
    
    CONTENT: {data[:4000]}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: Explanation generate nahi ho payi. ({e})"

def get_yt_suggestions(model, topic):
    """Resource Radar ke liye keywords generate karna"""
    prompt = f"Give 5 high-quality YouTube search phrases for learning about: {topic[:100]}. Give just the phrases, one per line."
    try:
        res = model.generate_content(prompt).text.strip().split("\n")
        # Har phrase ke liye clickable link banana
        links = "".join([f"<li><a href='https://www.youtube.com/results?search_query={p.strip().replace(' ','+')}' target='_blank' style='color:#6C5CE7; font-weight:bold;'>▶️ {p.strip()}</a></li>" for p in res[:5]])
        return f"<ul>{links}</ul>"
    except:
        return "Radar Offline: Resource links nahi mil paye."

def solve_doubt(model, doubt, context):
    """Sidebar Chatbot ke liye logic"""
    prompt = f"Context: {context[:2000]}\nDoubt: {doubt}\nAnswer strictly in 3 simple sentences."
    try:
        return model.generate_content(prompt).text
    except:
        return "Sage is thinking deeply... please try again."

def extract_pdf(file):
    """PDF file se text nikalne ke liye"""
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text
    except Exception as e:
        return f"Error: PDF read nahi ho payi. ({e})"