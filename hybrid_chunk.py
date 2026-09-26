# Load document
with open("knowledge.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Split into paragraphs
paragraphs = [
    paragraph.strip()
    for paragraph in text.split("\n\n")
    if paragraph.strip()
]

max_chunk_size = 300

chunks = []
current_chunk = ""

for paragraph in paragraphs:

    # If adding the paragraph stays within the limit
    if len(current_chunk) + len(paragraph) + 2 <= max_chunk_size:

        if current_chunk:
            current_chunk += "\n\n"

        current_chunk += paragraph

    else:
        # Save current chunk
        if current_chunk:
            chunks.append(current_chunk)

        # Start a new chunk
        current_chunk = paragraph

# Save final chunk
if current_chunk:
    chunks.append(current_chunk)


print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {i} ---")
    print(chunk)
    print("Characters:", len(chunk))