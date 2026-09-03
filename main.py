from fastapi import FastAPI, UploadFile, File
import shutil, uuid, os

from document_processor import extract_text_from_pdf, chunk_text
from vector_store import create_collection, add_chunks, search_similar
from rag_pipeline import generate_answer

app = FastAPI()

collections = {}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    doc_id = str(uuid.uuid4())
    temp_path = f"temp_{doc_id}.pdf"

    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = extract_text_from_pdf(temp_path)
    chunks = chunk_text(text)

    collection = create_collection(doc_id)
    add_chunks(collection, chunks)
    collections[doc_id] = collection

    os.remove(temp_path)

    return {"doc_id": doc_id, "numar_chunks": len(chunks)}

@app.post("/ask")
async def ask_question(doc_id: str, question: str):
    collection = collections.get(doc_id)
    if not collection:
        return {"eroare": "doc_id necunoscut. Fa upload la un PDF intai."}

    relevant_chunks = search_similar(collection, question)
    answer = generate_answer(relevant_chunks, question)

    return {"raspuns": answer, "surse": relevant_chunks}