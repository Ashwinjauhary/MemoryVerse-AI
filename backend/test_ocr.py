import pytesseract
from PIL import Image
import io
import os

tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    print("Found Tesseract at:", tesseract_path)
else:
    print("Tesseract NOT found at:", tesseract_path)

# test with a dummy image (a solid white square)
img = Image.new('RGB', (100, 100), color = 'white')
try:
    text = pytesseract.image_to_string(img)
    print("OCR works! Extracted text:", repr(text))
except Exception as e:
    print("OCR Error:", e)
