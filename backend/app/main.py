from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
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
# CORS (Frontend access)
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Later restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Health Check
# -----------------------
@app.get("/")
def home():
    return {"message": "🚀 Auto Job Apply Backend Running Successfully!"}

# -----------------------
# Register API Routers
# -----------------------
app.include_router(users_router)
app.include_router(skills_router)
app.include_router(jobs_router)
app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
