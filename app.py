
import streamlit as st
import os
import glob
import json
import datetime
import time
import hashlib
import io
import difflib
import html
import re
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# --- Dependency Check ---
try:
    from google import genai
    import requests
    from bs4 import BeautifulSoup
    from pypdf import PdfReader
    from youtube_transcript_api import YouTubeTranscriptApi

    def get_youtube_transcript(url):
        try:
            import re
            # More robust video ID extraction
            match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
            if not match:
                return "Error: Could not find valid YouTube video ID."
            video_id = match.group(1)
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return " ".join([t['text'] for t in transcript])
        except Exception as e: return f"Error fetching YouTube transcript: {e}"

    dependencies_installed = True
except ImportError as e:
    dependencies_installed = False
    missing_module = str(e)

# --- Configuration & Setup ---
st.set_page_config(
    page_title="Content OS v4.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    :root {
        --bg-color: #050505;
        --card-bg: rgba(20, 20, 22, 0.7);
        --accent-blue: #1E90FF;
        --accent-red: #DC143C;
        --text-primary: #FFFFFF;
        --text-secondary: #A0A0A0;
        --glass-border: rgba(255, 255, 255, 0.08);
    }

    /* Global Overrides */
    .stApp {
        background-color: var(--bg-color);
        background-image: 
            radial-gradient(circle at 15% 15%, rgba(220, 20, 60, 0.12) 0%, transparent 35%),
            radial-gradient(circle at 85% 85%, rgba(30, 144, 255, 0.12) 0%, transparent 35%),
            radial-gradient(circle at 50% 50%, rgba(30, 144, 255, 0.03) 0%, transparent 50%);
        background-attachment: fixed;
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }

    /* Typography */
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #A0A0A0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 10, 12, 0.95) !important;
        border-right: 1px solid var(--glass-border);
    }
    
    section[data-testid="stSidebar"] .stRadio > label {
        color: var(--text-secondary);
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.1em;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, var(--accent-blue) 0%, #0056b3 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.6rem !important;
        font-weight: 600 !important;
        font-family: 'Outfit', sans-serif !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(30, 144, 255, 0.25) !important;
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(30, 144, 255, 0.45) !important;
        border: none !important;
    }

    /* Secondary Buttons Styling */
    button[data-testid="stBaseButton-secondary"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--glass-border) !important;
        color: var(--text-primary) !important;
        backdrop-filter: blur(5px);
    }
    
    button[data-testid="stBaseButton-secondary"]:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: var(--accent-blue) !important;
    }

    /* Cards */
    .content-card {
        background: var(--card-bg);
        backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 24px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .content-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent-blue), transparent);
        opacity: 0;
        transition: opacity 0.4s;
    }

    .content-card:hover {
        transform: translateY(-6px);
        border-color: rgba(30, 144, 255, 0.3);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }
    
    .content-card:hover::before {
        opacity: 1;
    }

    /* Status Tags */
    .badge {
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        backdrop-filter: blur(4px);
    }
    .status-Idea { background-color: rgba(30, 144, 255, 0.15); color: #60a5fa; border: 1px solid rgba(30, 144, 255, 0.3); }
    .status-Draft { background-color: rgba(255, 193, 7, 0.15); color: #fbbf24; border: 1px solid rgba(255, 193, 7, 0.3); }
    .status-Review { background-color: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
    .status-Approval { background-color: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
    .status-Publication { background-color: rgba(30, 144, 255, 0.25); color: #FFFFFF; border: 1px solid var(--accent-blue); }
    .status-Archival { background-color: rgba(220, 20, 60, 0.15); color: var(--accent-red); border: 1px solid rgba(220, 20, 60, 0.3); }

    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid var(--glass-border) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 1px var(--accent-blue) !important;
    }

    /* Metadata Box */
    .meta-box {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 16px;
        border: 1px solid var(--glass-border);
        margin-top: 15px;
        font-size: 0.85rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .main .block-container { padding: 1.5rem 1rem !important; }
        h1 { font-size: 2.2rem !important; }
        .content-card { padding: 20px; }
    }

    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .main .block-container > div {
        animation: fadeIn 0.6s ease-out forwards;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: var(--bg-color); }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-blue); }

    /* Flashcard Style */
    .flashcard {
        background: linear-gradient(135deg, #1e1e22 0%, #141416 100%);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        transition: transform 0.3s;
        cursor: pointer;
    }
    .flashcard:hover { transform: scale(1.02); border-color: var(--accent-blue); }
    .flashcard-q { font-size: 1.2rem; font-weight: 700; color: var(--accent-blue); margin-bottom: 15px; font-family: 'Outfit', sans-serif; }
    .flashcard-a { font-size: 1rem; color: #a1a1aa; opacity: 0.9; margin-top: 10px; padding: 10px; background: rgba(255,255,255,0.03); border-radius: 8px; width: 100%; }

    /* Ambient Light States */
    .flashcard.correct { 
        border-color: #22c55e !important; 
        box-shadow: 0 0 30px rgba(34, 197, 94, 0.2);
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, #141416 100%);
    }
    .flashcard.incorrect { 
        border-color: #ef4444 !important; 
        box-shadow: 0 0 30px rgba(239, 68, 68, 0.2);
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, #141416 100%);
    }

    /* Modal Styling */
    div[data-testid="stDialog"] {
        background-color: rgba(5, 5, 5, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
    }

</style>
""", unsafe_allow_html=True)

# --- Security Checks ---
def check_security():
    # 1. Check for .gitignore
    if not os.path.exists(".gitignore"):
        st.error("🚨 SECURITY DISASTER: .gitignore is missing! API keys are at risk.")
        st.stop()
    
    # 2. Check if .env is ignored
    with open(".gitignore", "r") as f:
        ignored = f.read()
        if ".env" not in ignored:
            st.error("🚨 SECURITY RISK: .env is not in .gitignore. Your keys might be leaked!")
            st.stop()

check_security()

from core import (
    call_gemini, generate_hash, extract_text_from_pdf, 
    calculate_reading_time, sanitize_text, IngestionClient, 
    ContentManager, CMS_ROOT, get_youtube_transcript, export_to_docx, export_to_pdf,
    check_env_security, predict_engagement_metrics, predict_audience_insights, predict_user_behavior
)

# Authentication Imports
from auth import authenticate_user, get_user, create_user

# 3. Check API Key
sec_ok, sec_msg = check_env_security()
if not sec_ok:
    st.error(sec_msg)
    st.info("Please update your `.env` file or Streamlit Secrets with a valid Google Gemini API key.")
    st.stop()

# --- Deployment Info ---
is_cloud = os.getenv("STREAMLIT_RUNTIME_ENV") is not None or os.path.exists("/app")
if is_cloud:
    with st.sidebar:
        st.warning("☁️ Running on Streamlit Cloud. Note: Local file storage (CMS Library) is ephemeral and will be cleared on app restart. Use export features to save your work.")


def st_call_gemini(prompt, task_type, model_name='gemini-2.5-flash'):
    res = call_gemini(prompt, task_type, model_name)
    if res and (res.startswith("AI Error") or res.startswith("Error")):
        st.error(res)
        return ""
    return res or ""

ingest_client = IngestionClient()
cms = ContentManager()

# --- AUTH SESSION MANAGEMENT ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = None

# --- PERSONALIZATION MONITORING ---
class UserBehaviorTracker:
    def __init__(self):
        if 'user_prefs' not in st.session_state:
            st.session_state['user_prefs'] = {
                "interactions": 0,
                "liked_tones": [],
                "preferred_length": "Medium",
                "session_start": time.time(),
                "clicked_projects": set(),
                "ai_learning_data": {  # AI-driven preference learning
                    "successful_tones": [],
                    "successful_platforms": [],
                    "engagement_history": [],
                    "model_prediction": None # Store AI behavior prediction here
                }
            }
    
    def log_interaction(self, interaction_type, details=None):
        st.session_state['user_prefs']['interactions'] += 1
        if interaction_type == "click_project":
            st.session_state['user_prefs']['clicked_projects'].add(details)
            
    def get_metrics_prediction(self):
        """Replaced manual metrics with AI-predicted user model"""
        if st.session_state['user_prefs']['ai_learning_data']['model_prediction'] is None:
            # Predict behavior if not already predicted
            history = list(st.session_state['user_prefs']['clicked_projects'])
            prediction = predict_user_behavior(history, st.session_state['user_prefs'])
            st.session_state['user_prefs']['ai_learning_data']['model_prediction'] = prediction
        
        return st.session_state['user_prefs']['ai_learning_data']['model_prediction']
    
    def update_preference(self, category, value, positive=True):
        if category == "tone":
            if positive:
                st.session_state['user_prefs']['liked_tones'].append(value)
                st.session_state['user_prefs']['ai_learning_data']['successful_tones'].append(value)
            elif value in st.session_state['user_prefs']['liked_tones']:
                st.session_state['user_prefs']['liked_tones'].remove(value)
        # Clear model prediction so it regenerates with new preferences
        st.session_state['user_prefs']['ai_learning_data']['model_prediction'] = None
    
    def record_ai_prediction_accuracy(self, predicted_score, actual_feedback):
        """Track how accurate AI predictions are for continuous learning"""
        st.session_state['user_prefs']['ai_learning_data']['engagement_history'].append({
            'predicted': predicted_score,
            'feedback': actual_feedback,
            'timestamp': time.time()
        })



# --- AUTHENTICATION UI ---
def login_screen():
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="font-size: 3.5rem; margin-bottom: 0.5rem;">⚡ Content OS</h1>
            <p style="color: var(--text-secondary); font-size: 1.2rem;">Professional AI-Native Operating System</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab1:
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("Sign In", use_container_width=True):
                user = authenticate_user(username, password)
                if user:
                    st.session_state['authenticated'] = True
                    st.session_state['user'] = user.username
                    st.success(f"Welcome back, {user.full_name or user.username}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try admin / admin123")

            st.markdown("---")
            st.caption("Or continue with")
            oc1, oc2, oc3 = st.columns(3)
            
            # OAuth buttons redirect to FastAPI endpoints
            api_base = os.getenv("API_BASE_URL", "http://localhost:8000")
            
            if oc1.button("🌐 Google"):
                st.markdown(f'<meta http-equiv="refresh" content="0; url={api_base}/auth/google">', unsafe_allow_html=True)
            if oc2.button("💼 LinkedIn"):
                st.markdown(f'<meta http-equiv="refresh" content="0; url={api_base}/auth/linkedin">', unsafe_allow_html=True)
            if oc3.button("🐙 GitHub"):
                st.markdown(f'<meta http-equiv="refresh" content="0; url={api_base}/auth/github">', unsafe_allow_html=True)
            
        with tab2:
            new_user = st.text_input("New Username")
            new_email = st.text_input("Email")
            new_pass = st.text_input("New Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")
            
            if st.button("Create Account", use_container_width=True):
                if new_pass != confirm_pass:
                    st.error("Passwords do not match!")
                elif len(new_pass) < 6:
                    st.error("Password too short!")
                else:
                    success, msg = create_user({
                        "username": new_user,
                        "email": new_email,
                        "password": new_pass,
                        "disabled": False,
                        "role": "creator"
                    })
                    if success:
                        st.success("Account created! You can now login.")
                    else:
                        st.error(msg)
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop() if not st.session_state['authenticated'] else None

# Check authentication before showing the app
if not st.session_state['authenticated']:
    login_screen()

tracker = UserBehaviorTracker()

# --- UI STATE MANAGEMENT ---
if 'authenticated' not in st.session_state: st.session_state['authenticated'] = False
if 'user' not in st.session_state: st.session_state['user'] = None
if 'nav_engine' not in st.session_state: st.session_state['nav_engine'] = 'CMS Library'
if 'active_project' not in st.session_state: st.session_state['active_project'] = None
if 'generated_content' not in st.session_state: st.session_state['generated_content'] = ""

# --- SIDEBAR NAV ---
with st.sidebar:
    st.markdown(f"""
        <div style="padding: 1rem 0; text-align: center;">
            <p style="color: var(--text-secondary); margin: 0; font-size: 0.8rem;">Logged in as</p>
            <p style="color: var(--accent-blue); font-weight: 700; margin: 0;">{st.session_state['user']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.title("⚡ Content OS")
    st.markdown("---")
    
    engine = st.radio("Core Engine", ["CMS Library", "Creation Engine", "Transformation Engine", "Personalization Engine"], index=["CMS Library", "Creation Engine", "Transformation Engine", "Personalization Engine"].index(st.session_state['nav_engine']))
    st.session_state['nav_engine'] = engine
    
    st.markdown("---")
    if st.button("🚪 Logout"):
        st.session_state['authenticated'] = False
        st.session_state['user'] = None
        st.rerun()
    
    st.markdown("""
    <div style="margin-top: 10px; margin-bottom: 20px;">
        <span class="badge" style="background:rgba(30,144,255,0.1); color:var(--accent-blue); width: 100%; display: block; text-align: center;">Responsive Design Active</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    with st.expander("📂 Folder Manager", expanded=False):
        new_folder = st.text_input("New Folder", placeholder="Name...")
        if st.button("Create") and new_folder:
            os.makedirs(os.path.join(CMS_ROOT, new_folder), exist_ok=True)
            st.success(f"Created {new_folder}")
            time.sleep(0.5)
            st.rerun()
        
        folders = cms.get_folders()
        if folders:
            st.markdown("### Existing Folders")
            st.caption(", ".join(folders))
            
    with st.expander("📤 Import File to CMS", expanded=False):
        imp_file = st.file_uploader("Upload Document/Image", type=['txt', 'md', 'pdf', 'png', 'jpg', 'jpeg'])
        imp_folder = st.selectbox("Target Folder", folders or ["General"])
        if imp_file:
            imp_title = st.text_input("Project Title", os.path.splitext(imp_file.name)[0])
            if st.button("Import & Create"):
                text = ""
                extra_meta = {}
                
                # Try API Ingestion first for PDFs/Images
                if imp_file.type in ['application/pdf', 'image/png', 'image/jpeg', 'image/webp']:
                    with st.spinner("Analyzing document via OCR API..."):
                        api_res = ingest_client.ingest_file(imp_file.name, imp_file.getvalue(), imp_file.type)
                        if "text" in api_res:
                            text = api_res['text']
                            extra_meta = api_res.get('ocr_meta', {})
                            extra_meta['confidence'] = api_res.get('overall_confidence', 0)
                        else:
                            st.warning(f"API Ingestion failed, falling back to local: {api_res.get('error')}")
                
                # Fallback / Text files
                if not text:
                    if imp_file.type == "application/pdf":
                        text = extract_text_from_pdf(imp_file)
                    else:
                        try:
                            text = imp_file.getvalue().decode("utf-8")
                        except:
                            text = "Error: Could not decode text."
                
                if text:
                    cms.create_project(imp_title, imp_folder, text, st.session_state['user'], tags=["Imported", "Ingestion"], extra_meta=extra_meta)
                    st.success(f"Imported '{imp_title}'!")
                    if extra_meta.get('confidence'):
                        st.caption(f"Confidence: {extra_meta['confidence']}")
                    time.sleep(1)
                    st.rerun()

# --- WEB BOILERPLATE GENERATOR ---
def get_web_boilerplate(title, content):
    """
    Generates a standalone, premium HTML file for GitHub Pages deployment.
    Features heavy responsive design, typography optimization, and dark-mode aesthetics.
    """
    import html
    safe_title = html.escape(title)
    # Content is placed in a markdown script tag, but we should still be careful
    # especially about the closing script tag.
    safe_content = content.replace("</script>", "<\\/script>")
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title} | Content OS</title>
    <meta name="description" content="Professional content generated by Content OS">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #050505;
            --surface: #0A0A0B;
            --accent-blue: #1E90FF;
            --accent-red: #DC143C;
            --text: #FFFFFF;
            --text-dim: #A0A0A0;
            --border: rgba(255, 255, 255, 0.08);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: var(--bg); 
            color: var(--text); 
            font-family: 'Inter', sans-serif; 
            line-height: 1.7; 
            -webkit-font-smoothing: antialiased; 
        }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 80px 24px; min-height: 100vh; }}
        
        /* Premium Typography */
        h1 {{ 
            font-family: 'Outfit', sans-serif; 
            font-size: clamp(2.5rem, 8vw, 4rem); 
            line-height: 1.05; 
            margin-bottom: 24px; 
            background: linear-gradient(135deg, #fff 0%, #888 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.04em;
        }}
        .meta {{ 
            color: var(--text-dim); 
            font-size: 0.8rem; 
            margin-bottom: 60px; 
            display: flex; 
            align-items: center;
            gap: 15px;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            font-weight: 600;
        }}
        .meta::before {{
            content: "";
            width: 30px;
            height: 1px;
            background: var(--accent-blue);
        }}
        
        /* Markdown Content Styling */
        #content {{ font-size: 1.15rem; color: rgba(255,255,255,0.9); }}
        #content h2 {{ font-family: 'Outfit', sans-serif; margin: 56px 0 24px; font-size: 2.2rem; color: var(--text); letter-spacing: -0.02em; }}
        #content h3 {{ font-family: 'Outfit', sans-serif; margin: 40px 0 16px; font-size: 1.6rem; color: var(--text); }}
        #content p {{ margin-bottom: 28px; }}
        #content img {{ max-width: 100%; height: auto; border-radius: 24px; margin: 40px 0; border: 1px solid var(--border); box-shadow: 0 20px 40px rgba(0,0,0,0.4); }}
        #content pre {{ background: var(--surface); padding: 28px; border-radius: 16px; border: 1px solid var(--border); overflow-x: auto; margin: 40px 0; font-family: 'ui-monospace', monospace; }}
        #content code {{ background: rgba(255,255,255,0.05); padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }}
        #content blockquote {{ border-left: 2px solid var(--accent-blue); padding: 8px 0 8px 32px; margin: 48px 0; font-style: italic; color: var(--text-dim); font-size: 1.4rem; line-height: 1.5; }}
        #content ul, #content ol {{ margin: 0 0 32px 24px; }}
        #content li {{ margin-bottom: 12px; }}
        
        /* Decorative Glows */
        .glow-red {{ position: fixed; top: -15%; left: -10%; width: 50%; height: 50%; background: radial-gradient(circle, rgba(220, 20, 60, 0.12) 0%, transparent 70%); pointer-events: none; z-index: -1; }}
        .glow-blue {{ position: fixed; bottom: -15%; right: -10%; width: 50%; height: 50%; background: radial-gradient(circle, rgba(30, 144, 255, 0.12) 0%, transparent 70%); pointer-events: none; z-index: -1; }}
        
        /* Scroll Progress */
        #progress {{ position: fixed; top: 0; left: 0; height: 3px; background: linear-gradient(90deg, var(--accent-red), var(--accent-blue)); width: 0%; z-index: 100; transition: width 0.1s; }}

        /* Responsive Improvements */
        @media (max-width: 768px) {{
            .container {{ padding: 60px 24px; }}
            #content {{ font-size: 1.05rem; }}
        }}
    </style>
</head>
<body>
    <div id="progress"></div>
    <div class="glow-red"></div>
    <div class="glow-blue"></div>
    
    <div class="container">
        <div class="meta"><span>Content OS</span> • <span id="date"></span></div>
        <h1>{safe_title}</h1>
        <div id="content">Loading article...</div>
    </div>

    <!-- DATA HIDDEN IN SCRIPT FOR JS TO PARSE -->
    <script id="raw-markdown" type="text/markdown">{safe_content}</script>

    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const raw = document.getElementById('raw-markdown').textContent;
            document.getElementById('content').innerHTML = marked.parse(raw);
            document.getElementById('date').textContent = new Date().toLocaleDateString('en-US', {{ month: 'long', day: 'numeric', year: 'numeric' }});
            
            window.onscroll = function() {{
                const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
                const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                const scrolled = (winScroll / height) * 100;
                document.getElementById("progress").style.width = scrolled + "%";
            }};
        }});
    </script>
</body>
</html>"""
    return html_template

# ================= CMS LIBRARY VIEW =================
if engine == "CMS Library":
    st.markdown("""
        <div class="content-card" style="background: linear-gradient(135deg, rgba(30, 144, 255, 0.1) 0%, transparent 100%);">
            <h1 style="margin:0;">📂 Content Library</h1>
            <p style="color: var(--text-secondary);">Manage, version, and export your professional assets.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Filter
    search_col, sort_col = st.columns([3, 1])
    search_q = search_col.text_input("🔍 Semantic Search (Topic/Tags)", placeholder="Search by meaning...")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Projects")
        # --- PROJECT MODALS ---
        @st.dialog("📄 Project Viewer", width="large")
        def project_viewer(p):
            folder, pid = p['folder'], p['project_id']
            meta = cms.get_meta(folder, pid)
            if not meta:
                st.error("Project metadata could not be retrieved.")
                if st.button("Close"): 
                    st.session_state.pop('show_viewer', None)
                    st.rerun()
                st.stop()
            
            # Collaboration Info
            st.markdown(f"## {p.get('title', '--None--')}")
            st.code(f"Share ID: {pid}", language="text")
            
            with st.expander("👥 Collaborators & Permissions"):
                owner_id = meta.get('owner', '--None--')
                owner_role = meta.get('collaborators', {}).get(owner_id, "Developer")
                st.write(f"**Owner:** {owner_id} ({owner_role})")
                st.write("**Collaborator Roles:**")
                st.json(meta.get('collaborators', {}))
                
                if meta.get('owner') == st.session_state['user']:
                    new_collab = st.text_input("Invite Collaborator (User ID)")
                    role = st.selectbox("Role", ["Editor", "Co-Developer", "Viewer"])
                    if st.button("➕ Grant Access"):
                        meta.get('collaborators', {})[new_collab] = role
                        # Update meta
                        import json
                        with open(os.path.join(CMS_ROOT, folder, pid, "meta.json"), "w") as f:
                            json.dump(meta, f, indent=2)
                        st.success("Permission updated!")
            
            # Switch between main and collaborator branches
            available_branches = ["main"]
            branch_root = os.path.join(CMS_ROOT, folder, pid, "branches")
            if os.path.exists(branch_root):
                available_branches += [d for d in os.listdir(branch_root) if os.path.isdir(os.path.join(branch_root, d))]
            
            sel_branch = st.selectbox("View Branch", available_branches)
            history = cms.get_history(folder, pid, sel_branch)
            
            if history:
                version_options = {f"v.{v['timestamp'][11:16]} ({v['version_id'][:6]})": i for i, v in enumerate(history)}
                v_sel = st.selectbox("Version History", options=list(version_options.keys()))
                view_version = history[version_options[v_sel]]
                
                st.markdown("---")
                st.markdown(view_version['content'])
                st.markdown("---")
                
                # Developer Tools: Merging
                if sel_branch != "main" and meta.get('owner') == st.session_state['user']:
                    if st.button("✨ Merge this version to Main", use_container_width=True):
                        with st.spinner("Merging..."):
                            cms.merge_branch(folder, pid, sel_branch, view_version['version_id'], st.session_state['user'])
                            st.success("Merged successfully!")
                            st.rerun()

                c1, c2 = st.columns(2)
                if c1.button("✏️ Edit Content", use_container_width=True):
                    st.session_state['show_editor'] = p
                    if 'show_viewer' in st.session_state: del st.session_state['show_viewer']
                    st.rerun()
                if c2.button("❌ Close", use_container_width=True):
                    if 'show_viewer' in st.session_state: del st.session_state['show_viewer']
                    st.rerun()

        @st.dialog("✏️ Project Editor", width="large")
        def project_editor(p):
            folder, pid = p['folder'], p['project_id']
            meta = cms.get_meta(folder, pid)
            if not meta:
                st.error("Metadata missing.")
                st.stop()
                
            history = cms.get_history(folder, pid)
            if history:
                st.markdown(f"## Editing: {p.get('title', '--None--')}")
                latest = history[0]
                edited = st.text_area("Content", latest.get('content', ""), height=500)
                
                ec1, ec2, ec3 = st.columns([2, 2, 1])
                new_status = ec1.selectbox("Status", ContentManager.LIFECYCLE_STAGES, index=ContentManager.LIFECYCLE_STAGES.index(latest['status']))
                msg = ec2.text_input("Commit Message", "Manual update from editor")
                
                # Permission Check
                meta = cms.get_meta(folder, pid)
                if not meta:
                    is_authorized = False
                else:
                    is_authorized = meta.get('owner') == st.session_state['user'] or meta.get('collaborators', {}).get(st.session_state['user']) in ['Editor', 'Co-Developer']
                
                if ec3.button("💾 Save Changes", use_container_width=True, disabled=not is_authorized):
                    if is_authorized:
                        cms.commit_version(folder, pid, edited, st.session_state['user'], p['title'], latest.get('tags', []), new_status, msg)
                        st.toast("Pushed to your branch/main!")
                        if 'show_editor' in st.session_state: del st.session_state['show_editor']
                        st.rerun()
                    else:
                        st.error("Access Denied.")
                        
                if not is_authorized:
                    st.warning("⚠️ View-Only Mode: You don't have permission to commit changes.")
                if st.button("⬅️ Back to Viewer"):
                    st.session_state['show_viewer'] = p
                    if 'show_editor' in st.session_state: del st.session_state['show_editor']
                    st.rerun()

        # Trigger Modals from State
        if st.session_state.get('show_viewer'): project_viewer(st.session_state['show_viewer'])
        if st.session_state.get('show_editor'): project_editor(st.session_state['show_editor'])

        projects = cms.list_all_content()
        for p in projects:
            if search_q.lower() in p['title'].lower() or search_q.lower() in str(p['tags']).lower():
                with st.container():
                    st.markdown(f"""
                    <div class="content-card">
                        <div style="display:flex;justify-content:space-between;align-items:center">
                            <h4 style="margin:0">{sanitize_text(p['title'])}</h4>
                            <span class="badge status-{sanitize_text(p['status'])}">{sanitize_text(p['status'])}</span>
                        </div>
                        <small style="color:#6b7280; display:block; margin-top:5px;">
                            📁 {sanitize_text(p['folder'])} • 🕒 {sanitize_text(p['last_modified'][:10]) if p.get('last_modified') else 'N/A'}
                        </small>
                        <div style="margin-top:8px;">
                            <span style="font-size:0.8em; background:rgba(30,144,255,0.1); color:var(--accent-blue); padding:2px 6px; border-radius:4px;">
                                {p.get('latest_metrics', {}).get('word_count', 0)} words
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("🔍 Open Project", key=f"btn_{p['project_id']}", use_container_width=True):
                        st.session_state['show_viewer'] = p
                        st.rerun()

    with col2:
        st.markdown("""
            <div class="content-card" style="height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; border-style: dashed; opacity: 0.6; text-align:center;">
                <h3 style="margin:0;">Project Explorer</h3>
                <p>Select a project to view history and manage content.</p>
            </div>
        """, unsafe_allow_html=True)

# ================= CREATION ENGINE =================
elif engine == "Creation Engine":
    st.markdown("""
        <div class="content-card" style="background: linear-gradient(135deg, rgba(30, 144, 255, 0.1) 0%, transparent 100%);">
            <h1 style="margin:0;">🎨 Creation Engine</h1>
            <p style="color: var(--text-secondary);">Generate high-fidelity content from any source material.</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        # --- INPUTS ---
        with col1:
            st.subheader("1. Source & Mode")
            mode = st.selectbox("Content Mode", 
                ["Blog Post", "Social Media Post", "Video Script", "Newsletter", "Study Notes", "Marketing Copy", "Technical Documentation"])
            
            src_type = st.radio("Input Source", ["Raw Idea", "Existing Project", "Paste Text", "Document/Image Upload", "YouTube Video", "URL"])
            
            input_context = ""
            api_meta_data = None
            
            if src_type == "Raw Idea":
                input_context = st.text_area("Ideas / Topics", height=150)
            elif src_type == "Existing Project":
                all_projs = cms.list_all_content()
                if not all_projs:
                    st.warning("No existing projects found.")
                else:
                    proj_opts = {p['title']: p for p in all_projs}
                    selected_exist = st.selectbox("Select Project", list(proj_opts.keys()))
                    if selected_exist:
                        p_meta = proj_opts[selected_exist]
                        # Get latest version content
                        latest_content = cms.get_history(p_meta['folder'], p_meta['project_id'])[0]['content']
                        st.text_area("Preview", latest_content[:500]+"...", height=100, disabled=True)
                        input_context = latest_content
            
            elif src_type == "Paste Text":
                input_context = st.text_area("Paste Content", height=150)
            elif src_type == "Document/Image Upload":
                f = st.file_uploader("Upload (PDF, Images, Text)", type=["pdf", "png", "jpg", "jpeg", "webp", "txt", "md"])
                if f: 
                    # Use API if possible
                    if f.type in ['application/pdf', 'image/png', 'image/jpeg', 'image/webp']:
                         with st.spinner("Processing with Ingestion API..."):
                             res = ingest_client.ingest_file(f.name, f.getvalue(), f.type)
                             if "text" in res:
                                 input_context = res['text']
                                 api_meta_data = res.get('ocr_meta', {})
                                 st.success(f"Ingested! Confidence: {res.get('overall_confidence')}")
                             else:
                                 st.error(f"API Error: {res.get('error')}")
                                 # Fallback logic could go here if user wants, but API is preferred
                                 if f.type == "application/pdf":
                                     st.info("Attempting local PDF fallback...")
                                     input_context = extract_text_from_pdf(f)
                    else:
                        # Simple text read
                        input_context = f.getvalue().decode("utf-8")

            elif src_type == "YouTube Video":
                 yt_url = st.text_input("YouTube URL")
                 if yt_url: 
                     with st.spinner("Fetching Transcript..."):
                        input_context = get_youtube_transcript(yt_url)
                        if "Error" in input_context: st.error(input_context)
                        else: st.success("Transcript loaded!")
                        
            elif src_type == "URL":
                u = st.text_input("URL")
                if u:
                    with st.spinner("Ingesting URL..."):
                        # Try API first
                        res = ingest_client.ingest_url(u)
                        if "text" in res:
                             input_context = res['text']
                             api_meta_data = res.get('ocr_meta', {})
                             st.success(f"Page Ingested. Noise Level: {api_meta_data.get('noise_level', 'Unknown')}")
                        else:
                            st.warning(f"Ingestion API failed ({res.get('error')}). Using basic scraper.")
                            try: input_context = BeautifulSoup(requests.get(u).content, 'html.parser').get_text()[:5000]
                            except: st.error("Bad URL - Local scrape failed too.")

        # --- CONTROLS ---
        with col2:
            st.subheader("2. Generation Controls")
            audience = st.text_input("Target Audience", "General Tech")
            
            c_tone, c_len = st.columns(2)
            tone = c_tone.select_slider("Tone", ["Informal", "Casual", "Professional", "Academic", "Expert"])
            length = c_len.select_slider("Length", ["Short", "Medium", "Long", "Deep Dive"])
            
            depth = st.select_slider("Explanation Depth", ["Basic", "Intermediate", "Advanced", "Expert"])
            platform = st.selectbox("Platform Format", ["Generic", "LinkedIn", "Twitter/X", "Medium", "Substack", "GitHub README"])
            
            with st.expander("Advanced Options"):
                adv_ab = st.checkbox("Generate A/B Variants")
                adv_human = st.checkbox("Human-like Rewriting")
                adv_analogy = st.checkbox("Use Analogies")
            
            save_folder = st.selectbox("Save to Folder", cms.get_folders() or ["General"])

        if st.button("✨ Generate Content", use_container_width=True):
            if not input_context:
                st.error("Please provide valid input source.")
            else:
                with st.spinner("Compiling high-quality content..."):
                    prompt = f"""
                    ACT AS: Expert Content Creator.
                    TASK: Write a {mode}.
                    SOURCE MATERIAL: {input_context[:20000]}
                    
                    TARGET AUDIENCE: {audience}
                    TONE: {tone}
                    LENGTH: {length}
                    DEPTH: {depth}
                    PLATFORM: {platform}
                    
                    ADVANCED INSTRUCTIONS:
                    - { "Create 2 distinct variants (Option A and Option B)" if adv_ab else "Single high-quality version" }
                    - { "Use natural, human-like phrasing (avoid AI cliches)" if adv_human else "" }
                    - { "Explain complex concepts using simple analogies" if adv_analogy else "" }
                    """
                    
                    result = st_call_gemini(prompt, "creation")
                    if result:
                        st.session_state['generated_content'] = result
                        
                        # Auto-Tagging
                        tags = ["AI-Gen", mode, platform]
                        if adv_ab: tags.append("A/B Testing")
                        
                        # Store gen params in meta
                        gen_meta = {
                            "mode": mode,
                            "source_type": src_type,
                            "tone": tone,
                            "platform": platform
                        }
                        
                        # Save
                        title = f"{mode}: {audience[:15]}... ({datetime.datetime.now().strftime('%H:%M')})"
                        if save_folder == "General" and not os.path.exists(os.path.join(CMS_ROOT, "General")):
                            os.makedirs(os.path.join(CMS_ROOT, "General"))
                        
                        cms.create_project(title, save_folder, result, st.session_state['user'], tags, extra_meta=gen_meta)
                        st.success(f"Generated & Saved to '{save_folder}'!")

    if st.session_state['generated_content']:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Preview Generated Content")
        st.markdown(st.session_state['generated_content'][:1000] + ("..." if len(st.session_state['generated_content']) > 1000 else ""))
        
        @st.dialog("Fine-tune & Save Generation")
        def creation_edit_modal():
            st.markdown(f"#### Mode: {mode}")
            edited = st.text_area("Edit Content", st.session_state['generated_content'], height=500)
            target_f = st.selectbox("Target Folder", cms.get_folders() or ["General"])
            
            if st.button("💾 Save to Library"):
                # Auto-Tagging
                tags = ["AI-Gen", mode, platform]
                gen_meta = {"mode": mode, "source_type": src_type, "tone": tone, "platform": platform}
                title = f"{mode}: {audience[:15]}... ({datetime.datetime.now().strftime('%H:%M')})"
                
                cms.create_project(title, target_f, edited, st.session_state['user'], tags, extra_meta=gen_meta)
                st.toast(f"Saved to {target_f}!")
                st.rerun()

        if st.button("✨ Edit & Commit to Library", use_container_width=True):
            creation_edit_modal()
        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("📥 Quick Export"):
            qec1, qec2, qec3, qec4 = st.columns(4)
            res_text = st.session_state['generated_content']
            res_title = "Generated_Content"
            
            qec1.download_button("📥 Markdown", res_text, file_name=f"{res_title}.md", use_container_width=True)
            qec2.download_button("🌍 HTML", get_web_boilerplate(res_title, res_text), file_name=f"{res_title}.html", mime="text/html", use_container_width=True)
            
            try:
                docx_data = export_to_docx(res_title, res_text)
                qec3.download_button("📄 Word", docx_data, file_name=f"{res_title}.docx", 
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
            except Exception as e: 
                st.error(f"Docx Error: {e}")
            
            try:
                pdf_data = export_to_pdf(res_title, res_text)
                qec4.download_button("📕 PDF", pdf_data, file_name=f"{res_title}.pdf", mime="application/pdf", use_container_width=True)
            except Exception as e: 
                st.error(f"PDF Error: {e}")
            
            # JSON Quick Export
            res_json = json.dumps({"title": "Generated", "content": res_text, "timestamp": str(datetime.datetime.now())}, indent=2)
            st.download_button("📦 Download JSON Metadata", res_json, file_name="generated_content.json", mime="application/json")

# ================= TRANSFORMATION ENGINE =================
elif engine == "Transformation Engine":
    st.markdown("""
        <div class="content-card" style="background: linear-gradient(135deg, rgba(220, 20, 60, 0.1) 0%, transparent 100%);">
            <h1 style="margin:0;">🔄 Transformation</h1>
            <p style="color: var(--text-secondary);">Repurpose your content across formats and styles.</p>
        </div>
    """, unsafe_allow_html=True)
    
    projects = cms.list_all_content()
    opts = {p['title']: p for p in projects}
    sel_proj = st.selectbox("Select Content to Transform", list(opts.keys()) if opts else [])
    
    if sel_proj:
        meta = opts[sel_proj]
        current = cms.get_history(meta['folder'], meta['project_id'])[0]['content']
        st.text_area("Source", current, height=150, disabled=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("One-to-Many Conversion")
            trans_mode = st.selectbox("Convert To", 
                ["Social Media Thread", "Blog Post from Video/Notes", "Quiz/Flashcards", "Executive Summary"])
                
        with col2:
            st.subheader("Semantic Refinement")
            sem_mode = st.selectbox("Refinement Type", 
                ["Simplify (EL15)", "Expand/Elaborate", "Reframe (New Perspective)", "Counter-Argument Gen", "Tone Adjustment"])
        
        if st.button("🚀 Run Transformation"):
            with st.spinner("Transforming..."):
                if trans_mode == "Quiz/Flashcards":
                    prompt = f"""
                    TASK: Generate Educational Flashcards
                    SOURCE: {current[:15000]}
                    FORMAT: Provide a JSON array of objects.
                    Example: [{{ "question": "What is AI?", "answer": "Artificial Intelligence" }}]
                    RULES: 
                    1. Return ONLY the JSON. No markdown backticks.
                    2. Ensure all quotes are double quotes.
                    3. No trailing commas.
                    4. Content should be in {sem_mode} style.
                    """
                else:
                    prompt = f"""
                    TASK: Content Transformation
                    SOURCE: {current[:15000]}
                    PRIMARY GOAL: Convert to {trans_mode}
                    SECONDARY REFINEMENT: {sem_mode}
                    Keep the core meaning but adapt strictly to the new format.
                    """
                res = st_call_gemini(prompt, "transformation")
                st.session_state['transform_result'] = res
                st.session_state['trans_mode_active'] = trans_mode
    
    if 'transform_result' in st.session_state and st.session_state['transform_result'] is not None:
        st.markdown("### Transformation Result")
        
        # --- FLASHCARD VISUALIZATION ---
        if st.session_state.get('trans_mode_active') == "Quiz/Flashcards":
            try:
                # 1. Extreme Input Hardening
                res_val = st.session_state.get('transform_result', "")
                if res_val is None: res_val = ""
                
                raw_source = str(res_val).strip()
                if not raw_source:
                    st.info("Waiting for AI response...")
                    st.stop()
                
                # 2. Layered Unescaping & Cleaning
                import re as regex
                processed = html.unescape(raw_source)
                processed = regex.sub(r'^```json\s*', '', processed)
                processed = regex.sub(r'\s*```$', '', processed)
                
                # 3. Robust JSON Extraction
                match = regex.search(r'\[.*\]', processed, regex.DOTALL)
                if match:
                    json_str = str(match.group())
                    # Final prep for JSON parser
                    json_str = regex.sub(r',\s*\]', ']', json_str)
                    json_str = regex.sub(r',\s*\}', '}', json_str)
                    
                    flashcards = json.loads(json_str) or []
                    
                    # 4. State Management
                    if 'quiz_state' not in st.session_state:
                        st.session_state['quiz_state'] = {}
                    
                    @st.dialog("Quiz Result")
                    def quiz_modal(title, message):
                        st.markdown(f"### {title}")
                        st.write(str(message))
                        if st.button("Close"): st.rerun()

                    # 5. Safe Rendering Loop
                    cols = st.columns(2)
                    for idx, card in enumerate(flashcards):
                        if not card or not isinstance(card, dict): continue
                        
                        # Generate a stable key for session state
                        unique_id = hashlib.md5(f"{idx}_{json_str}".encode()).hexdigest()[:8]
                        card_id = f"card_{unique_id}"
                        state = st.session_state['quiz_state'].get(card_id, {"status": "default", "revealed": False})
                        
                        card_class = "flashcard"
                        if state.get('status') == "correct": card_class += " correct"
                        elif state.get('status') == "incorrect": card_class += " incorrect"
                        
                        with cols[idx % 2]:
                            # Render Question
                            q_text = str(card.get('question', '...'))
                            st.markdown(f"""<div class="{card_class}"><div class="flashcard-q">{q_text}</div></div>""", unsafe_allow_html=True)
                            
                            # Input & Action Controls
                            ans_input = st.text_input("Your Answer", key=f"in_{card_id}", label_visibility="collapsed", placeholder="Type answer here...")
                            
                            c1, c2 = st.columns(2)
                            if c1.button("✔️ Check", key=f"chk_{card_id}", use_container_width=True):
                                if not ans_input:
                                    st.warning("Please enter an answer.")
                                else:
                                    with st.spinner("AI Evaluating..."):
                                        check_prompt = f"QUESTION: {q_text}\nCORRECT: {card.get('answer')}\nUSER: {ans_input}\n\nTASK: Evaluate if the user is correct. Reply 'Correct' or 'Incorrect' first, then explain."
                                        feedback_res = st_call_gemini(check_prompt, "validation")
                                        if feedback_res:
                                            is_right = feedback_res.strip().lower().startswith("correct")
                                            st.session_state['quiz_state'][card_id] = {
                                                "status": "correct" if is_right else "incorrect",
                                                "revealed": True,
                                                "feedback": feedback_res
                                            }
                                            if is_right: quiz_modal("🎉 Correct!", feedback_res)
                                            else: st.toast("Try again!", icon="❌")
                                            st.rerun()

                            if c2.button("👁️ " + ("Hide" if state.get('revealed') else "Reveal"), key=f"rev_{card_id}", use_container_width=True):
                                st.session_state['quiz_state'][card_id] = {
                                    "status": state.get('status', 'default'), 
                                    "revealed": not state.get('revealed', False),
                                    "feedback": state.get('feedback', card.get('answer'))
                                }
                                st.rerun()

                            if state.get('revealed'):
                                f_text = str(state.get('feedback', card.get('answer', '...')))
                                st.markdown(f"""<div class="flashcard-a"><b>AI Insight:</b><br>{f_text}</div>""", unsafe_allow_html=True)
                            st.markdown("<br>", unsafe_allow_html=True)
                else:
                    st.error("No valid flashcard data found in AI response.")
                    st.code(processed)
            except Exception as e:
                st.error(f"Visualization Error: {e}")
                with st.expander("🔍 System Diagnostic"):
                    st.code(traceback.format_exc())
                st.text_area("Developer Log (Raw)", str(st.session_state.get('transform_result', 'No Data')), height=150)
        else:
            st.markdown(st.session_state['transform_result'])
        
        # --- MODAL EDITOR ---
        @st.dialog("Edit & Commit Transformation")
        def edit_modal():
            st.markdown(f"#### Refining: {sel_proj}")
            edited = st.text_area("Content Editor", st.session_state['transform_result'], height=400)
            
            c1, c2 = st.columns(2)
            msg = c1.text_input("Commit Message", "Refined via Transformation")
            if c2.button("✅ Confirm & Save"):
                with st.spinner("Saving..."):
                    meta = opts[sel_proj]
                    tags = meta.get('tags', []) + [st.session_state.get('trans_mode_active', 'Transformed')]
                    cms.commit_version(
                        folder=meta['folder'],
                        project_id=meta['project_id'],
                        content=edited,
                        user_id=st.session_state['user'],
                        title=meta.get('title', '--None--'),
                        tags=tags,
                        status="Draft",
                        message=msg,
                        extra_meta={"transformation_type": st.session_state.get('trans_mode_active')}
                    )
                    st.toast("Updated successfully!")
                    st.rerun()

        if st.button("✏️ Edit & Save as New Version"):
            edit_modal()

# ================= PERSONALIZATION ENGINE =================
elif engine == "Personalization Engine":
    st.markdown("""
        <div class="content-card" style="background: linear-gradient(135deg, rgba(30, 144, 255, 0.1) 0%, rgba(220, 20, 60, 0.05) 100%);">
            <h1 style="margin:0;">🧠 Personalization</h1>
            <p style="color: var(--text-secondary);">AI-driven audience insights and engagement predictive modeling.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 1. AI User Behavior Predictive Modeling
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.subheader("📊 AI User Behavior & Modeling")
    predictions = tracker.get_metrics_prediction()
    pmc1, pmc2, pmc3 = st.columns(3)
    pmc1.metric("Predicted Intensity", f"{predictions['predicted_intensity']}%")
    pmc2.metric("Satisfaction Prediction", f"{predictions['satisfaction_prediction']}%")
    pmc3.metric("Model Confidence", f"{predictions['learning_confidence']}%")
    
    st.info(f"**Predicted Focus Area:** {predictions['focus_area']}")
    st.success(f"**Suggested Next Action:** {predictions['suggested_action']}")
    
    # AI-Predicted Engagement Score for the user session
    st.progress(predictions['predicted_intensity'], text="Predicted User Engagement Level")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # 2. Dynamic Personalization Workspace
    st.subheader("🎯 Content Personalization & Smart Editor")
    
    # Select Project (CSM File)
    all_projects = cms.list_all_content()
    proj_map = {p['title']: p for p in all_projects}
    
    col_sel, col_act = st.columns([1, 2])
    
    with col_sel:
        st.markdown("#### Select Source (CSM)")
        selected_p_title = st.selectbox("Choose Project", list(proj_map.keys()), index=0 if list(proj_map.keys()) else None)
        
        if selected_p_title:
            p_data = proj_map[selected_p_title]
            tracker.log_interaction("click_project", selected_p_title)
            
            # --- AI-POWERED AUDIENCE ENGAGEMENT PREDICTIONS (Replaces Manual Input) ---
            with st.expander("🤖 AI-Predicted Engagement Analytics", expanded=True):
                st.caption("AI-generated predictions based on content analysis")
                
                # Get current content
                current_ver = cms.get_history(p_data['folder'], p_data['project_id'])[0]
                content = current_ver['content']
                
                # Extract metadata for better predictions
                tone = current_ver.get('extra_meta', {}).get('tone', 'Professional')
                platform = current_ver.get('extra_meta', {}).get('platform', 'Generic')
                audience = current_ver.get('extra_meta', {}).get('audience', 'General Tech')
                
                if st.button("🔮 Generate Engagement Predictions", key=f"pred_{p_data['project_id']}"):
                    with st.spinner("Analyzing content and predicting engagement..."):
                        # Get AI predictions
                        engagement_pred = predict_engagement_metrics(content, tone, platform)
                        audience_pred = predict_audience_insights(content, audience)
                        
                        # Store predictions in metadata
                        extra = current_ver.get('extra_meta', {})
                        extra['ai_engagement_prediction'] = engagement_pred
                        extra['ai_audience_insights'] = audience_pred
                        
                        cms.commit_version(
                            p_data['folder'], p_data['project_id'], 
                            current_ver['content'], 
                            p_data['title'], 
                            p_data['tags'], 
                            current_ver['status'], 
                            "AI Engagement Predictions Generated", 
                            extra_meta=extra
                        )
                        
                        st.success("✅ AI Predictions Generated!")
                        st.rerun()
                
                # Display predictions if they exist
                extra = cms.get_history(p_data['folder'], p_data['project_id'])[0].get('extra_meta', {})
                engagement_data = extra.get('ai_engagement_prediction', {})
                audience_data = extra.get('ai_audience_insights', {})
                
                if engagement_data:
                    st.markdown("#### 📊 Predicted Engagement Metrics")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("👍 Likes", engagement_data.get('likes', 0))
                    col2.metric("💬 Comments", engagement_data.get('comments', 0))
                    col3.metric("🔄 Shares", engagement_data.get('shares', 0))
                    col4.metric("🎯 Score", f"{engagement_data.get('engagement_score', 0)}/100")
                    
                    st.info(f"**Best Time to Post:** {engagement_data.get('best_time', 'N/A')} | "
                           f"**Predicted Reach:** {engagement_data.get('predicted_reach', 'N/A')} | "
                           f"**Confidence:** {engagement_data.get('confidence', 0)}%")
                
                if audience_data:
                    st.markdown("#### 👥 Audience Insights")
                    aud_col1, aud_col2 = st.columns(2)
                    with aud_col1:
                        st.write(f"**Age Group:** {audience_data.get('age_group', 'N/A')}")
                        st.write(f"**Engagement Pattern:** {audience_data.get('engagement_pattern', 'N/A')}")
                        st.write(f"**Preferred Length:** {audience_data.get('preferred_length', 'N/A')}")
                    with aud_col2:
                        st.write(f"**Sentiment:** {audience_data.get('sentiment', 'N/A')}")
                        st.write(f"**Retention Rate:** {audience_data.get('retention_rate', 0)}%")
                        topics = audience_data.get('interest_topics', [])
                        if topics:
                            st.write(f"**Interest Topics:** {', '.join(topics)}")
                
                # Feed predictions into learning model
                if engagement_data and engagement_data.get('engagement_score', 0) > 70:
                    tracker.update_preference("tone", tone, positive=True)


            # 3. Learning Feedback Loop Display
            st.info(f"Detected Tone Preference: {max(set(st.session_state['user_prefs']['liked_tones']), key=st.session_state['user_prefs']['liked_tones'].count) if st.session_state['user_prefs']['liked_tones'] else 'Neutral'}")

            st.markdown("#### ⚡ Quick Actions")
            if st.button("Summarize for Me"):
                with st.spinner("Personalizing summary..."):
                    # Get AI-Predicted Engagement Context
                    hist = cms.get_history(p_data['folder'], p_data['project_id'])[0]
                    ai_engagement = hist.get('extra_meta', {}).get('ai_engagement_prediction', {})
                    ai_audience = hist.get('extra_meta', {}).get('ai_audience_insights', {})
                    
                    # Dynamic Personalization with AI predictions
                    prompt = f"""
                    Summarize this content with insights from AI-predicted engagement analytics.
                    
                    USER PREFERENCES: {st.session_state['user_prefs']}
                    
                    AI-PREDICTED ENGAGEMENT METRICS:
                    - Expected Likes: {ai_engagement.get('likes', 'N/A')}
                    - Expected Comments: {ai_engagement.get('comments', 'N/A')}
                    - Engagement Score: {ai_engagement.get('engagement_score', 'N/A')}/100
                    - Predicted Reach: {ai_engagement.get('predicted_reach', 'N/A')}
                    
                    AI-PREDICTED AUDIENCE INSIGHTS:
                    - Age Group: {ai_audience.get('age_group', 'N/A')}
                    - Engagement Pattern: {ai_audience.get('engagement_pattern', 'N/A')}
                    - Sentiment: {ai_audience.get('sentiment', 'N/A')}
                    - Interest Topics: {', '.join(ai_audience.get('interest_topics', []))}
                    
                    Based on these predictions, explain:
                    1. Why this content is predicted to perform at this level
                    2. What elements contribute to the predicted engagement
                    3. Suggestions to improve engagement score
                    
                    Content: {hist['content'][:5000]}
                    """
                    summary = st_call_gemini(prompt, "personalization")
                    st.session_state['pers_output'] = summary

            if st.button("Adapt Tone to My Style"):
                with st.spinner("Adapting tone..."):
                    prompt = f"Rewrite this intro to match a professional but engaging tone (User Preference Model). Content: {cms.get_history(p_data['folder'], p_data['project_id'])[0]['content'][:1000]}"
                    adaptation = st_call_gemini(prompt, "personalization")
                    st.session_state['pers_output'] = adaptation

    with col_act:
        if selected_p_title:
            # CSM Editor Section (Working on previous CSM file)
            st.markdown(f"### 📝 Smart Editor: {selected_p_title}")
            
            # Load Content
            current_ver = cms.get_history(p_data['folder'], p_data['project_id'])[0]
            current_text = current_ver['content']
            
            # AI Assist Input
            ai_instruction = st.text_input("🤖 Ask AI to edit (e.g., 'Make the second paragraph funnier')", key="ai_edit_input")
            
            if st.button("Run AI Edit"):
                if ai_instruction:
                    with st.spinner("AI is editing..."):
                        edit_prompt = f"""
                        TASK: Edit the following text based on the user instruction.
                        INSTRUCTION: {ai_instruction}
                        TEXT TO EDIT:
                        {current_text}
                        
                        RETURN ONLY THE UPDATED TEXT.
                        """
                        edited_text = st_call_gemini(edit_prompt, "personalization")
                        if edited_text:
                            current_text = edited_text
                            st.session_state[f'edit_buffer_{p_data["project_id"]}'] = edited_text
                            st.success("AI Edit Applied! Review below.")
            
            # Editor Text Area
            # distinct key to allow manual override
            initial_val = st.session_state.get(f'edit_buffer_{p_data["project_id"]}', current_text)
            new_content = st.text_area("Edit Content", value=initial_val, height=500)
            
            # Save Controls
            if st.button("💾 Save Changes to CSM"):
                cms.commit_version(p_data['folder'], p_data['project_id'], new_content, p_data['title'], p_data['tags'], "Draft", "Personalized/Smart Edit")
                st.toast("Changes Saved!")
                tracker.log_interaction("save_edit")
                time.sleep(1)
                st.rerun()

            # Feedback Loop (Learning)
            if 'pers_output' in st.session_state:
                 st.markdown("---")
                 st.markdown("#### AI Suggestion / Output")
                 st.info(st.session_state['pers_output'])
                 
                 fb_col1, fb_col2 = st.columns(2)
                 if fb_col1.button("👍 Helpful"):
                     tracker.update_preference("tone", "Professional", True) # Simplified model update
                     st.toast("Feedback recorded: Preference updated.")
                 if fb_col2.button("👎 Not Helpful"):
                     tracker.update_preference("tone", "Professional", False)
                     st.toast("Feedback recorded: Adjustment noted.")
