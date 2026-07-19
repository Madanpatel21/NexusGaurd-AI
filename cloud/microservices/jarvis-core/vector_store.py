# cloud/microservices/jarvis-core/vector_store.py
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, TextLoader
import os

class NexusGuardVectorStore:
    def __init__(self):
        self.persist_dir = "./data/vector_store"
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        if not os.path.exists(self.persist_dir):
            self._ingest_data()

        self.store = Chroma(persist_directory=self.persist_dir, embedding_function=self.embeddings)

    def _ingest_data(self):
        """Ingests 50k+ lines of code, docs, logs, and manuals."""
        loader = DirectoryLoader("./data/documents", glob="**/*.{md,txt,c,cpp,py,go,java,sql}")
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = text_splitter.split_documents(docs)

        self.store.add_documents(splits)
        self.store.persist()
        print(f"Ingested {len(splits)} chunks into Vector Store.")

    def similarity_search(self, query: str) -> str:
        docs = self.store.similarity_search(query, k=4)
        return "\n\n---\n\n".join([doc.page_content for doc in docs])
