from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import Config


class VectorDBManager:
    def __init__(self):
        self.embedding_function = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL)

        self.client = QdrantClient(path=Config.QDRANT_PATH)

        if not self.client.collection_exists(Config.COLLECTION_NAME):
            self.client.create_collection(
                collection_name=Config.COLLECTION_NAME,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
            print(f"Collection '{Config.COLLECTION_NAME}' created.")

        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=Config.COLLECTION_NAME,
            embedding=self.embedding_function
        )

    def ingest_document(self, file_path: str):
        loader = TextLoader(file_path, encoding="utf-8")
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(documents)

        self.vector_store.add_documents(chunks)
        print(f"Successfully ingested {len(chunks)} chunks into Qdrant.")

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": Config.RETRIEVER_K})