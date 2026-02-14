"""
Google OAuth2 Integration for Content OS
Implements server-side OAuth flow for Google authentication
"""

import os
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from dotenv import load_dotenv

load_dotenv()

# OAuth Configuration
config = Config(environ=os.environ)
oauth = OAuth(config)

# Register OAuth providers
try:
    google = oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
except Exception:
    google = None

try:
    linkedin = oauth.register(
        name='linkedin',
        client_id=os.getenv('LINKEDIN_CLIENT_ID'),
        client_secret=os.getenv('LINKEDIN_CLIENT_SECRET'),
        authorize_url='https://www.linkedin.com/oauth/v2/authorization',
        access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
        client_kwargs={
            'scope': 'r_liteprofile r_emailaddress'
        }
    )
except Exception:
    linkedin = None

try:
    github = oauth.register(
        name='github',
        client_id=os.getenv('GITHUB_CLIENT_ID'),
        client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
        authorize_url='https://github.com/login/oauth/authorize',
        access_token_url='https://github.com/login/oauth/access_token',
        client_kwargs={
            'scope': 'user:email'
        }
    )
except Exception:
    github = None

def get_oauth_providers():
    """Returns configured OAuth providers"""
    providers = {}
    
    if google and os.getenv('GOOGLE_CLIENT_ID'):
        providers['google'] = google
    if linkedin and os.getenv('LINKEDIN_CLIENT_ID'):
        providers['linkedin'] = linkedin
    if github and os.getenv('GITHUB_CLIENT_ID'):
        providers['github'] = github
    
    return providers
