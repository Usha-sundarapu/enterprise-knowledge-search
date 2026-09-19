import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=api_key
)


def generate_rag_answer(query, search_results):

    context_parts = []

    for result in search_results:

        context_parts.append(
            f"""
Source: {result["source"]}
Chunk: {result["chunk_index"]}

Content:
{result["content"]}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
You are an Enterprise Knowledge Assistant.

Answer the user's question using ONLY the information
provided in the retrieved context.

Do not invent information.
Do not use outside knowledge.

If the answer cannot be found in the context,
respond that the information is not available
in the provided documents.

User Question:
{query}

Retrieved Context:
{context}

Provide a clear and concise answer.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text