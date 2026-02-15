# ⚡ Content OS v5.0

**An AI-Native Content Operating System for the Complete Digital Content Lifecycle**

Content OS is an enterprise-grade platform that enhances every stage of content operations: creation, transformation, management, distribution, personalization, and performance analysis. Unlike single-use tools, it embeds AI at every decision point, acting as a true operating system for content teams.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)

---

## 🌟 Key Features

### 🎨 AI Content Creation Engine
- **7+ Content Modes**: Blog posts, Social Media, Video Scripts, Newsletters, Study Notes, Marketing Copy, Technical Documentation
- **Multi-Source Ingestion**:
  - Raw text ideas and brainstorming
  - Existing CMS projects for iteration
  - Document uploads (PDF with OCR, images)
  - YouTube video transcripts (automatic extraction)
  - Web URL scraping with semantic extraction
  - Direct text paste
- **Granular Controls**: 
  - Target audience selector (customizable)
  - Tone control (5 levels: Informal → Expert)
  - Length management (4 levels: Short → Deep Dive)
  - Explanation depth (4 levels: Basic → Expert)
  - Platform-specific formatting (LinkedIn, Twitter/X, Medium, Substack, GitHub README)
- **Advanced Options**: 
  - A/B variant generation for testing
  - Human-like rewriting to eliminate AI clichés
  - Analogy-based explanations for complex concepts
  - AI-text reduction and naturalization
- **Modern AI SDK**: Uses `google-genai` (latest) instead of deprecated `google-generativeai`
- **Auto-Save**: Generated content automatically saved to CMS with intelligent tagging

### 🔄 Content Transformation Engine
- **One-to-Many Conversions**: 
  - Convert long articles to social media threads
  - Transform videos/notes to blog posts
  - Generate interactive quizzes and flashcards
  - Create executive summaries
- **Semantic Refinement**: 
  - Simplification (ELI5 mode)
  - Expansion and elaboration
  - Reframing from new perspectives
  - Counter-argument generation
  - Tone adjustment
- **Interactive Quiz System**:
  - AI-generated question-answer pairs
  - Visual flashcard interface with animations
  - AI-powered answer evaluation with feedback
  - Progress tracking (correct/incorrect indicators)
  - Study mode with reveal/hide mechanism

### 📂 Smart Content Management System (CMS)
- **Git-Like Versioning**: Track every change with unique hash IDs and user attribution
- **Branch-Based Collaboration**: 
  - **Main Branch**: Developers & Co-Developers only
  - **User Branches**: Editors commit to side branches (`/branches/{username}/`)
  - **Merge Control**: Developers can merge collaborator changes to main
- **Folder Organization**: Categorize projects into custom folders with hierarchical structure
- **Semantic Search**: Meaning-based discovery (not just keywords)
- **AI-Generated Tags**: Automatic topic tagging
- **Topic Clustering**: Related content grouping
- **Metadata Tracking**: 
  - Automated word count and reading time
  - Collaborator tracking with roles
  - AI generation parameters
  - Engagement predictions
  - Version history with timestamps
- **Content Lifecycle**: Idea → Draft → Review → Approval → Publication → Archival

### 👥 Collaboration Hub
- **Role-Based Access Control**:
  - **Developer (Owner)**: Full control, manage team, create share links, merge branches
  - **Co-Developer**: Same as Developer (shared leadership)
  - **Editor**: Edit content, push to side branches only, no team management
  - **Viewer**: Read-only access, no editing capabilities
  - **Analyst**: View analytics, read-only content
  - **Admin**: Full system access, user management
- **Shareable Links**: 
  - Cryptographically secure invite URLs (SHA-256)
  - Customizable default roles per link
  - Revocable at any time
  - URL-based invite acceptance
  - Link expiration tracking
- **Manual Team Management**:
  - Search and add users by username
  - Real-time role assignment
  - User existence validation
  - Centralized team dashboard
- **Workspace Management**:
  - Multiple workspaces per user
  - Team invitations
  - Permission levels (View, Edit, Publish, Admin)

### 🔐 Enterprise Authentication & Security
- **JWT Authentication**: Industry-standard token-based security (30-day expiry for local use)
- **Argon2 Password Hashing**: Modern, unlimited-length password support (OWASP recommended)
- **OAuth 2.0 Integration**:
  - 🌐 Google (OpenID Connect)
  - 💼 LinkedIn
  - 🐙 GitHub
  - Auto-user creation on first OAuth login
  - Secure callback handling
- **Session Management**: Secure user sessions with logout functionality
- **Default Credentials**: `admin` / `admin123` (change immediately in production!)
- **Security Headers**: X-Content-Type-Options, X-Frame-Options, CSP, HSTS
- **Input Sanitization**: HTML escaping, character limits, XSS prevention
- **API Key Redaction**: Error messages automatically redact API keys

### 🧠 Personalization & Predictive Engine
- **AI-Powered Behavior Tracking**: 
  - Session duration and interaction counts
  - Project engagement metrics
  - User preference learning
  - Focus area prediction
- **Predictive Engagement Analytics**: 
  - Automatically predicts likes, comments, shares BEFORE publication
  - Calculates engagement scores (0-100)
  - Recommends optimal posting times
  - Predicts content reach (Low/Medium/High/Viral)
  - Provides confidence scores
- **Dynamic Audience Insights**: 
  - AI-generated demographic predictions
  - Engagement pattern analysis (Quick Scanners, Deep Readers, Visual Learners)
  - Sentiment analysis (Positive/Neutral/Negative)
  - Interest topic extraction
  - Retention rate calculation
- **Smart Content Editor**:
  - AI-assisted editing with natural language instructions
  - Tone adaptation based on user preferences
  - Personalized content summaries
  - Real-time feedback loop
- **Continuous Learning**: 
  - Tracks prediction accuracy
  - Records successful tones and platforms
  - Builds user preference models
  - Adapts recommendations over time

### 🤖 AI Creative Assistant (Copilot Mode)
- **Inline Assistance**:
  - Headline improvement
  - Hook suggestions
  - Clarity enhancement
  - Redundancy reduction
  - Natural language editing ("Make this funnier", "Simplify this section")
- **Idea Intelligence**:
  - Content gap detection
  - Trend-based topic suggestions
  - Seasonal and event hooks
- **Quality Filters**:
  - Generic content detection
  - Cliché identification
  - Originality enhancement suggestions

### 📤 Multi-Format Export & Publishing
- **Export Formats**:
  - **Markdown (.md)**: Native format with full formatting
  - **HTML**: Standalone web pages with premium styling
    - Responsive design (mobile-first)
    - Dark mode aesthetics
    - Scroll progress indicator
    - Typography optimization (Google Fonts)
    - GitHub Pages ready
  - **Word (.docx)**: Microsoft Word compatible documents
  - **PDF**: Professional PDF generation with headers
  - **JSON**: Structured metadata export
- **Web Boilerplate Generator**:
  - Production-ready standalone HTML pages
  - Gradient visual effects
  - Scroll animations
  - Client-side markdown rendering (marked.js)
  - SEO-ready with meta tags

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

### 4. First Login
- Open http://localhost:8501
- Login with: `admin` / `admin123`
- **Important**: Change the default password immediately!

### 5. Create Your First Project
1. Navigate to **Creation Engine**
2. Select content mode (e.g., "Blog Post")
3. Enter your ideas or upload a document
4. Configure audience, tone, and length
5. Click **Generate Content**
6. Review and save to CMS Library

---

## 📂 Project Structure

```
Content-OS/
├── app.py                    # Streamlit dashboard (main UI)
├── main_api.py               # FastAPI server + OAuth endpoints
├── core.py                   # Shared AI/CMS logic & utilities
├── auth.py                   # JWT authentication & user management
├── oauth_providers.py        # OAuth 2.0 integration (Google/LinkedIn/GitHub)
├── project_sharing.py        # Collaboration system & share links
├── requirements.txt          # Python dependencies
├── design.md                 # System architecture documentation
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── LICENSE                   # MIT License
├── smart_cms_data/           # Local project storage (git-ignored)
│   ├── {folder}/             # User-created folders
│   │   └── {project_id}/     # Individual projects
│   │       ├── meta.json     # Project metadata
│   │       ├── main/         # Main branch versions
│   │       │   └── v_*.json  # Version files
│   │       └── branches/     # Collaborator branches
│   │           └── {user}/   # User-specific branches
└── security_data/            # Security files (git-ignored)
    ├── users.json            # User credentials & profiles
    └── share_links.json      # Shareable link database
```

---

## 🎯 Use Cases

### For Content Creators
- Generate blog posts from video transcripts
- Create social media content variations (A/B testing)
- Transform long-form content into multiple formats
- Track content versions and iterate based on feedback
- Export to multiple formats for different platforms

### For Marketing Teams
- Collaborate on campaign content with role-based access
- Predict engagement before publishing
- Generate platform-specific content variations
- Track content performance predictions vs. actuals
- Maintain brand consistency across team members

### For Educators
- Create study materials from lecture notes
- Generate interactive quizzes and flashcards
- Transform complex topics into simplified explanations
- Share educational content with students (Viewer role)
- Track content revisions and improvements

### For Technical Writers
- Generate documentation from code or specifications
- Create multiple documentation formats (README, Wiki, PDF)
- Collaborate with developers on technical content
- Version control for documentation updates
- Export to GitHub-ready formats

### For Researchers
- Summarize research papers and articles
- Generate executive summaries for stakeholders
- Create presentations from research notes
- Collaborate with co-authors on papers
- Track document revisions with full history

---

## 💡 Collaboration Workflow

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
| Action | Developer | Co-Developer | Editor | Viewer | Analyst |
|--------|-----------|--------------|--------|--------|---------|
| View Content | ✅ | ✅ | ✅ | ✅ | ✅ |
| Edit Content | ✅ | ✅ | ✅ | ❌ | ❌ |
| Push to Main Branch | ✅ | ✅ | ❌ | ❌ | ❌ |
| Manage Team | ✅ | ✅ | ❌ | ❌ | ❌ |
| Create Share Links | ✅ | ✅ | ❌ | ❌ | ❌ |
| View Analytics | ✅ | ✅ | ✅ | ❌ | ✅ |

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Frontend** | Streamlit | 1.31+ |
| **Backend API** | FastAPI | 0.110+ |
| **Web Server** | Uvicorn | 0.27+ |
| **AI Model** | Google Gemini 1.5 Flash | via `google-genai` 0.2+ |
| **Authentication** | JWT (python-jose) | 3.3+ |
| **Password Hashing** | Argon2-cffi | 23.1+ |
| **OAuth** | Authlib | 1.3+ |
| **Session Management** | Starlette | 0.36+ |
| **Web Scraping** | BeautifulSoup4 | 4.12+ |
| **PDF Processing** | PyPDF | 4.0+ |
| **Document Export** | python-docx, fpdf2 | Latest |
| **YouTube** | youtube-transcript-api | 0.6+ |
| **HTTP Client** | httpx, requests | Latest |
| **Environment** | python-dotenv | 1.0+ |
| **Data Validation** | Pydantic | 2.7+ |
| **Database** | JSON (file-based) | Native |

---

## 📝 API Documentation

Once the FastAPI backend is running, access interactive API docs at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Authentication Endpoints
- `POST /token` - Login and get JWT token
- `GET /users/me/` - Get current user info
- `GET /auth/{provider}` - Initiate OAuth flow (google/linkedin/github)
- `GET /auth/{provider}/callback` - OAuth callback handler

### Content Creation Endpoints
- `POST /create` - Generate AI content with parameters
- `POST /transform` - Transform existing content
- `POST /personalize/predict_engagement` - Get engagement predictions
- `POST /personalize/predict_audience` - Get audience insights
- `POST /personalize/predict_user_behavior` - Get user behavior predictions
- `POST /personalize/summarize` - Generate personalized summary
- `POST /personalize/adapt_tone` - Adapt content tone

### CMS Endpoints
- `GET /cms/folders` - List all folders
- `POST /cms/folders/{folder}` - Create new folder
- `GET /cms/projects` - List all projects
- `GET /cms/project/{folder}/{project_id}` - Get project details
- `POST /cms/project` - Create new project
- `POST /cms/project/commit` - Commit new version
- `GET /cms/project/{folder}/{project_id}/compare` - Compare versions

### Ingestion Endpoints
- `POST /ingest/url` - Ingest content from URL
- `POST /ingest/file` - Ingest uploaded file (PDF, images)

---

## 🔐 Security Highlights

### Authentication & Authorization
- **JWT Tokens**: Secure, stateless authentication with 30-day expiry (configurable)
- **Argon2 Hashing**: Industry-leading password security (no 72-byte limit like bcrypt)
- **OAuth 2.0**: Secure social login with auto-user provisioning
- **Role-Based Access**: Granular permissions (Developer, Co-Developer, Editor, Viewer, Analyst, Admin)
- **Session Management**: Secure session handling with logout

### Data Protection
- **Input Sanitization**: All outputs are HTML-escaped to prevent XSS attacks
- **Resource Limits**: 
  - 50,000-character input cap
  - 50-page PDF limit
  - Request timeouts
- **Environment Verification**: Startup checks validate API keys and `.env` security
- **Git Protection**: `.env`, `security_data/`, and `smart_cms_data/` are strictly gitignored
- **API Key Redaction**: Error messages automatically redact API keys

### API Security
- **CORS Policy**: Managed cross-origin resource sharing (configurable for production)
- **Protected Endpoints**: All API routes require valid JWT tokens
- **Session Middleware**: Required for OAuth state management
- **Security Headers**: 
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - X-XSS-Protection: 1; mode=block
  - Strict-Transport-Security: max-age=31536000
  - Content-Security-Policy: default-src 'self'

### Cryptographic Security
- **Share Links**: SHA-256 hashed tokens
- **Password Storage**: Argon2id with automatic salt generation
- **JWT Signing**: HS256 algorithm with secret key
- **Secure Randomness**: Uses `secrets` module for token generation

---

## 💡 Tips & Best Practices

### Content Creation
- **Use Multi-Source Ingestion**: Combine ideas from multiple sources for richer content
- **Leverage A/B Testing**: Generate variants to test different approaches
- **Platform Optimization**: Always select the target platform for better formatting
- **Save Iterations**: Use CMS versioning to track content evolution

### Collaboration
- **Clear Roles**: Assign appropriate roles based on team member responsibilities
- **Branch Strategy**: Editors work in branches, Developers merge to main
- **Share Links**: Use time-limited share links for external collaborators
- **Regular Merges**: Developers should regularly review and merge branch contributions

### Security
- **Change Default Password**: Immediately change `admin` password after first login
- **Rotate API Keys**: Regularly rotate your Gemini API keys
- **Review Permissions**: Periodically audit project collaborators and their roles
- **Revoke Old Links**: Deactivate share links that are no longer needed

### Performance
- **Folder Organization**: Use folders to categorize projects by topic or team
- **Regular Cleanup**: Archive or delete old projects to maintain performance
- **Export Important Content**: Regularly export critical content as backup
- **Monitor API Usage**: Track your Gemini API usage to avoid rate limits

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: "API Key is missing or invalid"
- **Solution**: Check `.env` file has valid `GEMINI_API_KEY`
- Ensure no extra spaces or quotes around the key
- Verify key is active in Google AI Studio

**Issue**: OAuth login not working
- **Solution**: Verify OAuth credentials in `.env`
- Check callback URLs match in provider console
- Ensure FastAPI backend is running on correct port
- Verify `API_BASE_URL` and `APP_BASE_URL` are correct

**Issue**: "Could not validate credentials" error
- **Solution**: JWT token may have expired
- Logout and login again
- Check `AUTH_SECRET_KEY` is consistent across restarts

**Issue**: Content not saving to CMS
- **Solution**: Check `smart_cms_data/` folder permissions
- Verify folder exists and is writable
- Check disk space availability

**Issue**: PDF/Image ingestion failing
- **Solution**: Verify file size is reasonable (< 10MB)
- Check file format is supported
- Try local fallback if API fails
- Ensure `pypdf` and image libraries are installed

**Issue**: Slow content generation
- **Solution**: Reduce input context length (< 20,000 chars)
- Check internet connection to Gemini API
- Try different model (e.g., gemini-1.5-flash)
- Monitor API rate limits

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

## 🔮 Roadmap & Future Features

### Q2 2026
- [ ] Real-time collaboration with WebSockets
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)
- [ ] Multi-language support

### Q3 2026
- [ ] RAG integration with ChromaDB
- [ ] Direct publishing to LinkedIn/Twitter/Medium
- [ ] DALL-E integration for image generation
- [ ] Advanced permission templates
- [ ] Audio file ingestion (lectures, podcasts)

### Q4 2026
- [ ] Enterprise SSO integration
- [ ] Custom AI model fine-tuning
- [ ] Workflow automation
- [ ] API rate limiting and quotas
- [ ] Plagiarism detection
- [ ] Fact-checking suggestions

### 2027 and Beyond
- [ ] Blockchain-based content verification
- [ ] AI-powered content recommendations
- [ ] Multi-tenant architecture
- [ ] White-label solutions
- [ ] Competitor content analysis
- [ ] Automated content calendars
- [ ] Mood-based content rewriting

---

## 📊 Performance Metrics

### Typical Performance
- **Content Generation**: 5-15 seconds (depends on length)
- **Transformation**: 3-10 seconds
- **CMS Operations**: < 1 second (local file system)
- **Engagement Prediction**: 2-5 seconds
- **OCR Processing**: 5-20 seconds (depends on document size)

### Scalability
- **Projects**: Tested with 1000+ projects
- **Versions**: Unlimited per project
- **Collaborators**: Up to 50 per project (recommended)
- **File Size**: Up to 10MB per upload
- **Concurrent Users**: 10-20 (Streamlit limitation)

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the repository
- 📢 Share with others

### Development Setup
```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/Content-OS.git
cd Content-OS

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes and test
streamlit run app.py

# Commit and push
git commit -m 'Add amazing feature'
git push origin feature/amazing-feature

# Open Pull Request
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ❌ Liability
- ❌ Warranty

---

## 🙏 Acknowledgments

### Technologies
- **Google Gemini** for powerful AI capabilities
- **Streamlit** for the amazing UI framework
- **FastAPI** for the blazing-fast backend
- **Authlib** for OAuth integration
- **Argon2** team for secure password hashing

### Inspiration
- Git version control system
- Notion's collaboration features
- Grammarly's AI assistance
- Medium's content platform

---

## 📧 Contact & Support

**Developer**: Sanhik Nandi  
**GitHub**: [@Sanhik-2](https://github.com/Sanhik-2)  
**Project**: [Content-OS](https://github.com/Sanhik-2/Content-OS)  
**Issues**: [GitHub Issues](https://github.com/Sanhik-2/Content-OS/issues)

### Support Channels
- 🐛 Bug Reports: GitHub Issues
- 💡 Feature Requests: GitHub Discussions
- 📧 Email: [Create an issue for contact]
- 💬 Community: GitHub Discussions

---

**Built with ❤️ for collaborative content creation**

*Version 5.0.0 - February 2026*

**Content OS: Your AI-Native Content Operating System**
