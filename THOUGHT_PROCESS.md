# MemoryVerse AI - Thought Process

## 1. The Problem
During my college journey, I realized that students generate a massive amount of valuable digital artifacts: certificates, internship offer letters, resumes, and project reports. However, these documents are scattered across Google Drive, local folders, and emails. Existing cloud storage solutions (like Dropbox or Drive) just store files—they don't understand the **context** of a student's journey. It becomes incredibly difficult to connect a specific skill learned in 2023 to a project built in 2024 and an internship secured in 2025.

## 2. The Solution
I decided to build **MemoryVerse AI**, a system that shifts the paradigm from "cloud storage" to a "spatial digital identity." The goal was to build a zero-touch pipeline where a user simply drops a file, and AI handles the categorization, summarization, and, most importantly, the semantic relationship mapping.

## 3. Technology Choices & Architecture

### Frontend (Next.js & Tailwind CSS)
I chose Next.js for its fast rendering and solid routing capabilities. The UI was designed with a "glassmorphism" aesthetic to feel modern and spatial, reinforcing the idea that this is a premium digital archive, not just a file manager.

### Backend (FastAPI & Python)
Python was the obvious choice for the backend due to its unmatched ecosystem for AI and machine learning. FastAPI provides incredible performance and async support, which is critical when waiting for LLM and OCR operations.

### Data Ingestion (Tesseract OCR + Groq Llama-3)
Instead of relying on users to manually tag their documents, the system uses Tesseract OCR to extract raw text from images and PDFs. This raw text is sent to Groq's blazing-fast inference API running the `Llama-3.3-70b-versatile` model. The LLM is prompted to return structured JSON containing the document's title, category (Academics, Skills, Internships, etc.), date, and a concise summary.

### The Relationship Engine (HuggingFace + Supabase pgvector)
This is the core innovation of MemoryVerse AI. For every uploaded document, the system generates a 384-dimensional vector embedding using the `all-MiniLM-L6-v2` model from `sentence-transformers`. 

These embeddings are stored in Supabase using the `pgvector` extension. When a new document is ingested, the system performs a cosine similarity search against all existing documents. If the similarity score exceeds a strict threshold (0.65), a relationship is automatically formed. The LLM is then invoked to explain *why* these two documents are related (e.g., "The React certificate provides the foundational skill used in the E-Commerce project").

## 4. Key Challenges Overcome
* **Memory Limits on Deployment:** During deployment on Render's free tier, loading the PyTorch models for embeddings caused Out-of-Memory (OOM) crashes. I solved this by strictly installing the CPU-only version of PyTorch in the Dockerfile and tuning the memory allocator (`MALLOC_ARENA_MAX=2`).
* **Relationship Deduplication:** Initially, the system created duplicate bi-directional relationships (A->B and B->A). I optimized the backend logic to enforce a single direction and clear old relationships before re-indexing.

## 5. Future Roadmap
* **Auto-Resume Generation:** Using the connected timeline and relationship graph to automatically generate tailored resumes for specific job applications based on semantic matching.
* **Skill Gap Analysis:** Identifying missing skills based on the user's career goals and their current uploaded timeline.
