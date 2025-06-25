"""
통합 main.py - AI 법률 서비스 API 서버
=====================================

Description:  
내용증명 생성, 계약서 검토, 특약사항 생성을 포함한 통합 AI 법률 서비스 FastAPI 앱
환경설정, 예외처리, CORS, 라우터 등록 및 헬스체크 포함

Author: ooheunsu  
Date: 2025-06-16  
Requirements: fastapi, uvicorn, python-dotenv, logging
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
# 벡터DB 로더들을 위한 경로 추가
sys.path.append(os.path.dirname(__file__))  # ml/ 디렉토리 추가

import logging
from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
# 추가 - 기존 유지
from config import ANTHROPIC_API_KEY  # 필수 키
from config import APP_VERSION  # 버전 문자열
from config import CORS_ORIGINS  # CORS 도메인 허용
from config import OPENAI_API_KEY  # 선택 키
from config import RELOAD  # 서버 실행 설정
from config import HOST, PORT
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# import os
from dotenv import load_dotenv


# 환경변수 로드
load_dotenv()

# 라우터 임포트
try:
    # 특약사항 생성 라우터

    # ml/src/routes/contract_terms_router.py
    from src.routes.contract_terms_router import router as contract_router
except ImportError:
    contract_router = None
    print("⚠️  contract_terms_router를 찾을 수 없습니다.")

try:
    # 내용증명 생성 라우터
    from src.routes.generate_letter import router as letter_router
except ImportError:
    letter_router = None
    print("⚠️  generate_letter router를 찾을 수 없습니다.")

try:
    # 계약서 검토 라우터
    from src.routes.analyze_contract import router as analyze_router
except ImportError:
    analyze_router = None
    print("⚠️  analyze_contract router를 찾을 수 없습니다.")

# 로깅 설정
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    앱 생명주기 관리
    - 시작 시: 필요한 초기화 작업
    - 종료 시: 리소스 정리
    """
    # 앱 시작 시
    logger.info("🚀 통합 AI 법률 서비스 시작")
    logger.info(f"📅 시작 시간: {datetime.now().isoformat()}")

    # 환경변수 검증
    missing_vars = []
    if not ANTHROPIC_API_KEY:
        missing_vars.append("ANTHROPIC_API_KEY")

    missing_optional = []
    if not OPENAI_API_KEY:
        missing_optional.append("OPENAI_API_KEY")

    if missing_vars:
        logger.error(f"❌ 필수 환경변수가 없습니다: {missing_vars}")
        raise HTTPException(
            status_code=500,
            detail=f"필수 환경변수가 설정되지 않았습니다: {missing_vars}",
        )

    if missing_optional:
        logger.warning(f"⚠️  선택적 환경변수가 없습니다: {missing_optional}")

    logger.info("✅ 환경변수 검증 완료")

    # 로드된 라우터 확인
    router_status = {
        "특약사항 생성": "✅" if contract_router else "❌",
        "내용증명 생성": "✅" if letter_router else "❌",
        "계약서 검토": "✅" if analyze_router else "❌",
    }

    for service, status in router_status.items():
        logger.info(f"{status} {service} 서비스")

    logger.info("✅ 통합 AI 법률 서비스 초기화 완료")

    yield

    # 앱 종료 시
    logger.info("🛑 통합 AI 법률 서비스 종료")


# FastAPI 앱 생성
app = FastAPI(
    title="🏛️ 통합 AI 법률 서비스 API v2",
    description="""
    ## 📋 통합 AI 법률 서비스
    
    **Claude Sonnet 4** 기반의 종합 법률 자동화 시스템으로, 
    임대차 전문 변호사의 25년 경력을 바탕으로 한 AI 법률 서비스입니다.
    
    ### 🎯 주요 서비스
    
    #### 1. 📝 내용증명 생성
    - **기능**: 임대차 관련 내용증명서 자동 생성
    - **특징**: 법적 근거와 판례 기반 문서 작성
    - **엔드포인트**: `/api/v1/generate-letter`
    
    #### 2. 🔍 계약서 검토 분석
    - **기능**: 임대차 계약서 조항별 위험도 분석
    - **특징**: RAG 기반 법령·판례 검색 및 분석
    - **엔드포인트**: `/api/v1/analyze-contract`
    
    #### 3. ⚖️ 특약사항 생성
    - **기능**: 임차인 중심의 맞춤형 특약 조건 제안
    - **특징**: 법령 근거 제시 및 협상 전략 제공
    - **엔드포인트**: `/api/v1/contract/generate-special-terms`
    
    ### 📊 공통 특징
    - **AI 모델**: Claude Sonnet 4 (최신 버전)
    - **전문 분야**: 임대차 계약 전문
    - **법적 근거**: 상세한 법령 해설 (조, 항, 호까지)
    - **판례 정보**: 관련 판례 요약과 분석
    - **실무 중심**: 25년 경력 변호사 페르소나
    
    ### 🔧 기술 스택
    - **프레임워크**: FastAPI + LangChain
    - **AI 엔진**: Claude Sonnet 4 API
    - **검증**: Pydantic 스키마
    - **검색**: RAG 기반 법령·판례 데이터베이스
    
    ### 📞 지원 정보
    - **문의**: contact@example.com
    - **문서**: 각 엔드포인트별 상세 API 문서 제공
    - **버전**: v1.0.0 (통합 버전)
    """,
    version=APP_VERSION,
    contact={
        "name": "통합 AI 법률 서비스",
        "email": "contact@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS.split(",") if CORS_ORIGINS != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
if letter_router:
    app.include_router(letter_router, prefix="/api/v1", tags=["📝 내용증명 생성"])

if analyze_router:
    app.include_router(analyze_router, prefix="/api/v1", tags=["🔍 계약서 검토"])

if contract_router:
    app.include_router(
        contract_router, prefix="/api/v1/contract", tags=["⚖️ 특약사항 생성"]
    )


# 루트 엔드포인트
@app.get("/", tags=["🏠 기본 정보"])
async def root():
    """
    통합 AI 법률 서비스 기본 정보 조회
    """
    # 활성화된 서비스 확인
    active_services = []
    if letter_router:
        active_services.append("📝 내용증명 생성")
    if analyze_router:
        active_services.append("🔍 계약서 검토")
    if contract_router:
        active_services.append("⚖️ 특약사항 생성")

    return {
        "service": "🏛️ 통합 AI 법률 서비스 API",
        "version": APP_VERSION,
        "description": "Claude Sonnet 4 기반 종합 법률 자동화 시스템",
        "specialist": "임대차 전문 (25년 경력 변호사 페르소나)",
        "ai_model": "Claude Sonnet 4",
        "active_services": active_services,
        "available_endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "detailed_health": "/health/detailed",
            "letter_generation": (
                "/api/v1/generate-letter" if letter_router else "❌ 비활성화"
            ),
            "contract_analysis": (
                "/api/v1/analyze-contract" if analyze_router else "❌ 비활성화"
            ),
            "special_terms": (
                "/api/v1/contract/generate-special-terms"
                if contract_router
                else "❌ 비활성화"
            ),
            "special_terms_health": (
                "/api/v1/contract/health" if contract_router else "❌ 비활성화"
            ),
            "special_terms_validate": (
                "/api/v1/contract/validate-input" if contract_router else "❌ 비활성화"
            ),
        },
        "features": [
            "📝 RAG 기반 내용증명 자동 생성",
            "🔍 계약서 조항별 위험도 분석",
            "⚖️ 임차인 중심 특약사항 제안",
            "📚 법령·판례 검색 및 해설",
            "💼 실무 중심 협상 전략 제공",
        ],
        "timestamp": datetime.now().isoformat(),
        "status": "🟢 정상 운영 중",
    }


# 헬스체크 엔드포인트들
@app.get("/health", tags=["🏥 모니터링"])
async def health_check():
    """
    기본 헬스체크 엔드포인트
    """
    return {
        "status": "healthy",
        "service": "unified-ai-legal-assistant",
        "timestamp": datetime.now().isoformat(),
        "version": APP_VERSION,
    }


@app.get("/health/detailed", tags=["🏥 모니터링"])
async def detailed_health_check():
    """
    상세 헬스체크 - 각 서비스별 상태 확인
    """
    service_health = {
        "내용증명_생성": {
            "status": "active" if letter_router else "inactive",
            "endpoint": "/api/v1/generate-letter" if letter_router else None,
            "description": "임대차 관련 내용증명서 자동 생성",
        },
        "계약서_검토": {
            "status": "active" if analyze_router else "inactive",
            "endpoint": "/api/v1/analyze-contract" if analyze_router else None,
            "description": "임대차 계약서 조항별 위험도 분석",
        },
        "특약사항_생성": {
            "status": "active" if contract_router else "inactive",
            "endpoint": (
                "/api/v1/contract/generate-special-terms" if contract_router else None
            ),
            "description": "임차인 중심의 맞춤형 특약 조건 제안",
        },
    }

    active_count = sum(
        1 for service in service_health.values() if service["status"] == "active"
    )

    return {
        "overall_status": "healthy" if active_count > 0 else "warning",
        "active_services": active_count,
        "total_services": len(service_health),
        "services": service_health,
        "system_info": {
            "python_version": "3.x",
            "fastapi_version": APP_VERSION,
            "ai_model": "Claude Sonnet 4",
            "framework": "FastAPI + LangChain",
        },
        "environment": {
            "anthropic_api": "✅" if ANTHROPIC_API_KEY else "❌",
            "openai_api": "✅" if OPENAI_API_KEY else "⚠️",
        },
        "timestamp": datetime.now().isoformat(),
    }


# 전역 예외 처리
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    전역 예외 처리기
    """
    logger.error(f"예상치 못한 오류 발생: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "서버에서 예상치 못한 오류가 발생했습니다.",
            "error_code": "INTERNAL_SERVER_ERROR",
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url),
            "service": "unified-ai-legal-assistant",
        },
    )


# 404 에러 처리
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """
    404 에러 처리기
    """
    available_endpoints = ["/docs", "/health", "/health/detailed"]

    if letter_router:
        available_endpoints.append("/api/v1/generate-letter")
    if analyze_router:
        available_endpoints.append("/api/v1/analyze-contract")
    if contract_router:
        available_endpoints.extend(
            [
                "/api/v1/contract/generate-special-terms",
                "/api/v1/contract/health",
                "/api/v1/contract/validate-input",
            ]
        )

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": "요청하신 API 엔드포인트를 찾을 수 없습니다.",
            "error_code": "NOT_FOUND",
            "path": str(request.url),
            "available_endpoints": available_endpoints,
            "tip": "'/docs'에서 전체 API 문서를 확인하세요.",
            "timestamp": datetime.now().isoformat(),
        },
    )


# 메인 실행
if __name__ == "__main__":

    logger.info("=" * 60)
    logger.info("🏛️  통합 AI 법률 서비스 시작")
    logger.info("=" * 60)
    logger.info(f"🌐 서버 주소: {HOST}:{PORT}")
    logger.info(f"📖 API 문서: http://{HOST}:{PORT}/docs")
    logger.info(f"📚 ReDoc 문서: http://{HOST}:{PORT}/redoc")
    logger.info(f"🔄 자동 리로드: {RELOAD}")
    logger.info(f"🏥 헬스체크: http://{HOST}:{PORT}/health")
    logger.info("=" * 60)

    uvicorn.run("main:app", host=HOST, port=PORT, reload=RELOAD, log_level="info")
