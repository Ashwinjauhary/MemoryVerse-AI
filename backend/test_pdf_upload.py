import os
import requests
import cloudinary.uploader
import config
from config import supabase

print("Starting PDF migration to 'image' resource type...")
res = supabase.table('documents').select('id, file_url, title').eq('file_type', 'pdf').like('file_url', '%/raw/upload/%').execute()
docs = res.data

if not docs:
    print("No PDFs found with /raw/upload/")
else:
    for doc in docs:
        try:
            print(f"\nProcessing {doc['title']} ({doc['id']})")
            pdf_url = doc['file_url']
            print(f"Downloading from: {pdf_url}")
            
            # Download PDF
            req = requests.get(pdf_url)
            file_bytes = req.content
            
            # Upload as image
            # We want to maintain a clean filename, without query params or weird path
            filename = pdf_url.split('/')[-1]
            if '?' in filename:
                filename = filename.split('?')[0]
                
            base_name = os.path.splitext(filename)[0]
            pub_id = f"{base_name}.pdf"
            
            print(f"Uploading as image to Cloudinary... (public_id: {pub_id})")
            result = cloudinary.uploader.upload(
                file_bytes,
                folder="memoryverse",
                resource_type="image",
                public_id=pub_id,
                overwrite=True,
            )
            new_url = result["secure_url"]
            print(f"New URL: {new_url}")
            
            # Update Supabase
            print("Updating Supabase...")
            supabase.table('documents').update({'file_url': new_url}).eq('id', doc['id']).execute()
            print("Done!")
            
        except Exception as e:
            print(f"Failed to process {doc['id']}: {e}")

print("\nMigration complete.")
