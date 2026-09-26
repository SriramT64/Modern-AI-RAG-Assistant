from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from ollama import embed, chat

app = FastAPI(title="Local RAG AI Assistant")

# ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="knowledge")


class QueryRequest(BaseModel):
    question: str


def generate_answer(query):
    # 1. Create query embedding
    embedding_response = embed(
        model="nomic-embed-text",
        input=query
    )

    query_embedding = embedding_response["embeddings"][0]

    # 2. Retrieve documents
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        include=["documents", "distances"]
    )

    documents = results["documents"][0]
    distances = results["distances"][0]

    # 3. Reranking
    query_words = set(query.lower().split())
    ranked = []

    for document, distance in zip(documents, distances):
        document_words = set(document.lower().split())

        overlap = len(query_words & document_words)

        score = overlap - distance

        ranked.append(
            (document, distance, overlap, score)
        )

    ranked.sort(
        key=lambda x: x[3],
        reverse=True
    )

    # 4. Select top chunks
    top_chunks = ranked[:3]

    # 5. Relevance threshold
    best_score = top_chunks[0][3]

    if best_score < 0:
        return {
            "answer": "I don't know based on the available documents.",
            "sources": []
        }

    # 6. Build context
    context = "\n\n".join(
        item[0]
        for item in top_chunks
    )

    # 7. Prompt LLM
    prompt = f"""
You are a helpful AI assistant.

Answer the user's question using ONLY the provided context.

Do not invent information.

If the answer cannot be found in the context, say:

"I don't know based on the available documents."

Context:
{context}

Question:
{query}

Answer:
"""

    # 8. Generate answer
    response = chat(
        model="qwen2.5-coder:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.message.content

    # 9. Return answer + source chunks
    return {
        "answer": answer,
        "sources": [
            item[0]
            for item in top_chunks
        ]
    }


@app.get("/")
def home():
    return {
        "message": "Local RAG AI Assistant API is running"
    }


@app.post("/ask")
def ask(request: QueryRequest):

    result = generate_answer(
        request.question
    )

    return result