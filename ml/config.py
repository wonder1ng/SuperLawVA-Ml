"""
[config.py]
- .env 에서 민감·가변 값을 읽어오고
- 경로·고정 상수는 여기에서 일괄 관리
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ───────────────────────────────────────────
# 기본 경로
# ───────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")  # .env 로드

# ───────────────────────────────────────────
# API KEY (민감 정보)
# ───────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY")

# ───────────────────────────────────────────
# 서버 설정
# ───────────────────────────────────────────
HOST   = os.getenv("HOST", "127.0.0.1")
PORT   = int(os.getenv("PORT", 8000))
RELOAD = os.getenv("RELOAD", "false").lower() == "true"

# ───────────────────────────────────────────
# 벡터 DB 경로 (고정 경로 → 여기서만 관리)
# ───────────────────────────────────────────
# 벡터DB 루트 경로: src/vectordb/
VDB_ROOT = BASE_DIR / "src" / "vectordb"

# 각각의 DB 경로 지정
CHROMA_LAW_DB_PATH  = VDB_ROOT / "chroma_law" / "chroma_openai_law"
CHROMA_CASE_DB_PATH = VDB_ROOT / "chroma_case" / "chroma_openai_case"

# 예: loaders 디렉토리 경로도 필요하면
VECTOR_LOADER_PATH = VDB_ROOT / "loaders"

# ───────────────────────────────────────────
# 컬렉션 이름 (바꿀 일 거의 없음 → 하드코딩)
# ───────────────────────────────────────────
LAW_COLLECTION_NAME  = "law_chunks_openai"
CASE_COLLECTION_NAME = "case_chunks_openai"

# ___________________________________________
# 벡터 검색 및 기타 서비스에서 사용하는 상수들을 중앙 관리
# ___________________________________________
# 벡터 검색 관련 설정 - document_search.py
LAW_SEARCH_LIMIT = 5
CASE_SEARCH_LIMIT = 5
CASE_SCORE_THRESHOLD = 1.5
CASE_RESULT_LIMIT = 3

# ______________________________________
# 판례 내용 미리보기 길이 - document_search.py
CASE_CONTENT_PREVIEW_LENGTH = 500

#--------------------------------------
# 판례 처리 관련 설정 - case_processor.py
CASE_TEXT_MAX_LENGTH = 1000
CASE_SNIPPET_LENGTH = 300  
CASE_SUMMARY_PREVIEW_LENGTH = 100

# ───────────────────────────────────────────
# AI 모델 설정 (모델명만 .env, 나머진 고정)
# ───────────────────────────────────────────
CLAUDE_MODEL       = os.getenv("CLAUDE_MODEL")
CLAUDE_TEMPERATURE = 0.1
CLAUDE_MAX_TOKENS  = 4_000

# ───────────────────────────────────────────
# 로깅·성능·검색·보안 등 고정 상수
# ───────────────────────────────────────────
LOG_LEVEL  = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

CORS_ORIGINS       = "*"
API_KEY_REQUIRED   = False

VECTOR_SEARCH_K    = 5
MAX_DISTANCE       = 1.5

REQUEST_TIMEOUT           = 60
MAX_CONCURRENT_REQUESTS   = 10

DEBUG     = False   # dev/prod 분기는 Docker-Compose override에서 처리 권장
TEST_MODE = False

# ───────────────────────────────────────────
# 프로젝트 메타 정보
# ───────────────────────────────────────────
APP_NAME    = "계약서 특약사항 생성 API"
APP_VERSION = "1.0.0"

# ───────────────────────────────────────────
# 추가로 자주 쓰는 고정 상수 예시
# ───────────────────────────────────────────
SUPPORTED_MODELS       = ["gpt-4o", CLAUDE_MODEL]
DEFAULT_RESPONSE_TYPE  = "json"
