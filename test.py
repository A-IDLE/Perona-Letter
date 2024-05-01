from embeddings import embedding_data, embed_docs
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from vector_database import load_cached_db
from retriever import load_bm25_retriever, load_faiss_retriever, load_ensemble_retriever
from langchain_openai import OpenAIEmbeddings
from vector_database import load_vector_db, load_cached_db
from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers import EnsembleRetriever
import os
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore



 # 환경변수들 불러오기
load_dotenv()
vector_db_path = os.getenv('VECTOR_DB_PATH')  # vector db 의 경로
DB_INDEX = os.getenv('DB_INDEX')  # db index 이름
CACHE_DB_INDEX = os.getenv('CACHE_DB_INDEX')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL') #  embedding 모델
embeddings_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)
path = "/Users/user/Documents/aix4/dev/practice/demo/data"

load_dotenv()
vector_db_path = os.getenv('VECTOR_DB_PATH')  # vector db 의 경로
CACHE_DB_INDEX = os.getenv('CACHE_DB_INDEX')  # db index 이름
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL') #  embedding 모델

db = load_cached_db()

retriever = load_ensemble_retriever(path)
docs = retriever.invoke("Harry Potter was very angry")
# 전체 검색 결과를 출력합니다.
print(docs)
# 문서의 개수를 출력합니다.
print(f"문서의 개수: {len(docs)}")

