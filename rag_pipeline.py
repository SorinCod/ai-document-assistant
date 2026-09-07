import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client_groq = Groq(api_key=os.environ["GROQ_API_KEY"])

def generate_answer(context_chunks: list[str], question: str) -> str:
    context = "\n\n".join(context_chunks)
    prompt = f"""Use ONLY the information from the context below to answer the question.
If the answer is not found in the context, say that you don't have enough information.

Context:
{context}

Question: {question}

Answer:"""

    response = client_groq.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content