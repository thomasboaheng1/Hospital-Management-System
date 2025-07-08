#!/usr/bin/env python3
"""
Development startup script for Hospital Management System
"""

import uvicorn
import os
import sys
from pathlib import Path

def main():
    """Start the development server"""
    print("🏥 Starting Hospital Management System...")
    
    # Check if we're in the right directory
    if not Path("app/main.py").exists():
        print("❌ Error: app/main.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Set development environment
    os.environ.setdefault("DEBUG", "true")
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 