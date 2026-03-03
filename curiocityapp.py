import streamlit as st
import os
from dotenv import load_dotenv
from utils import *

# ==============================
# 🔐 LOAD ENVIRONMENT VARIABLES
# ==============================

load_dotenv()

# ==============================
# 🎨 PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="CurioCity | AI Alchemist",
    page_icon="🧪",
    layout="wide"
)

# ==============================
# 🎨 LOAD CSS SAFELY
# ==============================

if os.path.exists("styles.css"):
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("⚠ styles.css not found. Default UI loaded.")

# ==============================
# 🤖 INITIALIZE MODEL (CACHED)
# ==============================

@st.cache_resource
def load_model():
    return setup_model()

model = load_model()

# ==============================
# 🧠 SESSION STATE INIT
# ==============================

if "auth" not in st.session_state:
    st.session_state.update({
        "auth": False,
        "username": "",
        "step": "input",
        "wisdom": "",
        "yt": "",
        "topic": "General Learning",
        "history": []
    })

# ==============================
# 🔐 LOGIN SCREEN
# ==============================

if not st.session_state.auth:

    st.markdown(
        "<h1 style='text-align: center; color: #4834d4;'>🏙️ CurioCity Prototype</h1>",
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns([1, 1.5, 1])

    with c2:
        st.markdown("<div class='logic-card'>", unsafe_allow_html=True)

        name = st.text_input("Enter your Alchemist Name:")

        if st.button("Unleash The Lab 🚀"):
            if name.strip():
                st.session_state.username = name.strip()
                st.session_state.auth = True
                st.rerun()
            else:
                st.warning("Please enter a name to continue.")

        st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# 🏙️ MAIN APPLICATION
# ==============================

else:

    if not model:
        st.error("🚨 AI Model not loaded. Check API key.")
        st.stop()

    # ==========================
    # 🧙 SIDEBAR
    # ==========================

    st.sidebar.title(f"🧙‍♂️ {st.session_state.username}")
    st.sidebar.markdown("**Rank:** Senior Alchemist")
    st.sidebar.markdown("---")

    # Doubt Solver
    st.sidebar.subheader("💬 Sage Doubt Solver")

    doubt_input = st.sidebar.text_input("Ask a quick doubt...")

    if st.sidebar.button("Ask Sage"):
        if doubt_input.strip():
            with st.sidebar.spinner("Sage is thinking..."):
                answer = solve_doubt(
                    model,
                    doubt_input,
                    st.session_state.topic
                )
                st.session_state.history.append({
                    "q": doubt_input,
                    "a": answer
                })
        else:
            st.sidebar.warning("Enter a doubt first.")

    # Show last 2 chats
    for chat in reversed(st.session_state.history[-2:]):
        st.sidebar.info(f"**Q:** {chat['q']}\n\n**A:** {chat['a']}")

    # ==========================
    # 📥 INPUT SCREEN
    # ==========================

    if st.session_state.step == "input":

        st.header("🧪 Transmute Knowledge")

        source = st.selectbox(
            "Select Learning Source",
            [
                "▶️ YouTube Link",
                "📄 PDF Document",
                "📜 Raw Text / Topic"
            ]
        )

        raw_data = ""

        # --------------------------
        # YOUTUBE INPUT
        # --------------------------
        if source == "▶️ YouTube Link":

            url = st.text_input("Paste YouTube URL here:")

            if url.strip():
                with st.spinner("Fetching transcript..."):
                    raw_data = get_yt_transcript(url)

                if "❌" in raw_data or "⚠" in raw_data:
                    st.error(raw_data)

        # --------------------------
        # PDF INPUT
        # --------------------------
        elif source == "📄 PDF Document":

            pdf_file = st.file_uploader("Upload PDF", type=["pdf"])

            if pdf_file:
                with st.spinner("Extracting text..."):
                    raw_data = extract_pdf(pdf_file)

                if "❌" in raw_data or "⚠" in raw_data:
                    st.error(raw_data)

        # --------------------------
        # RAW TEXT INPUT
        # --------------------------
        else:
            raw_data = st.text_area(
                "Write a topic or paste content:",
                height=200
            )

        # --------------------------
        # TRANSMUTE BUTTON
        # --------------------------

        if st.button("Transmute & Analyze ✨"):

            if raw_data and "❌" not in raw_data and "⚠" not in raw_data:

                with st.spinner("Alchemist decoding..."):

                    st.session_state.topic = raw_data[:1000]

                    st.session_state.wisdom = get_alchemist_explanation(
                        model,
                        raw_data
                    )

                    st.session_state.yt = get_yt_suggestions(
                        model,
                        raw_data
                    )

                    st.session_state.step = "revelation"

                st.rerun()

            else:
                st.warning("Please provide valid content first!")

    # ==========================
    # 🔮 OUTPUT SCREEN
    # ==========================

    elif st.session_state.step == "revelation":

        st.header("🔮 The Revelation")

        col1, col2 = st.columns([2, 1])

        # Wisdom Panel
        with col1:
            st.markdown("<div class='logic-card'>", unsafe_allow_html=True)
            st.subheader("📜 Wisdom Decoded")
            st.markdown(st.session_state.wisdom)
            st.markdown("</div>", unsafe_allow_html=True)

        # Resource Radar
        with col2:
            st.markdown(
                "<div class='logic-card' style='border-left-color:#ff4b4b;'>",
                unsafe_allow_html=True
            )
            st.subheader("📡 Resource Radar")
            st.markdown(
                st.session_state.yt,
                unsafe_allow_html=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # New Quest Button
        if st.button("Start New Quest 🎯"):
            st.session_state.step = "input"
            st.session_state.wisdom = ""
            st.session_state.yt = ""
            st.rerun()