import asyncio
import httpx

async def test_flow():
    base_url = "http://127.0.0.1:8000/api"
    user_id = "00000000-0000-0000-0000-000000000001" # dummy user id
    
    async with httpx.AsyncClient() as client:
        print("1. Testing Upload (URL)")
        try:
            res = await client.post(
                f"{base_url}/documents/upload", 
                data={"user_id": user_id, "url": "https://www.python.org/about/"},
                timeout=30.0
            )
            print(f"Upload Status: {res.status_code}")
            if res.status_code == 200:
                print(f"Upload Response: {res.json()}")
            else:
                print(f"Upload Error: {res.text}")
        except Exception as e:
            print(f"Upload exception: {e}")

        print("\n2. Testing Timeline")
        try:
            res = await client.get(f"{base_url}/timeline/{user_id}")
            print(f"Timeline Status: {res.status_code}")
            if res.status_code == 200:
                print(f"Timeline Response: {res.json()}")
            else:
                print(f"Timeline Error: {res.text}")
        except Exception as e:
            print(f"Timeline exception: {e}")

        print("\n3. Testing Search")
        try:
            res = await client.post(
                f"{base_url}/search",
                json={"user_id": user_id, "query": "Python"}
            )
            print(f"Search Status: {res.status_code}")
            if res.status_code == 200:
                print(f"Search Response: {res.json()}")
            else:
                print(f"Search Error: {res.text}")
        except Exception as e:
            print(f"Search exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_flow())
