import chromadb
from sentence_transformers import SentenceTransformer

# modèle gratuit
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)


def add_chunks(chunks, document_name):
    for i, chunk in enumerate(chunks):

        embedding = embedding_model.encode(
            chunk
        ).tolist()

        collection.add(
            ids=[f"{document_name}_{i}"],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[
                {
                    "document": document_name,
                    "chunk_id": i
                }
            ]
        )

def search_chunks(query, n_results=3):

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results["documents"][0]
