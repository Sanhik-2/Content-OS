# ⚡ Content OS v4.0

A high-performance, AI-driven content generation and management system. This platform allows users to create, transform, and manage professional-grade content using the Google Gemini model, featuring a unified backend accessible via both a **Streamlit Dashboard** and a **FastAPI Backend**.

## 🌟 Key Features

### 🎨 AI Content Creation Engine
- **Multiple Modes**: Blog posts, Social Media, Video Scripts, Newsletters, Study Notes, Marketing Copy, Technical Documentation.
- **Granular Controls**: Target audience selector, Tone control, Length management, Platform-specific formatting, and Explanation depth.
- **Advanced Options**: A/B variant generation, Human-like rewriting, and Analogy-based explanations.

### 🔄 Content Transformation Engine
- **One-to-Many**: Convert long articles to social threads, videos to blogs, and notes to quizzes.
- **Semantic Refinement**: Simplification (ELI5), Expansion, Reframing, and Counter-argument generation.

### 📂 Smart Content Management System (CMS)
- **Git-Like Versioning**: Track every change, compare versions with diff-checking, and rollback to previous states.
- **Folder Organization**: Categorize projects into custom folders.
- **Metadata Tracking**: Automated word count, reading time, and engagement simulation.

### 🧠 Personalization Engine
- **Behavior Tracking**: Session duration, interaction counts, and project engagement metrics.
- **AI-Powered Engagement Predictions**: Automatically predicts likes, comments, shares, and engagement scores based on content analysis.
- **Audience Insights**: AI-generated predictions for age groups, engagement patterns, sentiment, and interest topics.
- **Adaptive AI**: Suggests summaries and tone adjustments based on predicted performance and user preferences.
- **Continuous Learning**: Tracks prediction accuracy to improve future recommendations.


## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Google Gemini API Key

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Ashwath-Raj/AI-enhanced-Content-Creation.git
   cd AI-enhanced-Content-Creation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   Create a `.env` file in the root directory and add your API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

### 🖥️ Running the Application

#### Option A: Interactive Dashboard (Streamlit)
Best for end-users and content managers.
```bash
streamlit run app.py
```

#### Option B: Professional API Backend (FastAPI)
Best for developers integrating Content OS into other apps.
```bash
python main_api.py
```
- **API Entry**: `http://127.0.0.1:8000`
- **Interactive Documentation**: `http://127.0.0.1:8000/docs`

## 📂 Project Structure
- `app.py`: The Streamlit dashboard.
- `main_api.py`: FastAPI server implementation.
- `core.py`: Shared core logic and AI integration.
- `smart_cms_data/`: Local storage for projects and version history.

## 🚀 Deployment & Security

### GitHub Readiness
- **Environment Variables**: All sensitive keys are moved to `.env` (managed via `python-dotenv`).
- **Gitignore Protection**: `.env`, `smart_cms_data/`, and `__pycache__` are strictly ignored.
- **Dependency Pining**: All libraries in `requirements.txt` are pinned to specific versions to ensure environment stability.

### 🔐 Security Measures
- **Input Sanitization**: All content outputs are sanitized using `html.escape` to prevent XSS.
- **Resource Protection**: 
  - Input size limits (`MAX_INPUT_SIZE`) protect against resource exhaustion.
  - PDF processing is limited to 50 pages.
- **Environment Verification**: Automated startup checks verify that API keys are valid and not placeholders.
- **CORS Management**: FastAPI backend includes a managed CORS policy.
- **Leak Prevention**: Automated logic prevents starting the app if `.env` is detected as tracked by Git.

### 🌍 Cloud Deployment (Optional)
This app is ready for deployment on platforms like **Render**, **Railway**, or **Heroku**.
1. Set up a Python environment.
2. Add your `GEMINI_API_KEY` to the platform's Environment Variables.
3. Run `uvicorn main_api:app --host 0.0.0.0 --port 8000` for the API.
4. Run `streamlit run app.py --server.port $PORT` for the UI.

---
Built with ❤️ by [Ashwath-Raj](https://github.com/Ashwath-Raj)
