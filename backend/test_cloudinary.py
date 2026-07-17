import os
import requests
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
  cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
  api_key = os.getenv('CLOUDINARY_API_KEY'),
  api_secret = os.getenv('CLOUDINARY_API_SECRET')
)

# create a dummy PDF
pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n188\n%%EOF"

# Test raw
res_raw = cloudinary.uploader.upload(pdf_content, resource_type="raw", public_id="test_raw.pdf")
print("RAW URL:", res_raw['secure_url'])
req_raw = requests.head(res_raw['secure_url'])
print("RAW Content-Type:", req_raw.headers.get('Content-Type'))
print("RAW Content-Disposition:", req_raw.headers.get('Content-Disposition'))

# Test image
res_img = cloudinary.uploader.upload(pdf_content, resource_type="image", public_id="test_img.pdf")
print("IMG URL:", res_img['secure_url'])
req_img = requests.head(res_img['secure_url'])
print("IMG Content-Type:", req_img.headers.get('Content-Type'))
print("IMG Content-Disposition:", req_img.headers.get('Content-Disposition'))
