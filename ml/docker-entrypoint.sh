#!/bin/bash

VDB_CHECK_DIR="/app/src/vectordb/chroma_law/chroma_openai_law"

if [ -d "$VDB_CHECK_DIR" ] && [ "$(ls -A "$VDB_CHECK_DIR")" ]; then
  echo "✅ 벡터DB가 이미 존재합니다. 압축 해제 생략"
else
  echo "🔄 S3에서 벡터DB 압축 파일 다운로드 중..."
  aws s3 cp s3://superlawva-ml-bucket/vectordb.zip ./vectordb.zip

  echo "📦 압축 해제 중..."
  unzip -o ./vectordb.zip -d /app/src/

  echo "🧹 불필요한 파일 정리 중..."
  rm -rf /app/src/__MACOSX
  rm -f ./vectordb.zip

  echo "✅ 벡터DB 준비 완료. 서버 시작 중..."
fi

# 최종적으로 FastAPI 실행
exec uvicorn main:app --host 0.0.0.0 --port 8000

