# app/main.py

from pathlib import Path
from io import BytesIO

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from PyPDF2 import PdfReader

from app.models import GraphResponse
from app.llama_utils import extract_graph_from_text

# === Resolve project root & static dir ===
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI()

# === CORS (allow all for dev) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Serve your frontend ===
@app.get("/")
async def serve_frontend():
    return FileResponse(STATIC_DIR / "index.html")

# === Mount static assets ===
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# === API: extract graph ===
@app.post("/api/extract-graph", response_model=GraphResponse)
async def extract_graph(file: UploadFile = File(...)):
    # 1) Read raw bytes
    raw = await file.read()

    # 2) Extract text
    if file.content_type == "application/pdf":
        reader = PdfReader(BytesIO(raw))
        pages = [pg.extract_text() or "" for pg in reader.pages]
        text = "\n".join(pages)
    else:
        text = raw.decode("utf-8", errors="ignore")

    # 3) Basic sanity check
    if len(text) < 10:
        raise HTTPException(status_code=400, detail="Document too short")

    # 4) Call your LLM-based extractor
    try:
        graph = extract_graph_from_text(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {e}")

    # 5) Post-process nodes: ensure every node has a label
    for node in graph.get("nodes", []):
        if not node.get("label"):
            node["label"] = node.get("id", "")

    # 6) Post-process edges: ensure every edge has a label
    for edge in graph.get("edges", []):
        if not edge.get("label"):
            edge["label"] = edge.get("type", "")

    return graph
