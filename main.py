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
        raise HTTPException(status_code=400, detail="Doar fisiere PDF sunt acceptate.")

    doc_id = str(uuid.uuid4())
    temp_path = f"temp_{doc_id}.pdf"

    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        text = extract_text_from_pdf(temp_path)
    except Exception:
        os.remove(temp_path)
        raise HTTPException(status_code=400, detail="Nu am putut citi acest PDF. Fisierul poate fi corupt.")

    os.remove(temp_path)

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Nu am gasit text in acest PDF. Poate fi un document scanat (imagine)."
        )

    chunks = chunk_text(text)

    collection = create_collection(doc_id)
    add_chunks(collection, chunks)
    collections[doc_id] = collection

    return {"doc_id": doc_id, "numar_chunks": len(chunks)}

@app.post("/ask")
async def ask_question(doc_id: str, question: str):
    if not question.strip():
        raise HTTPException(status_code=400, detail="Intrebarea nu poate fi goala.")

    collection = collections.get(doc_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Documentul nu a fost gasit. Fa upload la un PDF intai.")

    relevant_chunks = search_similar(collection, question)

    try:
        answer = generate_answer(relevant_chunks, question)
    except Exception:
        raise HTTPException(status_code=503, detail="Serviciul de generare a raspunsurilor este momentan indisponibil. Incearca din nou in cateva momente.")

    return {"raspuns": answer, "surse": relevant_chunks}