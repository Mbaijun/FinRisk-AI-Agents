"""
Vercel Serverless Function Entry Point
This file MUST be named index.py for Vercel Python runtime
"""
import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    # Import the FastAPI app
    from api.main import app
    
    # Vercel handler
    def handler(request):
        # This will be handled by FastAPI/ASGI
        pass
        
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure requirements.txt is installed")
    raise
