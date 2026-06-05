import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Import the original app instance robustly from app.main or main
try:
    from app.main import app
except ModuleNotFoundError:
    from main import app

# Define path to frontend UI file (sibling directory 'static/')
FRONTEND_PATH = Path(__file__).resolve().parent / "static" / "index.html"

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    if not FRONTEND_PATH.exists():
        return HTMLResponse(
            """
            <html>
                <head>
                    <title>Error</title>
                    <style>
                        body { background: #f0f4f9; color: #ef4444; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                        div { text-align: center; border: 1px solid #ef4444; padding: 2rem; border-radius: 16px; background: rgba(239,68,68,0.05); }
                    </style>
                </head>
                <body>
                    <div>
                        <h2>UI Dashboard File Missing</h2>
                        <p>The UI file <code>app/static/index.html</code> was not found.</p>
                    </div>
                </body>
            </html>
            """, 
            status_code=404
        )
    with open(FRONTEND_PATH, "r", encoding="utf-8") as f:
        return f.read()
