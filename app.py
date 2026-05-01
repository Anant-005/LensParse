import streamlit as st
from PIL import Image
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# =========================
# 🎨 ENTERPRISE UI CONFIG
# =========================
st.set_page_config(
    page_title="LensParse | Gen 2.5 AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS for a High-Tech Portfolio Aesthetic
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #050505;
        font-family: 'Inter', sans-serif;
        color: #E0E0E0;
    }

    .hero-section {
        padding: 2rem 0rem;
        background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .data-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 25px;
        backdrop-filter: blur(10px);
    }

    .stButton>button {
        background: linear-gradient(135deg, #0072FF 0%, #00C6FF 100%);
        color: white;
        border: none;
        height: 3em;
        border-radius: 8px;
        font-weight: 700;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(0, 114, 255, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# ⚙️ CORE ENGINE (GEN 2.5)
# =========================
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Explicitly targeting the 2.5 Flash model
MODEL_ID = "gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_ID)

PROMPT = """
Extract structured data from the document and return ONLY valid JSON.
Format dates as YYYY-MM-DD. Use null for missing values.
"""

# =========================
# 🏗️ UI LAYOUT
# =========================
cols = st.columns([4, 1])
with cols[0]:
    st.markdown('<h1 class="hero-section">LensParse.ai</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#888; font-size:1.1rem; margin-top:-20px;">Multimodal Intelligence for Structured Data Extraction</p>', unsafe_allow_html=True)
with cols[1]:
    st.write("")
    st.markdown(f'<div style="text-align:right;"><span style="background:#111; padding:8px 12px; border-radius:20px; border:1px solid #333; font-size:0.8rem; color:#00C6FF;">● Gen 2.5 Flash</span></div>', unsafe_allow_html=True)

st.markdown("---")

main_left, main_right = st.columns([1, 1], gap="large")

with main_left:
    st.markdown("### 💠 Input Workspace")
    with st.container():
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Document Upload", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
        
        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with main_right:
    st.markdown("### ⚡ AI Structured Output")
    
    if uploaded_file:
        if st.button("🚀 EXECUTE AI EXTRACTION", use_container_width=True):
            with st.spinner("Processing via Gemini 2.5 Flash..."):
                try:
                    # Multimodal inference
                    response = model.generate_content([PROMPT, image])
                    raw_output = response.text

                    # Sanitization logic
                    try:
                        parsed = json.loads(raw_output)
                    except:
                        cleaned = raw_output.replace('```json', '').replace('```', '').strip()
                        parsed = json.loads(cleaned)

                    st.markdown('<div class="data-card">', unsafe_allow_html=True)
                    st.json(parsed)
                    
                    st.download_button(
                        "📥 DOWNLOAD JSON DATA",
                        json.dumps(parsed, indent=2),
                        "lensparse_export.json",
                        use_container_width=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.success("Analysis Complete.")
                except Exception as e:
                    st.error(f"Engine Error: {str(e)}")
    else:
        st.info("Upload a document to enable AI processing.")

# =========================
# 🛡️ PORTFOLIO FOOTER
# =========================
st.markdown("<br><br><p style='text-align:center; color:#444; font-size:0.8rem;'>Project: LensParse | Developer: Anant Singh <br> Specialized in GenAI and Autonomous Agents</p>", unsafe_allow_html=True)