
import streamlit as st
import os
import glob
import json
import datetime
import time
import hashlib
import io
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# --- Dependency Check ---
try:
    import google.generativeai as genai
    import requests
    from bs4 import BeautifulSoup
    from pypdf import PdfReader
    dependencies_installed = True
except ImportError as e:
    dependencies_installed = False
    missing_module = str(e)

# --- Configuration & Setup ---
st.set_page_config(
    page_title="Content OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    /* Premium Look */
    .main { background-color: #f8f9fa; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #111827; font-weight: 700; letter-spacing: -0.025em; }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white; border: none; border-radius: 8px;
        padding: 0.5rem 1.2rem; font-weight: 600;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.2);
    }
    .stButton>button:hover { transform: translateY(-1px); box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3); }
    
    /* Cards */
    .content-card {
        background: white; border-radius: 12px; padding: 24px;
        border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 16px; transition: border-color 0.2s;
    }
    .content-card:hover { border-color: #6366f1; }
    
    /* Status Tags */
    .badge { padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; }
    .status-Idea { background-color: #e0f2fe; color: #0369a1; }
    .status-Draft { background-color: #fef9c3; color: #854d0e; }
    .status-Review { background-color: #f3e8ff; color: #6b21a8; }
    .status-Published { background-color: #dcfce7; color: #15803d; }
    .status-Archived { background-color: #f3f4f6; color: #374151; }
    
    /* Tree View mockup */
    .tree-item { padding: 4px 8px; cursor: pointer; border-radius: 4px; }
    .tree-item:hover { background-color: #f3f4f6; }
</style>
""", unsafe_allow_html=True)

if not dependencies_installed:
    st.error(f"❌ Missing Dependency: {missing_module}")
    st.warning("Please run: `pip install google-generativeai beautifulsoup4 requests python-dotenv pypdf`")
    st.stop()

# --- Helpers ---
def get_api_key(task_type):
    key_map = {
        "creation": "GEMINI_API_KEY_CREATION",
        "transformation": "GEMINI_API_KEY_TRANSFORMATION",
        "cms": "GEMINI_API_KEY_CMS",
        "personalization": "GEMINI_API_KEY_PERSONALIZATION"
    }
    env_var = key_map.get(task_type)
    key = os.getenv(env_var)
    if not key or "YOUR_API_KEY" in key:
        key = os.getenv("GEMINI_API_KEY")
    return key.strip() if key else None

def call_gemini(prompt, task_type, model_name='gemini-2.5-flash'):
    api_key = get_api_key(task_type)
    if not api_key:
        st.error(f"⚠️ API Key for '{task_type}' is missing.")
        return None
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    try:
        return model.generate_content(prompt).text
    except Exception as e:
        st.error(f"AI Error: {e}")
        return None

def generate_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()[:12]

def extract_text_from_pdf(file):
    try:
        pdf = PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

# --- Smart CMS with Git-Like Versioning ---
CMS_ROOT = "smart_cms_data"

class ContentManager:
    LIFECYCLE_STAGES = ["Idea", "Draft", "Review", "Approval", "Publication", "Archival"]
    
    def __init__(self):
        if not os.path.exists(CMS_ROOT):
            os.makedirs(CMS_ROOT)
            
    def _get_path(self, folder, project_id):
        return os.path.join(CMS_ROOT, folder, project_id)

    def create_project(self, title, folder, content, tags=None):
        timestamp = int(time.time())
        project_id = f"{timestamp}_{title.lower().replace(' ', '_')[:20]}"
        path = self._get_path(folder, project_id)
        
        if not os.path.exists(path):
            os.makedirs(path)
            
        # Initial Commit
        self.commit_version(folder, project_id, content, title, tags or [], "Draft", "Initial commit")
        return project_id

    def commit_version(self, folder, project_id, content, title, tags, status, message="Update"):
        path = self._get_path(folder, project_id)
        timestamp = datetime.datetime.now().isoformat()
        
        # Calculate Hash
        content_hash = generate_hash(content + timestamp)
        
        version_data = {
            "version_id": content_hash,
            "timestamp": timestamp,
            "title": title,
            "content": content,
            "tags": tags,
            "status": status,
            "message": message
        }
        
        # Save Version File
        with open(os.path.join(path, f"v_{content_hash}.json"), "w") as f:
            json.dump(version_data, f, indent=2)
            
        # Update HEAD (Meta file)
        meta = {
            "current_head": content_hash,
            "folder": folder,
            "project_id": project_id,
            "last_modified": timestamp,
            "title": title, # Keep current title in meta for easy indexing
            "tags": tags,
            "status": status
        }
        with open(os.path.join(path, "meta.json"), "w") as f:
            json.dump(meta, f, indent=2)
            
        return content_hash

    def get_meta(self, folder, project_id):
        try:
            with open(os.path.join(self._get_path(folder, project_id), "meta.json"), "r") as f:
                return json.load(f)
        except: return None

    def get_version(self, folder, project_id, version_hash):
        try:
            with open(os.path.join(self._get_path(folder, project_id), f"v_{version_hash}.json"), "r") as f:
                return json.load(f)
        except: return None

    def get_history(self, folder, project_id):
        path = self._get_path(folder, project_id)
        files = glob.glob(os.path.join(path, "v_*.json"))
        history = []
        for f in files:
            with open(f, "r") as r:
                history.append(json.load(r))
        return sorted(history, key=lambda x: x['timestamp'], reverse=True)

    def list_all_content(self):
        # Scan all folders
        projects = []
        for folder_path in glob.glob(os.path.join(CMS_ROOT, "*")):
            if os.path.isdir(folder_path):
                folder_name = os.path.basename(folder_path)
                for proj_path in glob.glob(os.path.join(folder_path, "*")):
                    if os.path.isdir(proj_path):
                        proj_id = os.path.basename(proj_path)
                        meta = self.get_meta(folder_name, proj_id)
                        if meta:
                            projects.append(meta)
        return sorted(projects, key=lambda x: x['last_modified'], reverse=True)
    
    def get_folders(self):
        return [d for d in os.listdir(CMS_ROOT) if os.path.isdir(os.path.join(CMS_ROOT, d))]

cms = ContentManager()

# --- UI STATE MANGEMENT ---
if 'nav_engine' not in st.session_state: st.session_state['nav_engine'] = 'CMS'
if 'active_project' not in st.session_state: st.session_state['active_project'] = None

# --- SIDEBAR NAV ---
with st.sidebar:
    st.title("⚡ Content OS")
    st.markdown("---")
    
    # Engine Selector
    engine = st.radio("Select Engine", ["CMS Library", "Creation Engine", "Transformation Engine"], index=0)
    
    st.markdown("---")
    st.markdown("#### 📁 Quick Folders")
    
    # Simple Folder Creator
    new_folder = st.text_input("New Folder Name", placeholder="e.g. BlogPosts")
    if st.button("Create Folder") and new_folder:
        os.makedirs(os.path.join(CMS_ROOT, new_folder), exist_ok=True)
        st.success(f"Created {new_folder}")
        st.rerun()
        
    # List Folders
    folders = cms.get_folders()
    if not folders:
        st.caption("No folders yet.")
    for f in folders:
        st.markdown(f"📂 **{f}**")

# --- MAIN ENGINE VIEWS ---

# ================= CMS LIBRARY VIEW =================
if engine == "CMS Library":
    st.header("📂 Content Library")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Search & Filter
        search_q = st.text_input("🔍 Semantic Search", placeholder="Search by concept...")
        # (For now simple text search, could upgrade to embedding search later)
        
        st.markdown("### Projects")
        projects = cms.list_all_content()
        
        for p in projects:
            if search_q.lower() in p['title'].lower() or search_q.lower() in str(p['tags']).lower():
                with st.container():
                    # Card
                    st.markdown(f"""
                    <div class="content-card">
                        <div style="display:flex;justify-content:space-between;align-items:center">
                            <h4>{p['title']}</h4>
                            <span class="badge status-{p['status']}">{p['status']}</span>
                        </div>
                        <small style="color:#6b7280">{p['folder']} • Last mod: {p['last_modified'][:10]}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Open Editor", key=f"btn_{p['project_id']}"):
                        st.session_state['active_project'] = p
                        st.rerun()

    with col2:
        if st.session_state['active_project']:
            active_meta = st.session_state['active_project']
            folder = active_meta['folder']
            pid = active_meta['project_id']
            
            # Fetch History
            history = cms.get_history(folder, pid)
            latest_version = history[0]
            
            # --- EDITOR HEADER ---
            st.subheader(f"✏️ {latest_version['title']}")
            
            # Meta Controls
            c1, c2, c3 = st.columns(3)
            new_status = c1.selectbox("Lifecycle Status", ContentManager.LIFECYCLE_STAGES, index=ContentManager.LIFECYCLE_STAGES.index(latest_version['status']))
            
            # Version Control Dropdown
            version_options = {f"{v['timestamp'][:16]} - {v['message']} ({v['version_id'][:6]})": v for v in history}
            selected_v_key = c2.selectbox("History / Versions", list(version_options.keys()), index=0)
            view_version = version_options[selected_v_key]
            
            c3.markdown(f"**Current View:** `{view_version['version_id'][:8]}`")
            
            # Diff Check Logic could go here
            
            # --- CONTENT EDITOR ---
            edit_content = st.text_area("Content Body", view_version['content'], height=500)
            
            # Tags
            current_tags = ", ".join(view_version['tags'])
            edit_tags = st.text_input("Tags (comma separated)", current_tags)
            
            # --- SAVE ACTIONS ---
            sc1, sc2 = st.columns([1, 1])
            commit_msg = sc1.text_input("Commit Message", placeholder="What did you change?")
            
            if sc2.button("💾 Commit New Version"):
                if not commit_msg:
                    st.error("Please enter a commit message.")
                else:
                    tag_list = [t.strip() for t in edit_tags.split(",") if t.strip()]
                    cms.commit_version(folder, pid, edit_content, active_meta['title'], tag_list, new_status, commit_msg)
                    st.success("Committed successfully!")
                    time.sleep(1)
                    st.rerun()
            
            st.divider()
            if st.button("🤖 AI Analysis & Suggestions", type="secondary"):
                with st.spinner("Analyzing semantics..."):
                    prompt = f"Analyze this content for tone, clarity, and SEO improvements:\n\n{edit_content}"
                    rem = call_gemini(prompt, "cms")
                    st.info(rem)

        else:
            st.info("👈 Select a project from the list to edit.")

# ================= CREATION ENGINE =================
elif engine == "Creation Engine":
    st.header("🎨 AI Content Creation")
    
    with st.container():
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        # INPUT SOURCE
        with col1:
            st.subheader("1. Input Source")
            src_type = st.radio("Source Type", ["Raw Topic/Idea", "Text Paste", "PDF Upload", "URL"])
            
            input_context = ""
            if src_type == "Raw Topic/Idea":
                input_context = st.text_area("Enter your topic/idea", height=150)
            elif src_type == "Text Paste":
                input_context = st.text_area("Paste existing text", height=150)
            elif src_type == "PDF Upload":
                f = st.file_uploader("Upload PDF Transcript", type=["pdf"])
                if f:
                    txt = extract_text_from_pdf(f)
                    st.caption(f"Extracted {len(txt)} chars")
                    input_context = txt
            elif src_type == "URL":
                u = st.text_input("URL")
                if u:
                    try:
                        input_context = BeautifulSoup(requests.get(u).content, 'html.parser').get_text()[:5000] # Limit char count
                        st.caption("Extracted text from URL")
                    except: st.error("Invalid URL")

        # CONFIG
        with col2:
            st.subheader("2. Generation Config")
            out_format = st.selectbox("Output Format", ["Blog Post", "Social Thread", "Executive Summary", "Study Notes"])
            tone = st.select_slider("Tone", ["Informal", "Casual", "Professional", "Academic", "Expert"])
            audience = st.text_input("Target Audience", "General Audience")
            
            save_folder = st.selectbox("Save to Folder", cms.get_folders() or ["General"])

        generate_btn = st.button("✨ Generate & Draft", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    if generate_btn and input_context:
        with st.spinner("Generating content..."):
            prompt = f"""
            TASK: Create a {out_format}.
            SOURCE: {input_context[:10000]}
            AUDIENCE: {audience}
            TONE: {tone}
            
            Output should be formatted in Markdown.
            """
            result = call_gemini(prompt, "creation")
            
            if result:
                st.subheader("Result")
                st.markdown(result)
                
                # Auto-save to CMS
                title = f"{out_format} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
                if save_folder == "General" and not os.path.exists(os.path.join(CMS_ROOT, "General")):
                     os.makedirs(os.path.join(CMS_ROOT, "General"))
                     
                pid = cms.create_project(title, save_folder, result, tags=["AI-Generated", out_format])
                st.success(f"Saved to CMS as '{title}' in {save_folder}")

# ================= TRANSFORMATION ENGINE =================
elif engine == "Transformation Engine":
    st.header("🔄 Content Transformation")
    st.info("Convert existing content into new formats (One-to-Many).")
    
    # Select from CMS
    projects = cms.list_all_content()
    opts = {p['title']: p for p in projects}
    
    sel_proj = st.selectbox("Select Project to Transform", list(opts.keys()) if opts else [])
    
    if sel_proj:
        meta = opts[sel_proj]
        # Get latest content
        current = cms.get_history(meta['folder'], meta['project_id'])[0]['content']
        
        st.text_area("Source Content", current, height=150, disabled=True)
        
        target_format = st.selectbox("Transform To", ["Twitter/X Thread", "LinkedIn Post", "Quiz Questions", "Analogy Explanation"])
        
        if st.button("Run Transformation"):
            with st.spinner("Transforming..."):
                res = call_gemini(f"Transform this into a {target_format}:\n\n{current}", "transformation")
                st.markdown(res)
