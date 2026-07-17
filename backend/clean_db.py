from config import supabase

res = supabase.table('documents').select('id, file_url').execute()
for doc in res.data:
    url = doc['file_url']
    if url and '.pdf' in url.lower() and '/image/upload' in url:
        print(f"Deleting broken old PDF: {url}")
        # Delete related relationships first to avoid FK constraint error
        supabase.table('relationships').delete().eq('source_doc_id', doc['id']).execute()
        supabase.table('relationships').delete().eq('target_doc_id', doc['id']).execute()
        # Delete document
        supabase.table('documents').delete().eq('id', doc['id']).execute()
print("Cleanup complete!")
