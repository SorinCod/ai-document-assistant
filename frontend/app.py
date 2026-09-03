import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("AI Document Assistant")

if "doc_id" not in st.session_state:
    st.session_state.doc_id = None

uploaded_file = st.file_uploader("Incarca un PDF", type="pdf")

if uploaded_file is not None and st.session_state.doc_id is None:
    with st.spinner("Procesez documentul..."):
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        response = requests.post(f"{API_URL}/upload", files=files)

        if response.status_code == 200:
            data = response.json()
            st.session_state.doc_id = data["doc_id"]
            st.success(f"Document procesat! ({data['numar_chunks']} chunk-uri)")
        else:
            error_detail = response.json().get("detail", "A aparut o eroare necunoscuta.")
            st.error(error_detail)

if st.session_state.doc_id is not None:
    question = st.text_input("Pune o intrebare despre document:")

    if question:
        with st.spinner("Caut raspunsul..."):
            response = requests.post(
                f"{API_URL}/ask",
                params={"doc_id": st.session_state.doc_id, "question": question}
            )

        if response.status_code == 200:
            data = response.json()
            st.write(data["raspuns"])

            with st.expander("Vezi sursele folosite"):
                for i, sursa in enumerate(data["surse"]):
                    st.markdown(f"**Sursa {i+1}:**")
                    st.text(sursa)
                    st.divider()
        else:
            error_detail = response.json().get("detail", "A aparut o eroare necunoscuta.")
            st.error(error_detail)