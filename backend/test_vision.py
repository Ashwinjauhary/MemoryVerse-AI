import os
import base64
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq()

# Create a small dummy image (1x1 transparent png)
img_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
data_url = f"data:image/png;base64,{img_b64}"

try:
    response = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What is in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": data_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=50,
    )
    print("Success:", response.choices[0].message.content)
except Exception as e:
    print("Error:", e)
