import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client_groq = Groq(api_key=os.environ["GROQ_API_KEY"])

def generate_answer(context_chunks: list[str], question: str) -> str:
    context = "\n\n".join(context_chunks)
    prompt = f"""Foloseste DOAR informatiile din contextul de mai jos ca sa raspunzi la intrebare.
Daca raspunsul nu se gaseste in context, spune ca nu ai suficiente informatii.

Context:
{context}

Intrebare: {question}

Raspuns:"""

    response = client_groq.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content