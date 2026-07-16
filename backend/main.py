from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ingestion, timeline, search

app = FastAPI(title="MemoryVerse AI Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingestion.router)
app.include_router(timeline.router)
app.include_router(search.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to MemoryVerse AI Backend", "version": "1.0.0"}
