import os
import streamlit as st
import cohere

# === CONFIG ===
COHERE_API_KEY = os.getenv("COHERE_API_KEY") or "WzqmtxpUY4ImR6cpPnwUEerPoRJYBVxGELe9YNSM"

if not COHERE_API_KEY:
    st.error("⚠️ Cohere API Key not set!")
    st.stop()

# === SETUP ===
co = cohere.Client(COHERE_API_KEY)

# === FUNCTION ===
def generate_lyrics(prompt, language="English"):
    try:
        if language != "English":
            prompt += f"\n\nWrite the lyrics in {language} language."
        response = co.generate(prompt=prompt, max_tokens=500)
        return response.generations[0].text.strip()
    except Exception as e:
        return f"❌ Error generating lyrics: {e}"

# === CUSTOM CSS MAGIC ===
st.markdown("""
    <style>
    @keyframes rainbowBackground {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    body, .stApp {
        background: linear-gradient(-45deg, #ff6ec4, #7873f5, #4ade80, #facc15, #fb7185);
        background-size: 600% 600%;
        animation: rainbowBackground 15s ease infinite;
        color: white !important;
        font-family: 'Comic Sans MS', cursive;
    }

    .stTextInput>div>div>input, .stSelectbox, .stSlider {
        background-color: #ffffff10;
        color: black !important;
        border: 2px solid #ffffff50;
        border-radius: 12px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #ff6ec4, #7873f5, #4ade80, #facc15, #fb7185);
        border: none;
        border-radius: 999px;
        padding: 0.75em 2em;
        color: white;
        font-weight: bold;
        font-size: 1.2em;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
        transition: 0.3s ease;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(255, 255, 255, 0.6);
    }

    h1, h2, h3 {
        text-shadow: 2px 2px 5px #00000050;
    }

    .lyrics-box {
        background-color: rgba(0,0,0,0.5);
        border-radius: 12px;
        padding: 20px;
        color: white;
        font-size: 1.1em;
        white-space: pre-wrap;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# === STREAMLIT UI ===
st.title("✨ Magical AI Lyrics Generator 🌈")

title = st.text_input("🎵 Song Title", "Dreamscape Journey")
genre = st.selectbox("🎼 Genre", ["Pop", "Hip-Hop", "EDM", "Jazz", "Classical", "Lo-Fi"])
mood = st.selectbox("🎭 Mood", ["Uplifting", "Sad", "Energetic", "Chill", "Romantic"])
bpm = st.slider("🎚️ Tempo (BPM)", 60, 180, 100)
language = st.selectbox("🌍 Language", ["English", "Spanish", "French", "German", "Italian", 
                                       "Portuguese", "Russian", "Japanese", "Korean", "Chinese",
                                       "Hindi", "Arabic", "Turkish", "Dutch", "Swedish"])

if st.button("🎤 Generate Magical Lyrics"):
    with st.spinner("🪄 Crafting lyrics with a touch of magic..."):
        prompt = f"Write a {genre} song titled '{title}' with a {mood} mood and {bpm} BPM. Include a chorus and meaningful verses."
        lyrics = generate_lyrics(prompt, language)
        st.markdown("### 🌟 Your Enchanted Lyrics")
        st.markdown(f"<div class='lyrics-box'>{lyrics}</div>", unsafe_allow_html=True)

        st.download_button(
            label="💾 Download Lyrics as .txt",
            data=lyrics,
            file_name=f"{title.replace(' ', '_')}_lyrics.txt",
            mime="text/plain"
        )