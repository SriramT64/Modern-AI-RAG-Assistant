import chromadb
from ollama import embed, chat

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection(
    name="knowledge"
)

# Conversation memory
conversation_history = []

print("🤖 RAG Assistant started!")
print("Type 'exit' to stop.\n")


while True:

    # Get question
    query = input("You: ")

    if query.lower().strip() == "exit":
        print("Goodbye! 👋")
        break

    # Create query embedding
    embedding_response = embed(
        model="nomic-embed-text",
        input=query
    )

    query_embedding = embedding_response["embeddings"][0]

    # Retrieve more candidates
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        include=["documents", "distances"]
    )

    documents = results["documents"][0]
    distances = results["distances"][0]

    # Query words
    query_words = set(query.lower().split())

    # Rerank candidates
    ranked = []

    for document, distance in zip(documents, distances):

        document_words = set(document.lower().split())

        overlap = len(query_words & document_words)

        # Simple reranking score
        score = overlap - distance

        ranked.append(
            (document, distance, overlap, score)
        )

    # Highest score first
    ranked.sort(
        key=lambda x: x[3],
        reverse=True
    )

    # Select best 3 chunks
    top_chunks = ranked[:3]
    # Relevance check
    best_score = top_chunks[0][3]

    if best_score < 0:
        print("\nAI: I don't know based on the available documents.\n")
        conversation_history.append(
            "AI: I don't know based on the available documents."
        )
        continue

    retrieved_chunks = [
        item[0]
        for item in top_chunks
    ]

    # Combine chunks into context
    context = "\n\n".join(retrieved_chunks)

    # Add user message to memory
    conversation_history.append(
        f"User: {query}"
    )

    recent_history = "\n".join(
        conversation_history[-6:]
    )

    # RAG prompt
    prompt = f"""
You are a helpful AI assistant.

Answer the user's question using ONLY the provided context.

Use the conversation history to understand follow-up questions.

Do not invent information.

If the answer cannot be found in the context, say:

"I don't know based on the available documents."

Conversation history:
{recent_history}

Context:
{context}

Current question:
{query}

Answer:
"""

    # Generate streaming response
    print("\nAI: ", end="", flush=True)

    response = chat(
        model="qwen2.5-coder:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True
    )

    answer = ""

    # Stream the answer
    for chunk in response:

        text = chunk.message.content

        if text:
            print(text, end="", flush=True)
            answer += text

    # Finished streaming
    print("\n")

    # Save AI response
    conversation_history.append(
        f"AI: {answer}"
    )