import streamlit as st
from utils import *

# 1. Page Configuration
st.set_page_config(
    page_title="CurioCity | AI Alchemist",
    page_icon="🧪",
    layout="wide"
)

# 2. Load Visual Styles (CSS)
try:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception as e:
    st.warning("CSS file missing! UI standard dikhega.")

# 3. Initialize Gemini Model (From Utils)
model = setup_model()

# 4. Session State Management
if 'auth' not in st.session_state:
    st.session_state.update({
        'auth': False, 
        'username': "", 
        'step': "input", 
        'wisdom': "", 
        'yt': "", 
        'topic': "General Learning", 
        'history': []
    })

# --- UI FLOW ---

# PHASE 0: Login / Welcome Screen
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #4834d4;'>🏙️ CurioCity Prototype</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("<div class='logic-card'>", unsafe_allow_html=True)
        name = st.text_input("Enter your Alchemist Name:")
        if st.button("Unleash The Lab 🚀") and name:
            st.session_state.username = name
            st.session_state.auth = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# MAIN APP (After Login)
else:
    if not model:
        st.error("❌ AI Model Setup Failed! API key ya Internet check karein.")
        st.stop()

    # SIDEBAR: Sage Doubt Solver (Chatbot)
    st.sidebar.title(f"🧙‍♂️ {st.session_state.username}")
    st.sidebar.markdown(f"**Status:** Senior Alchemist")
    st.sidebar.markdown("---")
    
    st.sidebar.subheader("💬 Sage Doubt Solver")
    doubt_input = st.sidebar.text_input("Ask a quick doubt...")
    if st.sidebar.button("Ask Sage"):
        if doubt_input:
            with st.sidebar:
                with st.spinner("Sage is thinking..."):
                    ans = solve_doubt(model, doubt_input, st.session_state.topic)
                    st.session_state.history.append({"q": doubt_input, "a": ans})
    
    # Show last 2 chats in sidebar
    for chat in reversed(st.session_state.history[-2:]):
        st.sidebar.info(f"**Q:** {chat['q']}\n\n**A:** {chat['a']}")

    # PHASE 1: INPUT SCREEN
    if st.session_state.step == "input":
        st.header("🧪 Transmute Knowledge")
        st.write(f"Welcome back, {st.session_state.username}. Choose your source material:")
        
        source = st.selectbox("Select Learning Source", ["▶️ YouTube Link", "📄 PDF Document", "📜 Raw Text / Topic"])
        
        raw_data = ""
        if source == "▶️ YouTube Link":
            url = st.text_input("Paste YouTube URL here:")
            if url: 
                with st.spinner("Fetching transcript..."):
                    raw_data = get_yt_transcript(url)
        
        elif source == "📄 PDF Document":
            pdf_file = st.file_uploader("Upload your PDF file", type=['pdf'])
            if pdf_file: 
                with st.spinner("Extracting PDF text..."):
                    raw_data = extract_pdf(pdf_file)
        
        else:
            raw_data = st.text_area("Write a topic or paste long text content:")

        # Action Button
        if st.button("Transmute & Analyze ✨"):
            if raw_data and "Error" not in raw_data:
                with st.spinner("Alchemist is decoding the content..."):
                    st.session_state.topic = raw_data[:1000] # Save context for chatbot
                    st.session_state.wisdom = get_alchemist_explanation(model, raw_data)
                    st.session_state.yt = get_yt_suggestions(model, raw_data)
                    st.session_state.step = "revelation"
                    st.rerun()
            elif "Error" in raw_data:
                st.error(raw_data)
            else:
                st.warning("Please provide some content first!")

    # PHASE 2: REVELATION SCREEN (Output)
    elif st.session_state.step == "revelation":
        st.header("🔮 The Revelation")
        
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.markdown("<div class='logic-card'>", unsafe_allow_html=True)
            st.subheader("📜 Wisdom Decoded")
            st.markdown(st.session_state.wisdom)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col_right:
            st.markdown("<div class='logic-card' style='border-left-color: #ff4b4b;'>", unsafe_allow_html=True)
            st.subheader("📡 Resource Radar")
            st.write("Best YouTube videos to master this:")
            st.markdown(st.session_state.yt, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Back Button
        if st.button("Start New Quest 🎯"):
            st.session_state.step = "input"
            st.session_state.wisdom = ""
            st.session_state.yt = ""
            st.rerun()