"""
Project Sharing and Collaboration System
Generates shareable links and manages project permissions
"""

import hashlib
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

SHARE_LINKS_DB = "security_data/share_links.json"

class ProjectSharing:
    ROLES_HIERARCHY = {
        "Developer": 5,      # Owner - full control
        "Co-Developer": 5,   # Same as Developer
        "Editor": 3,         # Can edit, push to branches only
        "Viewer": 1          # Read-only
    }
    
    def __init__(self):
        self.ensure_db()
    
    def ensure_db(self):
        """Create share links database if it doesn't exist"""
        os.makedirs("security_data", exist_ok=True)
        if not os.path.exists(SHARE_LINKS_DB):
            with open(SHARE_LINKS_DB, 'w') as f:
                json.dump({}, f)
    
    def generate_share_link(self, folder: str, project_id: str, created_by: str, role: str = "Viewer") -> str:
        """Generate a shareable link for a project"""
        timestamp = datetime.now().isoformat()
        link_data = f"{folder}:{project_id}:{created_by}:{timestamp}"
        share_token = hashlib.sha256(link_data.encode()).hexdigest()[:16]
        
        # Store link metadata
        with open(SHARE_LINKS_DB, 'r') as f:
            links = json.load(f)
        
        links[share_token] = {
            "folder": folder,
            "project_id": project_id,
            "created_by": created_by,
            "default_role": role,
            "created_at": timestamp,
            "active": True
        }
        
        with open(SHARE_LINKS_DB, 'w') as f:
            json.dump(links, f, indent=2)
        
        return share_token
    
    def validate_share_link(self, share_token: str) -> Optional[Dict]:
        """Validate a share link and return project info"""
        with open(SHARE_LINKS_DB, 'r') as f:
            links = json.load(f)
        
        link_data = links.get(share_token)
        if link_data and link_data.get("active"):
            return link_data
        return None
    
    def revoke_share_link(self, share_token: str) -> bool:
        """Deactivate a share link"""
        with open(SHARE_LINKS_DB, 'r') as f:
            links = json.load(f)
        
        if share_token in links:
            links[share_token]["active"] = False
            with open(SHARE_LINKS_DB, 'w') as f:
                json.dump(links, f, indent=2)
            return True
        return False
    
    def get_project_links(self, folder: str, project_id: str) -> List[Dict]:
        """Get all active share links for a project"""
        with open(SHARE_LINKS_DB, 'r') as f:
            links = json.load(f)
        
        project_links = []
        for token, data in links.items():
            if (data["folder"] == folder and 
                data["project_id"] == project_id and 
                data["active"]):
                project_links.append({
                    "token": token,
                    **data
                })
        return project_links
    
    def can_push_to_main(self, user_role: str) -> bool:
        """Check if user role can push to main branch"""
        return self.ROLES_HIERARCHY.get(user_role, 0) >= 5
    
    def can_edit(self, user_role: str) -> bool:
        """Check if user role can edit content"""
        return self.ROLES_HIERARCHY.get(user_role, 0) >= 3
    
    def can_view(self, user_role: str) -> bool:
        """Check if user role can view content"""
        return self.ROLES_HIERARCHY.get(user_role, 0) >= 1

sharing = ProjectSharing()
