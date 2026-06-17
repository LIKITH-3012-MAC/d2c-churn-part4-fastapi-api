import sys
from pathlib import Path

# Add root directory to sys.path so app module is importable
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

if __name__ == "__main__":
    import uvicorn
    print("Starting ChurnLens AI unified server...")
    print("Dashboard will be available at http://127.0.0.1:8000")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
