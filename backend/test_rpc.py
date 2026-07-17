import os
import asyncio
from dotenv import load_dotenv
load_dotenv()
from supabase import create_client
from services.embeddings import get_query_embedding

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Get any user id
users = supabase.table("documents").select("user_id").limit(1).execute()
if users.data:
    user_id = users.data[0]['user_id']
    print(f"Testing for user_id: {user_id}")
    query = "resume"
    emb = get_query_embedding(query)
    
    res = supabase.rpc("match_documents", {
        "query_embedding": emb,
        "match_user_id": user_id,
        "exclude_doc_id": "00000000-0000-0000-0000-000000000000",
        "match_count": 10,
        "match_threshold": 0.0
    }).execute()
    print("Threshold 0.0:", len(res.data), res.data)
else:
    print("No users found.")
