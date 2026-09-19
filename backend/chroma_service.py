import chromadb
import uuid

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="enterprise_documents"
)


def store_chunks(chunks, embeddings, filename):

    ids = [str(uuid.uuid4()) for _ in chunks]

    metadatas = []

    for index in range(len(chunks)):
        metadatas.append({
            "filename": filename,
            "chunk_index": index
        })

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )

    return "Stored Successfully"


def search_chunks(query_embedding, n_results=5):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    return results