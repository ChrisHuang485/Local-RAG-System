import config
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever, ContextualCompressionRetriever, ParentDocumentRetriever
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredPowerPointLoader
from langchain_ollama import ChatOllama
from langchain_classic.chains import RetrievalQA
from langchain_classic.storage import InMemoryStore
from langchain_classic.prompts import PromptTemplate

class RAGPipeline:
    def __init__(self):
        self.embedding_model = None
        self.llm = None
        self.reranker = None

    def initialize_models(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL_PATH,
            model_kwargs={'device': 'cpu'}, 
            encode_kwargs={'normalize_embeddings': True}
        )

        self.llm = ChatOllama(model=config.LLM_MODEL_NAME, temperature=0)
        self.reranker = HuggingFaceCrossEncoder(model_name=config.RERANKER_MODEL_PATH)

    def build_chain(self, documents, user_prompt_req="None"):
        if not documents:
            raise ValueError("No documents provided to build index.")
        
        parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE_PARENT, 
            chunk_overlap=config.CHUNK_OVERLAP_PARENT
        )
        child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE_CHILD, 
            chunk_overlap=config.CHUNK_OVERLAP_CHILD
        )

        vectorstore = Chroma(
            collection_name="split_parents",
            embedding_function=self.embedding_model,
            #persist_directory="./chroma_db_parent"
        )
        store = InMemoryStore()

        retriever_parent = ParentDocumentRetriever(
            vectorstore=vectorstore,
            docstore=store,
            child_splitter=child_splitter,
            parent_splitter=parent_splitter,
            search_kwargs={"k": config.SEARCH_K}
        )
        retriever_parent.add_documents(documents)

        bm25_docs = parent_splitter.split_documents(documents)
        retriever_bm25 = BM25Retriever.from_documents(bm25_docs)
        retriever_bm25.k = config.SEARCH_K

        ensemble_retriever = EnsembleRetriever(
            retrievers=[retriever_bm25, retriever_parent],
            weights=[0.2, 0.8]
        )

        compressor = CrossEncoderReranker(model=self.reranker, top_n=config.TOP_N)

        final_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=ensemble_retriever
        )

        prompt = PromptTemplate(
            template=config.DEFAULT_SYSTEM_PROMPT,
            input_variables=["context", "question"],
            partial_variables={"user_req": user_prompt_req}
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=final_retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )

        return qa_chain