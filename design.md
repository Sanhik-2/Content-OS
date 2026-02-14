# 🏗️ Content OS v5.0: System Architecture & Design Specification

## 1. Project Overview
**Content OS** is an AI-native operational system designed for professional content creators, marketers, and collaborative teams. It serves as a centralized hub for content ideation, generation, transformation, and team-based management, leveraging predictive AI models and role-based collaboration to optimize user engagement and branding consistency.

---

## 2. System Architecture
The system follows a **Decoupled Monolithic Architecture with Multi-User Collaboration**, allowing for both a rich interactive UI (Streamlit), a headless integration layer (FastAPI), and team-based project sharing.

### 2.1 Technical Stack
| Layer | Technology |
| :--- | :--- |
| **Frontend UI** | Streamlit (Inter-based Premium Styling) |
| **Backend API** | FastAPI / Uvicorn |
| **Security** | JWT (JSON Web Tokens), Argon2 Hashing, OAuth2 (Google/LinkedIn/GitHub) |
| **AI LLM** | Google Gemini 1.5 Flash (via `google-genai`) |
| **Persistence** | Local File System (JSON-wrapped Versioning, User DB, Share Links) |
| **Ingestion** | BeautifulSoup4 (Web), PyPDF (Documents), YouTube Transcript API |
| **Collaboration** | Role-based Access Control, Shareable Links, Branch Protection |

### 2.2 Visual Architecture Flow
```mermaid
graph TD
    A[User Interface - Streamlit] --> B[Core Engine - Shared Logic]
    C[Headless API - FastAPI] --> B
    D[OAuth Providers] --> C
    A --> E[Collaboration Hub]
    B --> F[AI Generation Module]
    B --> G[Smart CMS Strategy]
    B --> H[Multi-Source Ingestion]
    F <-> I[Google Gemini API]
    G <-> J[(Local JSON Data Store)]
    H <-> K[OCR API / Web / YT]
    E <-> L[(Share Links DB)]
    E <-> M[Permission System]
```

---

## 3. Core Modules

### 3.1 AI Creation Engine
- **Multimodal Generation**: Supports Blog Posts, Social Media, Scripts, and Technical Docs.
- **Optimization Parameters**: Depth sliders (Basic to Expert), Tone selection (Casual to Academic), and Platform-specific formatting.
- **Advanced Features**: A/B Variant generation, Human-like rewriting, and Analogy-based explanation.
- **Modern AI Integration**: Uses `google-genai` (latest SDK) replacing deprecated `google-generativeai`.

### 3.2 Global Content Management (Smart CMS)
- **Git-like Versioning**: Every save creates a unique hash `v_sha256.json` with user attribution.
- **Branch-Based Collaboration**: 
  - **Main Branch**: Developers & Co-Developers only
  - **User Branches**: Editors commit to `/branches/{username}/`
  - **Merge Control**: Developers can merge collaborator branches to main
- **Atomic Metadata**: Projects store word counts, read times, collaborators, and AI generation parameters in `meta.json`.
- **Project History**: Maintains linear history per branch allowing for version comparisons and rollbacks.

### 3.3 👥 Collaboration Hub (NEW)
- **Role Hierarchy**:
  | Role | Edit Content | Push to Main | Manage Team | Create Share Links |
  |------|-------------|--------------|-------------|-------------------|
  | **Developer** (Owner) | ✅ | ✅ | ✅ | ✅ |
  | **Co-Developer** | ✅ | ✅ | ✅ | ✅ |
  | **Editor** | ✅ | ❌ (side branches only) | ❌ | ❌ |
  | **Viewer** | ❌ (read-only) | ❌ | ❌ | ❌ |

- **Shareable Links**: 
  - Cryptographically secure tokens (SHA-256)
  - Role-based default permissions
  - Revocable at any time
  - URL-based invite acceptance

- **Manual User Addition**:
  - Search users by username
  - Assign roles on-the-fly
  - Validates user existence before adding

- **Team Management UI**:
  - Centralized "Collaboration Hub" panel
  - View all projects and team members
  - Generate/manage share links
  - Real-time role assignment

### 3.4 Personalization & Predictive Engine
- **User Behavior Modeling**: Analyzes session intensity and satisfaction to suggest next actions.
- **Predictive Engagement**: Uses AI to forecast likes, comments, and reach BEFORE publication.
- **Dynamic Audience Insights**: Predicts demographics, interest topics, and sentiment drift.

### 3.5 Ingestion Client
- **OCR Integration**: Robust processing of images and PDFs via an external render-hosted endpoint.
- **Semantic Scraper**: Extracts meaningful content from URLs and YouTube transcripts for context-aware generation.

---

## 4. Security & Authentication

### 4.1 Core Security
- **JWT Authentication**: All API endpoints and UI sections are protected by industry-standard JWT tokens (30-min expiry).
- **Argon2 Password Hashing**: Modern password security replacing bcrypt (no 72-byte limit).
- **Key Isolation**: Environment variables are strictly ignored by Git and verified on app startup.
- **Input Hardening**: 50,000-character input clipping to prevent API abuse.
- **Output Sanitization**: Universal HTML escaping to prevent XSS attacks in CMS and AI result panels.

### 4.2 OAuth 2.0 Integration
- **Supported Providers**: 
  - 🌐 Google (OpenID Connect)
  - 💼 LinkedIn
  - 🐙 GitHub

- **OAuth Flow**:
  1. User clicks social login button in Streamlit
  2. Redirects to FastAPI OAuth endpoint (`/auth/{provider}`)
  3. Provider authenticates user
  4. FastAPI receives callback with user info
  5. Auto-creates user account if new
  6. Issues JWT token
  7. Redirects back to Streamlit with token

- **Auto-User Creation**: OAuth users are automatically registered with secure random passwords.

### 4.3 User Database
- **Location**: `security_data/users.json`
- **Schema**:
  ```json
  {
    "username": {
      "email": "user@example.com",
      "full_name": "User Name",
      "hashed_password": "$argon2id$...",
      "disabled": false,
      "role": "creator"
    }
  }
  ```

### 4.4 Share Links Database
- **Location**: `security_data/share_links.json`
- **Schema**:
  ```json
  {
    "token_hash": {
      "folder": "Personal Study",
      "project_id": "12345_Project",
      "created_by": "developer_user",
      "default_role": "Editor",
      "created_at": "2026-02-14T12:00:00",
      "active": true
    }
  }
  ```

---

## 5. Deployment & Configuration

### 5.1 Environment Variables
```bash
# AI API
GEMINI_API_KEY=your_gemini_key_here

# Authentication
AUTH_SECRET_KEY=random_secret_for_jwt_signing

# OAuth (Optional)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# API Configuration
API_BASE_URL=http://localhost:8000
APP_BASE_URL=http://localhost:8501
```

### 5.2 Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Start FastAPI backend (for OAuth & API)
uvicorn main_api:app --reload --port 8000

# Start Streamlit frontend
streamlit run app.py
```

---

## 6. Future Roadmap

### 6.1 RAG-Integrated Content Discovery
- **Technology**: ChromaDB or Pinecone integration.
- **Feature**: Enable "Chat with your CMS" to pull insights from hundreds of past projects.

### 6.2 Real-Time Collaboration
- **Feature**: WebSocket-based live editing for Co-Developers.
- **Capability**: See cursor positions and edits in real-time.

### 6.3 Multi-Channel Direct Publishing
- **Feature**: Direct API connectors for **LinkedIn**, **Twitter/X**, and **Medium**.
- **Capability**: Schedule posts and track *actual* vs. *predicted* engagement.

### 6.4 Advanced Permissions
- **Feature**: Fine-grained permissions (e.g., "Editor-No-Delete").
- **Capability**: Custom role definitions per project.

### 6.5 Multimedia Transformation
- **Feature**: Integration with DALL-E 3 or Stable Diffusion to automatically generate featured images.

---

## 7. Migration Notes

### 7.1 From google-generativeai to google-genai
- **Old**: `import google.generativeai as genai`
- **New**: `from google import genai`
- **API Changes**: 
  - Old: `genai.configure()` + `GenerativeModel()`
  - New: `Client(api_key)` + `client.models.generate_content()`

### 7.2 From BCrypt to Argon2
- **Reason**: Argon2 supports unlimited password length and is OWASP-recommended.
- **Migration**: Existing users must reset passwords (or re-hash on next login).

---

*Document Version: 5.0.0*  
*Last Updated: 2026-02-14*  
*Major Features: Collaboration Hub, OAuth, Argon2, google-genai*
