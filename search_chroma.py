import chromadb
from ollama import embed

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

# Get collection
collection = client.get_collection(
    name="knowledge"
)

# Get user question
query = input("Ask a question: ")

# Create embedding for the question
response = embed(
    model="nomic-embed-text",
    input=query
)

query_embedding = response["embeddings"][0]

# Search ChromaDB
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,
    include=["documents", "distances"]
)

# Display results with distances
print("\nTop relevant chunks:")

for i, document in enumerate(results["documents"][0]):
    distance = results["distances"][0][i]

    print(f"\n--- Rank {i + 1} ---")
    print("Distance:", distance)
    print("Document:")
    print(document)