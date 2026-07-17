import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Fetch all docs for this user
res = supabase.table("documents").select("id, title, category, embedding").execute()
print("Found docs:", len(res.data))
if len(res.data) > 0:
    for d in res.data:
        has_emb = d.get('embedding') is not None
        print(f"- {d['id']} | Title: {d['title']} | Has Embedding: {has_emb}")
