from fastapi import FastAPI, HTTPException, UploadFile, File, Request, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
import os
from dotenv import load_dotenv

# Load environment before any other imports that might use env vars
load_dotenv(override=True)

from core import (
    call_gemini, ContentManager, IngestionClient, CMS_ROOT, 
    check_env_security, predict_engagement_metrics, 
    predict_audience_insights, predict_user_behavior
)

app = FastAPI(title="Content OS API", version="4.0")

# Security: CORS Policy (More restrictive for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origins like ["https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-API-Key"],
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
    return response

# Security Check on Startup
sec_ok, sec_msg = check_env_security()
if not sec_ok:
    print(sec_msg)

cms = ContentManager()
ingest_client = IngestionClient()


# --- Models ---

class CreationRequest(BaseModel):
    mode: str
    input_context: str
    audience: Optional[str] = "General Tech"
    tone: Optional[str] = "Professional"
    length: Optional[str] = "Medium"
    depth: Optional[str] = "Intermediate"
    platform: Optional[str] = "Generic"
    adv_ab: Optional[bool] = False
    adv_human: Optional[bool] = False
    adv_analogy: Optional[bool] = False
    save_folder: Optional[str] = "General"

class TransformationRequest(BaseModel):
    content: str
    trans_mode: str
    sem_mode: str

class CommitRequest(BaseModel):
    folder: str
    project_id: str
    content: str
    title: str
    tags: List[str]
    status: str
    message: Optional[str] = "Update"
    extra_meta: Optional[Dict[str, Any]] = None

class CreateProjectRequest(BaseModel):
    title: str
    folder: str
    content: str
    tags: Optional[List[str]] = None
    extra_meta: Optional[Dict[str, Any]] = None

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to Content OS API", "status": "online"}

# 1. AI Content Creation Engine
@app.post("/create")
async def create_content(req: CreationRequest):
    prompt = f"""
    ACT AS: Expert Content Creator.
    TASK: Write a {req.mode}.
    SOURCE MATERIAL: {req.input_context[:20000]}
    
    TARGET AUDIENCE: {req.audience}
    TONE: {req.tone}
    LENGTH: {req.length}
    DEPTH: {req.depth}
    PLATFORM: {req.platform}
    
    ADVANCED INSTRUCTIONS:
    - { "Create 2 distinct variants (Option A and Option B)" if req.adv_ab else "Single high-quality version" }
    - { "Use natural, human-like phrasing (avoid AI cliches)" if req.adv_human else "" }
    - { "Explain complex concepts using simple analogies" if req.adv_analogy else "" }
    """
    
    result = call_gemini(prompt, "creation")
    if not result or result.startswith("Error"):
        raise HTTPException(status_code=500, detail=result)
    
    # Optional auto-save
    tags = ["AI-Gen", req.mode, req.platform]
    if req.adv_ab: tags.append("A/B Testing")
    
    gen_meta = {
        "mode": req.mode,
        "tone": req.tone,
        "platform": req.platform,
        "audience": req.audience
    }
    
    project_id = cms.create_project(
        title=f"{req.mode}: {req.audience[:15]}...",
        folder=req.save_folder,
        content=result,
        tags=tags,
        extra_meta=gen_meta
    )
    
    return {"content": result, "project_id": project_id, "folder": req.save_folder}

# 2. Content Transformation Engine
@app.post("/transform")
async def transform_content(req: TransformationRequest):
    prompt = f"""
    TASK: Content Transformation
    SOURCE: {req.content[:15000]}
    
    PRIMARY GOAL: Convert to {req.trans_mode}
    SECONDARY REFINEMENT: {req.sem_mode}
    
    Keep the core meaning but adapt strictly to the new format.
    """
    result = call_gemini(prompt, "transformation")
    if not result or result.startswith("Error"):
        raise HTTPException(status_code=500, detail=result)
    
    return {"content": result}

# 3. Smart Content Management System (CMS)
@app.get("/cms/folders")
def list_folders():
    return {"folders": cms.get_folders()}

@app.post("/cms/folders/{folder}")
def create_folder(folder: str):
    os.makedirs(os.path.join(CMS_ROOT, folder), exist_ok=True)
    return {"message": f"Folder {folder} created."}

@app.get("/cms/projects")
def list_projects():
    return {"projects": cms.list_all_content()}

@app.get("/cms/project/{folder}/{project_id}")
def get_project(folder: str, project_id: str):
    meta = cms.get_meta(folder, project_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Project not found")
    history = cms.get_history(folder, project_id)
    return {"metadata": meta, "history": history}

@app.post("/cms/project")
def create_new_project(req: CreateProjectRequest):
    pid = cms.create_project(req.title, req.folder, req.content, req.tags, req.extra_meta)
    return {"project_id": pid}

@app.post("/cms/project/commit")
def commit_version(req: CommitRequest):
    cms.commit_version(req.folder, req.project_id, req.content, req.title, req.tags, req.status, req.message, req.extra_meta)
    return {"message": "Version committed successfully."}

# 4. Personalization Engine
@app.post("/personalize/log_interaction")
def log_interaction(interaction_type: str, details: Optional[Dict[str, Any]] = None):
    # In a real app, this would save to a DB. For now, we just acknowledge.
    return {"message": f"Interaction {interaction_type} logged.", "details": details}

@app.post("/personalize/predict_engagement")
def predict_engagement(content: str, tone: str = "Professional", platform: str = "Generic"):
    """AI-powered engagement prediction endpoint"""
    predictions = predict_engagement_metrics(content, tone, platform)
    return {
        "predictions": predictions,
        "message": "Engagement metrics predicted successfully"
    }

@app.post("/personalize/predict_audience")
def predict_audience(content: str, audience: str = "General Tech"):
    """AI-powered audience insights prediction endpoint"""
    insights = predict_audience_insights(content, audience)
    return {
        "insights": insights,
        "message": "Audience insights generated successfully"
    }

@app.post("/personalize/predict_user_behavior")
def predict_user_modeling(history: List[str], user_prefs: Dict[str, Any]):
    """AI-powered user behavior modeling endpoint"""
    prediction = predict_user_behavior(history, user_prefs)
    return {
        "prediction": prediction,
        "message": "User behavior predicted successfully"
    }

@app.post("/personalize/summarize")
def personalize_summary(req: Dict[str, Any]):
    content = req.get("content", "")
    user_prefs = req.get("user_prefs", {})
    ai_engagement = req.get("ai_engagement", {})
    ai_audience = req.get("ai_audience", {})
    
    prompt = f"""
    Summarize this content with insights from AI-predicted engagement analytics.
    
    USER PREFERENCES: {user_prefs}
    
    AI-PREDICTED ENGAGEMENT METRICS: {ai_engagement}
    AI-PREDICTED AUDIENCE INSIGHTS: {ai_audience}
    
    Based on these predictions, explain:
    1. Why this content is predicted to perform at this level
    2. What elements contribute to the predicted engagement
    3. Suggestions to improve engagement score
    
    Content: {content[:5000]}
    """
    result = call_gemini(prompt, "personalization")
    return {"summary": result}

@app.post("/personalize/adapt_tone")
def adapt_tone(content: str, target_tone: str):
    prompt = f"Rewrite this content to match a {target_tone} tone. Content: {content[:2000]}"
    result = call_gemini(prompt, "personalization")
    return {"adapted_content": result}

# 5. Ingestion Helpers
@app.post("/ingest/url")
async def ingest_url(url: str):
    res = ingest_client.ingest_url(url)
    return res

@app.post("/ingest/file")
async def ingest_file(file: UploadFile = File(...)):
    content = await file.read()
    res = ingest_client.ingest_file(file.filename, content, file.content_type)
    return res

@app.get("/cms/project/{folder}/{project_id}/compare")
def compare_versions(folder: str, project_id: str, v1: str, v2: str):
    import difflib
    history = cms.get_history(folder, project_id)
    content1 = next((v['content'] for v in history if v['version_id'] == v1), None)
    content2 = next((v['content'] for v in history if v['version_id'] == v2), None)
    
    if content1 is None or content2 is None:
        raise HTTPException(status_code=404, detail="Version not found")
    
    diff = list(difflib.unified_diff(content1.splitlines(), content2.splitlines()))
    return {"diff": diff}

if __name__ == "__main__":
    print("🚀 Content OS API is starting...")
    print("📝 Access Swagger UI at: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)
