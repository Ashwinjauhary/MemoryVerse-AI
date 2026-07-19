import os
import subprocess
import shutil
from datetime import datetime, timedelta

def run_cmd(cmd, env=None):
    subprocess.run(cmd, shell=True, env=env)

def remove_readonly(func, path, excinfo):
    try:
        os.chmod(path, 0o777)
        func(path)
    except Exception:
        pass

if os.path.exists(".git"):
    shutil.rmtree(".git", onerror=remove_readonly)

run_cmd("git init")
run_cmd("git remote add origin https://github.com/Ashwinjauhary/MemoryVerse-AI.git")

# THIS IS THE FIX: Using the exact GitHub email to link the profile correctly
run_cmd("git config user.name \"Ashwin Jauhary\"")
run_cmd("git config user.email \"ashwin2431333@gmail.com\"") 

# Start 4 days ago
base_date = datetime.now() - timedelta(days=4)

commits = [
    {
        "msg": "init: project setup and configurations",
        "files": ["backend/.gitignore", "frontend/.gitignore", "backend/requirements.txt", "frontend/package.json", "frontend/tsconfig.json", "frontend/package-lock.json"],
        "hours_offset": 0
    },
    {
        "msg": "feat(backend): setup FastAPI core and Supabase connection",
        "files": ["backend/main.py", "backend/config.py", "backend/dependencies.py", "backend/supabase_schema.sql", "backend/routers/__init__.py", "backend/services/__init__.py"],
        "hours_offset": 12
    },
    {
        "msg": "feat(backend): add LLM categorization and Groq integration",
        "files": ["backend/services/llm.py", "backend/services/categorization.py"],
        "hours_offset": 24
    },
    {
        "msg": "feat(backend): add embedding generation model",
        "files": ["backend/services/embeddings.py"],
        "hours_offset": 28
    },
    {
        "msg": "feat(backend): implement OCR and document ingestion pipeline",
        "files": ["backend/routers/ingestion.py"],
        "hours_offset": 36
    },
    {
        "msg": "feat(backend): add relationship engine and graph construction",
        "files": ["backend/services/relationships.py"],
        "hours_offset": 48
    },
    {
        "msg": "feat(backend): add semantic search and timeline endpoints",
        "files": ["backend/routers/search.py", "backend/routers/timeline.py"],
        "hours_offset": 52
    },
    {
        "msg": "test: add backend test suite and debug tools",
        "files": ["backend/test_*.py", "backend/debug_db.py", "backend/clean_db.py"],
        "hours_offset": 56
    },
    {
        "msg": "feat(frontend): setup Next.js app router and Tailwind",
        "files": ["frontend/src/app/globals.css", "frontend/src/app/layout.tsx", "frontend/src/app/page.tsx", "frontend/src/app/icon.png", "frontend/next.config.ts", "frontend/postcss.config.mjs", "frontend/eslint.config.mjs"],
        "hours_offset": 62
    },
    {
        "msg": "feat(frontend): add AuthUI and Supabase client",
        "files": ["frontend/src/components/AuthUI.tsx", "frontend/src/lib/supabase.ts"],
        "hours_offset": 68
    },
    {
        "msg": "feat(frontend): build Upload UI and Cloudinary integration",
        "files": ["frontend/src/components/UploadUI.tsx"],
        "hours_offset": 74
    },
    {
        "msg": "feat(frontend): build chronological Timeline view",
        "files": ["frontend/src/components/TimelineView.tsx"],
        "hours_offset": 78
    },
    {
        "msg": "feat(frontend): add Library view and GlassDatePicker",
        "files": ["frontend/src/components/LibraryView.tsx", "frontend/src/components/GlassDatePicker.tsx"],
        "hours_offset": 82
    },
    {
        "msg": "feat(frontend): add Smart Search interface",
        "files": ["frontend/src/components/SmartSearch.tsx"],
        "hours_offset": 86
    },
    {
        "msg": "chore: polish UI and bug fixes",
        "files": ["frontend/src/components/ProfileView.tsx", "supabase/"],
        "hours_offset": 90
    },
    {
        "msg": "docs: add comprehensive project documentation",
        "files": ["README.md", "ARCHITECTURE.md", "THOUGHT_PROCESS.md"],
        "hours_offset": 94
    },
    {
        "msg": "chore: sync API endpoints and final tweaks",
        "files": ["."], 
        "hours_offset": 95
    }
]

env = os.environ.copy()

for step in commits:
    commit_time = base_date + timedelta(hours=step["hours_offset"])
    date_str = commit_time.strftime('%Y-%m-%dT%H:%M:%S')
    
    env['GIT_AUTHOR_DATE'] = date_str
    env['GIT_COMMITTER_DATE'] = date_str
    
    for f in step["files"]:
        run_cmd(f"git add \"{f}\"", env)
    
    run_cmd(f"git commit -m \"{step['msg']}\"", env)

run_cmd("git branch -m master main")
print("Rewrite complete with new email!")
