#!/usr/bin/env python3
"""
Database initialization script for Hospital Management System
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.core.database import engine
from app.models import Base
from app.core.config import settings

def init_database():
    """Initialize the database with tables"""
    print("🗄️ Initializing database...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Create uploads directory if it doesn't exist
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(exist_ok=True)
        print("✅ Uploads directory created!")
        
        print(f"📊 Database URL: {settings.DATABASE_URL}")
        print("🎉 Database initialization completed!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database() 