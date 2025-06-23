# Dockerfile
# Description: FastAPI + LLM 법률 서비스 (S3에서 벡터DB 압축 다운로드)
# Author: ooheunsu
# Date: 2025-06-23
# Requirements: Python 3.11, uvicorn, zip, wget

FROM python:3.11-slim

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    unzip wget awscli && \
    rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 생성
WORKDIR /app

# 소스 코드 복사
COPY . .
COPY requirements.txt .
COPY .env .

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 엔트리포인트 스크립트 복사
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

# 서버 실행
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
