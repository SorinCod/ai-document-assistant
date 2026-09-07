from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil, uuid, os

from document_processor import extract_text_from_pdf, chunk_text
from vector_store import create_collection, add_chunks, search_similar
from rag_pipeline import generate_answer

app = FastAPI()

collections = {}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    doc_id = str(uuid.uuid4())
    temp_path = f"temp_{doc_id}.pdf"

    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        text = extract_text_from_pdf(temp_path)
    except Exception:
        os.remove(temp_path)
        raise HTTPException(status_code=400, detail="Could not read this PDF. The file might be corrupted.")

    os.remove(temp_path)

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No text found in this PDF. It might be a scanned document (image)."
        )

    chunks = chunk_text(text)

    collection = create_collection(doc_id)
    add_chunks(collection, chunks)
    collections[doc_id] = collection

    return {"doc_id": doc_id, "num_chunks": len(chunks)}

@app.post("/ask")
async def ask_question(doc_id: str, question: str):
    if not question.strip():
        raise HTTPException(status_code=400, detail="The question cannot be empty.")

    collection = collections.get(doc_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Document not found. Please upload a PDF first.")

    relevant_chunks = search_similar(collection, question)

    try:
        answer = generate_answer(relevant_chunks, question)
    except Exception:
        raise HTTPException(status_code=503, detail="The answer generation service is currently unavailable. Please try again in a few moments.")

    return {"answer": answer, "sources": relevant_chunks}