# ⚡ Content OS v5.0

**A collaborative, AI-native content generation and management platform.** Content OS empowers teams to create, transform, and manage professional-grade content using Google Gemini AI, featuring secure authentication, role-based collaboration, and a unified backend accessible via both a **Streamlit Dashboard** and **FastAPI Backend**.

---

## 🌟 Key Features

### 🎨 AI Content Creation Engine
- **Multiple Modes**: Blog posts, Social Media, Video Scripts, Newsletters, Study Notes, Marketing Copy, Technical Documentation.
- **Granular Controls**: Target audience selector, Tone control, Length management, Platform-specific formatting, and Explanation depth.
- **Advanced Options**: A/B variant generation, Human-like rewriting, and Analogy-based explanations.
- **Modern AI SDK**: Uses `google-genai` (latest) instead of deprecated `google-generativeai`.

### 🔄 Content Transformation Engine
- **One-to-Many**: Convert long articles to social threads, videos to blogs, and notes to quizzes.
- **Semantic Refinement**: Simplification (ELI5), Expansion, Reframing, and Counter-argument generation.

### 📂 Smart Content Management System (CMS)
- **Git-Like Versioning**: Track every change with user attribution, compare versions, and rollback to previous states.
- **Branch-Based Collaboration**: 
  - **Main Branch**: Developers & Co-Developers only
  - **User Branches**: Editors commit to side branches (`/branches/{username}/`)
  - **Merge Control**: Developers can merge collaborator changes to main
- **Folder Organization**: Categorize projects into custom folders.
- **Metadata Tracking**: Automated word count, reading time, collaborators, and engagement simulation.

### 👥 Collaboration Hub (NEW in v5.0)
- **Role-Based Access Control**:
  - **Developer (Owner)**: Full control, manage team, create share links
  - **Co-Developer**: Same as Developer (shared leadership)
  - **Editor**: Edit content, push to side branches only
  - **Viewer**: Read-only access
- **Shareable Links**: 
  - Cryptographically secure invite URLs
  - Customizable default roles
  - Revocable at any time
- **Manual Team Management**:
  - Search and add users by username
  - Real-time role assignment
  - Centralized team dashboard
- **URL-Based Invites**: Share projects via simple invite links that auto-join users

### 🔐 Enterprise Authentication & Security
- **JWT Authentication**: Industry-standard token-based security (30-min expiry)
- **Argon2 Password Hashing**: Modern, unlimited-length password support (OWASP recommended)
- **OAuth 2.0 Integration**:
  - 🌐 Google (OpenID Connect)
  - 💼 LinkedIn
  - 🐙 GitHub
  - Auto-user creation on first OAuth login
- **Session Management**: Secure user sessions with logout functionality
- **Default Credentials**: `admin` / `admin123` (change immediately!)

### 🧠 Personalization Engine
- **Behavior Tracking**: Session duration, interaction counts, and project engagement metrics.
- **AI-Powered Engagement Predictions**: Automatically predicts likes, comments, shares, and engagement scores.
- **Audience Insights**: AI-generated predictions for demographics, engagement patterns, sentiment, and interests.
- **Adaptive AI**: Suggests summaries and tone adjustments based on predicted performance.
- **Continuous Learning**: Tracks prediction accuracy to improve future recommendations.

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.9+**
- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))
- **(Optional)** OAuth credentials for social login

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sanhik-2/Content-OS.git
   cd Content-OS
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   Copy `.env.example` to `.env` and configure your keys:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env`:
   ```env
   # Required
   GEMINI_API_KEY=your_gemini_api_key_here
   AUTH_SECRET_KEY=generate_random_secret_here
   
   # Optional: OAuth (for social login)
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   LINKEDIN_CLIENT_ID=your_linkedin_client_id
   LINKEDIN_CLIENT_SECRET=your_linkedin_secret
   GITHUB_CLIENT_ID=your_github_client_id
   GITHUB_CLIENT_SECRET=your_github_secret
   
   # API URLs (default for local)
   API_BASE_URL=http://localhost:8000
   APP_BASE_URL=http://localhost:8501
   ```

### 🖥️ Running the Application

#### Full Stack Mode (Recommended)
Run both Streamlit UI and FastAPI backend for complete functionality:

**Terminal 1: FastAPI Backend** (for OAuth & API access)
```bash
uvicorn main_api:app --reload --port 8000
```

**Terminal 2: Streamlit Frontend**
```bash
streamlit run app.py
```

Then access:
- **Streamlit UI**: http://localhost:8501
- **FastAPI Docs**: http://localhost:8000/docs

#### Streamlit Only Mode
For basic usage without OAuth:
```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
Content-OS/
├── app.py                    # Streamlit dashboard
├── main_api.py               # FastAPI server + OAuth
├── core.py                   # Shared AI/CMS logic
├── auth.py                   # JWT authentication
├── oauth_providers.py        # OAuth 2.0 integration
├── project_sharing.py        # Collaboration system
├── requirements.txt          # Python dependencies
├── design.md                 # System architecture
├── .env.example              # Environment template
├── smart_cms_data/           # Local project storage
└── security_data/            # User & share link DBs
```

---

## � Collaboration Workflow

### Creating a Project
1. Login to Content OS
2. Navigate to **CMS Library**
3. Create a new project (you become the **Developer**)

### Sharing with Team
**Option 1: Shareable Link**
1. Open project in **CMS Library** or **Collaboration Hub**
2. Click **🔗 Create Link** under "Management Tools"
3. Choose default role (Viewer/Editor/Co-Developer)
4. Share the generated URL

**Option 2: Manual Addition**
1. Go to **👥 Collaboration Hub** → **➕ Invite Users**
2. Enter teammate's username
3. Select project and assign role
4. Click **Add to Project**

### Role Capabilities
| Action | Developer | Co-Developer | Editor | Viewer |
|--------|-----------|--------------|--------|--------|
| View Content | ✅ | ✅ | ✅ | ✅ |
| Edit Content | ✅ | ✅ | ✅ | ❌ |
| Push to Main Branch | ✅ | ✅ | ❌ | ❌ |
| Manage Team | ✅ | ✅ | ❌ | ❌ |
| Create Share Links | ✅ | ✅ | ❌ | ❌ |

---

## 🔐 Security Highlights

### Authentication
- **JWT Tokens**: Secure, stateless authentication with 30-minute expiry
- **Argon2 Hashing**: Industry-leading password security (no 72-byte limit like bcrypt)
- **OAuth 2.0**: Secure social login with auto-user provisioning

### Data Protection
- **Input Sanitization**: All outputs are HTML-escaped to prevent XSS attacks
- **Resource Limits**: 50,000-character input cap, 50-page PDF limit
- **Environment Verification**: Startup checks validate API keys and `.env` security
- **Git Protection**: `.env`, `security_data/`, and `smart_cms_data/` are strictly gitignored

### API Security
- **CORS Policy**: Managed cross-origin resource sharing
- **Protected Endpoints**: All API routes require valid JWT tokens
- **Session Middleware**: Required for OAuth state management

---

## 🌍 Cloud Deployment

### Requirements
- Python 3.9+ environment
- Cloud platform (Render, Railway, Heroku, DigitalOcean)

### Deployment Steps

1. **Set Environment Variables** on your platform:
   - `GEMINI_API_KEY`
   - `AUTH_SECRET_KEY`
   - (Optional) OAuth credentials

2. **Deploy FastAPI Backend**:
   ```bash
   uvicorn main_api:app --host 0.0.0.0 --port $PORT
   ```

3. **Deploy Streamlit Frontend**:
   ```bash
   streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```

4. **Update `.env` URLs**:
   ```env
   API_BASE_URL=https://your-api-domain.com
   APP_BASE_URL=https://your-streamlit-domain.com
   ```

### OAuth Callback URLs
When deploying, update OAuth redirect URIs in provider consoles:
- **Google**: `https://your-api-domain.com/auth/google/callback`
- **LinkedIn**: `https://your-api-domain.com/auth/linkedin/callback`
- **GitHub**: `https://your-api-domain.com/auth/github/callback`

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit 1.31+ |
| **Backend API** | FastAPI, Uvicorn |
| **AI Model** | Google Gemini 1.5 Flash (via `google-genai`) |
| **Authentication** | JWT, Argon2, OAuth2 (Authlib) |
| **Database** | JSON (file-based) |
| **Password Hashing** | Argon2-cffi |
| **OAuth** | Starlette, Authlib |

---

## 📝 API Documentation

Once the FastAPI backend is running, access interactive API docs at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints
- `POST /token` - Login and get JWT
- `GET /users/me/` - Get current user info
- `GET /auth/{provider}` - Initiate OAuth flow
- `POST /create/` - Generate content
- `POST /transform/` - Transform content
- `GET /cms/` - List all projects

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- **Google Gemini** for the powerful AI capabilities
- **Streamlit** for the amazing UI framework
- **FastAPI** for the blazing-fast backend
- **Authlib** for OAuth integration
- **Argon2** team for secure password hashing

---

## 📧 Contact & Support

**Developer**: Sanhik Nandi  
**GitHub**: [@Sanhik-2](https://github.com/Sanhik-2)  
**Project**: [Content-OS](https://github.com/Sanhik-2/Content-OS)

---

**Built with ❤️ for collaborative content creation**

*Version 5.0.0 - February 2026*
