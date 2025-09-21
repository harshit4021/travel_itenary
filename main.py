#!/usr/bin/env python3
"""
Main entry point for the AI-Powered Trip Planner application.
Run this file to start the FastAPI server.
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🌍 Starting AI-Powered Trip Planner...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/api/docs")
    print("🎯 Frontend Interface: http://localhost:8000")
    
    uvicorn.run(
        "app.main:app",  # Import string instead of app object
        host="0.0.0.0", 
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
