from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from modules.knowledge_base import load_sample_clauses

class ClauseRetriever:
    def __init__(self, embedding_model="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(embedding_model)
        self.index = None
        self.clauses = []
        self.id_map = {}

    def build_index(self):
        self.clauses = load_sample_clauses()
        texts = [c["clause_text"] for c in self.clauses]
        embeddings = self.model.encode(texts)

        self.index = faiss.IndexFlatL2(len(embeddings[0]))
        self.index.add(np.array(embeddings))

        # Map FAISS indices to clause metadata
        for i, clause in enumerate(self.clauses):
            self.id_map[i] = clause

    def retrieve_similar(self, query_text, top_k=3):
        query_vec = self.model.encode([query_text])
        D, I = self.index.search(np.array(query_vec), top_k)
        return [self.id_map[i] for i in I[0]]
    
import streamlit as st

@st.cache_resource
def get_cached_retriever():
    from modules.retriever import ClauseRetriever
    retriever = ClauseRetriever()
    retriever.build_index()
    return retriever