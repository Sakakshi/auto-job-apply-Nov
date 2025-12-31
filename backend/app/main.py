from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.users import router as users_router
from backend.app.api.skills import router as skills_router
from backend.app.api.jobs import router as jobs_router
from backend.app.api.auth import router as auth_router
from backend.app.api.resume import router as resume_router

app = FastAPI(
    title="Auto Job Apply API",
    version="1.0.0",
    description="Backend for automated job application platform"
)

# -----------------------
# CORS
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Health check
# -----------------------
@app.get("/")
def home():
    return {"message": "🚀 Auto Job Apply Backend Running Successfully!"}

# -----------------------
# API ROUTES
# -----------------------
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(skills_router, prefix="/skills", tags=["Skills"])
app.include_router(jobs_router, prefix="/jobs", tags=["Jobs"])
app.include_router(resume_router, prefix="/resume", tags=["Resume"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
