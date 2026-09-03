# AI Document Assistant

Aplicatie RAG (Retrieval-Augmented Generation) care permite incarcarea unui document PDF si punerea de intrebari despre continutul lui, cu raspunsuri generate de un LLM pe baza informatiilor gasite semantic in document.

## Arhitectura

PDF Upload -> Extract text (pypdf) -> Chunking (LangChain)
-> Embeddings (sentence-transformers, multilingv) -> ChromaDB
-> [Intrebare] -> Semantic search -> Context + Prompt -> Groq LLM -> Raspuns

## Stack tehnologic

- **Backend**: Python, FastAPI
- **Procesare text**: pypdf, langchain-text-splitters
- **Embeddings**: sentence-transformers (model multilingv)
- **Vector database**: ChromaDB
- **LLM**: Groq API (openai/gpt-oss-120b)
- **Frontend**: Streamlit

## Instalare

Creeaza si activeaza un mediu virtual, apoi instaleaza pachetele:

    python -m venv venv
    source venv/Scripts/activate
    pip install -r requirements.txt

Creeaza un fisier `.env` in radacina proiectului, cu urmatorul continut:

    GROQ_API_KEY=cheia_ta_aici

## Rulare

Porneste backend-ul (intr-un terminal):

    uvicorn main:app --reload

Porneste frontend-ul (in alt terminal):

    cd frontend
    streamlit run app.py

Aplicatia va fi disponibila la `http://localhost:8501`.

## Functionalitati

- Upload de documente PDF
- Extragere si segmentare (chunking) automata a textului
- Cautare semantica prin embeddings, nu doar potrivire de cuvinte cheie
- Generare de raspunsuri contextuale, bazate strict pe continutul documentului

## Structura proiectului

    ai-document-assistant/
    ├── main.py                  # Endpoint-uri FastAPI
    ├── document_processor.py    # Extragere PDF + chunking
    ├── vector_store.py          # Logica ChromaDB + embeddings
    ├── rag_pipeline.py          # Prompt + apel catre Groq
    ├── requirements.txt
    ├── .env                     # Cheia API (nu se urca pe GitHub)
    └── frontend/
        └── app.py               # Interfata Streamlit
