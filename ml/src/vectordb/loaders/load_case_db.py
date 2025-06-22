
"""
[load_case_db.py] - 판례 벡터DB 로딩 모듈

OpenAI 임베딩 모델을 기반으로 Chroma 벡터스토어를 불러옵니다.
외부에서 `load_case_vectorstore()` 함수를 import해 사용하세요.
"""
from config import (
    OPENAI_API_KEY,
    CHROMA_CASE_DB_PATH,
    CASE_COLLECTION_NAME,
)
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

def load_case_vectorstore():
    # 💡 OpenAI 임베딩 모델 설정
    embedding_model = OpenAIEmbeddings(
        model="text-embedding-3-large",
        openai_api_key=OPENAI_API_KEY
    )

    # 💡 Chroma 벡터 DB 로드
    vectorstore = Chroma(
        persist_directory=str(CHROMA_CASE_DB_PATH),
        embedding_function=embedding_model,
        collection_name=CASE_COLLECTION_NAME
    )

    return vectorstore
