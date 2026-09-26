import chromadb
from ollama import embed

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

# Remove old collection
try:
    client.delete_collection("knowledge")
    print("Old collection deleted.")
except:
    pass

# Create fresh collection
collection = client.create_collection(
    name="knowledge"
)

# Load document
with open("knowledge.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Split into paragraphs
paragraphs = [
    paragraph.strip()
    for paragraph in text.split("\n\n")
    if paragraph.strip()
]

# Hybrid chunking
max_chunk_size = 300

chunks = []
current_chunk = ""

for paragraph in paragraphs:

    if len(current_chunk) + len(paragraph) + 2 <= max_chunk_size:

        if current_chunk:
            current_chunk += "\n\n"

        current_chunk += paragraph

    else:

        if current_chunk:
            chunks.append(current_chunk)

        current_chunk = paragraph

# Add final chunk
if current_chunk:
    chunks.append(current_chunk)

print("Number of chunks:", len(chunks))

# Generate embeddings
response = embed(
    model="nomic-embed-text",
    input=chunks
)

embeddings = response["embeddings"]

# Create IDs
ids = [
    f"chunk_{i}"
    for i in range(len(chunks))
]

# Store in ChromaDB
collection.add(
    ids=ids,
    documents=chunks,
    embeddings=embeddings
)

print("Documents stored successfully!")
print("Total documents in ChromaDB:", collection.count())

# Show stored chunks
for i, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {i} ---")
    print(chunk)