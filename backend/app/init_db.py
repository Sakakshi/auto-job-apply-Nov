from backend.app.db import engine, Base
from backend.app.models import models

print("🚀 Creating tables in PostgreSQL...")

Base.metadata.create_all(bind=engine)

print("✅ All tables created successfully!")