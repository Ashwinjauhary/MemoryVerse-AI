# MemoryVerse AI
**Your Digital Identity, Unscattered.**

## Problem Statement
Students and professionals today suffer from a scattered digital footprint—certificates, resumes, event passes, and project reports pile up across Google Drive, local folders, and emails. There is no easy way to see the connections between these achievements or retrieve them contextually. MemoryVerse AI solves this by transforming isolated files into a structured, searchable spatial knowledge repository.

## Features
- **Ingestion:** Seamlessly extracts text from uploaded PDFs and images using PyMuPDF and Tesseract OCR, while simultaneously storing the original assets securely in Cloudinary.
- **Categorization:** Employs advanced LLMs to automatically parse document text, determine the best category (e.g., Certificate, Resume, Project), and extract a rich, structured JSON summary.
- **Relationship Engine:** Automatically discovers hidden links between your documents (e.g., connecting a Hackathon Certificate to a Project Report) using vector similarity and LLM-verified relationship labeling.
- **Timeline:** Automatically plots all your uploaded documents chronologically on a beautiful, interactive timeline, visually mapping out your educational and professional journey over time.
- **Smart Search:** Allows you to query your entire document history using natural language semantic search, instantly retrieving the most conceptually relevant documents even if keywords don't perfectly match.

## Tech Stack
![Next.js](https://img.shields.io/badge/Next.js-black?style=for-the-badge&logo=next.js&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/pgvector-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-f55036?style=for-the-badge&logo=groq&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)

- **Frontend:** Next.js (App Router, Tailwind CSS, Lucide Icons)
- **Backend:** FastAPI (Python)
- **Database:** Supabase (Postgres + pgvector)
- **LLM:** Groq API (`llama-3.3-70b-versatile`)
- **Embeddings:** HuggingFace `sentence-transformers` (`all-MiniLM-L6-v2`)
- **Storage & OCR:** Cloudinary (Asset Storage), Tesseract OCR & PyMuPDF (Text Extraction)

## Architecture Overview
MemoryVerse AI uses a modern decoupled architecture. The Next.js frontend provides a fluid, spatial glassmorphism UI that communicates securely with the FastAPI backend via JWT-authenticated REST endpoints. When documents are ingested, they are processed through an intelligent pipeline consisting of OCR extraction, LLM categorization, and local embedding generation before being stored in a Supabase pgvector database, where the Relationship Engine constructs a knowledge graph. 

For a detailed visual breakdown of the data flow, please see the [Architecture Document](ARCHITECTURE.md).

## Setup Instructions

**Prerequisites:** Node.js (18+), Python (3.10+), and Tesseract OCR installed on your host machine.

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Ashwinjauhary/MemoryVerse-AI.git
   cd MemoryVerse-AI
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   python -m venv venv
   # Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup:**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Environment Variables:**
   Create `.env` in the `backend` folder and `.env.local` in the `frontend` folder using the variables listed in the section below.

5. **Database Initialization:**
   Run the Supabase SQL schema script provided in `backend/supabase_schema.sql` within your Supabase project's SQL editor to set up the necessary tables, pgvector extensions, and RPC functions.

6. **Run the Application:**
   ```bash
   # Terminal 1 (Backend)
   cd backend
   uvicorn main:app --reload --port 8000
   
   # Terminal 2 (Frontend)
   cd frontend
   npm run dev
   ```
   Open `http://localhost:3000` in your browser.

## Environment Variables

### Backend (`backend/.env`)
| Variable | Description |
|----------|-------------|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_SERVICE_KEY` | Your Supabase service role key (required for backend auth/DB) |
| `GROQ_API_KEY` | API key for Groq to access Llama models |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name |
| `CLOUDINARY_API_KEY` | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret |
| `FRONTEND_URL` | Production URL of the frontend (e.g., https://memoryverse.vercel.app) for CORS |
| `TESSERACT_PATH` | (Optional) Path to tesseract executable if not in system PATH |

### Frontend (`frontend/.env.local`)
| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Your Supabase project URL (used for client-side auth/state) |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Your Supabase anon key |
| `NEXT_PUBLIC_API_URL` | URL of the deployed FastAPI backend (e.g. https://memoryverse-api.onrender.com) |

## API Endpoints

| Method | Path | Auth Required | Description |
|--------|------|---------------|-------------|
| POST | `/api/documents/upload` | Yes | Uploads a file, extracts text (OCR), stores in Cloudinary, categorizes via LLM, and saves to DB. |
| POST | `/api/documents/retry` | Yes | Retries categorization and embedding for documents that previously failed processing. |
| PUT | `/api/documents/{doc_id}` | Yes | Updates a document's metadata (Title, Summary, Category, Date) and triggers relationship re-mapping. |
| POST | `/api/documents/delete` | Yes | Deletes a document from the database and removes associated relationships. |
| POST | `/api/search` | Yes | Performs a semantic similarity search across user documents using pgvector. Accepts query string in request body. |
| GET | `/api/timeline/{path_user_id}` | Yes | Retrieves all user documents sorted chronologically for the timeline view. |

## Live Demo
*(Link to live deployment will be added here once deployed)*

## Known Limitations
- **Route Protection:** Frontend route protection currently relies on client-side state rather than server-side middleware.
- **OCR Dependency:** Tesseract OCR must be installed natively on the host machine running the backend server.
- **Relationship Processing Overhead:** Relationship generation currently runs synchronously during document upload, which can cause slight latency on large uploads.

## Team / Author
**Ashwin Jauhary**  
BCA Student, PSIT College of Higher Education
