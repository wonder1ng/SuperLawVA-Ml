# SuperLawVA
> Super Law Virtual Assistant
1. 특약 생성
2. 계약서 검토
3. 내용증명생성
---
## 🤖 MLOps 기능 요약

> **법률 특화 RAG 시스템 + FastAPI 기반 서비스화**

### 🔧 주요 역할

- **주요 생성 기능 3가지 구현**
  - ✍️ 특약 생성
  - 🔍 계약서 검토
  - 📩 내용증명서 작성  
  → 모두 **Claude** 기반 생성 모델 사용

- **간단한 질의응답 챗봇 구현**  
  → **GPT** 기반으로 챗GPT 스타일 UI에 맞춘 대화형 설계

- **벡터DB 구축**
  - 판례 / 법령 데이터를 각각 **ChromaDB**에 저장
  - OpenAI `text-embedding-3-large` 임베딩 모델 사용

- **LangChain 기반 RAG 체인 구성**
  - 기능별로 Prompt, Retriever, Output Parser 등을 모듈화하여 설계

- **FastAPI 기반 ML API 서버 구축**
  - 백엔드와 완전 연동되는 REST API 제공

- **GitHub Actions 기반 CI/CD 자동화 파이프라인 구축**
  - 코드 Push 시 Docker Build → EC2 자동 배포

---

### 🧪 MLOps 기술 요약

| 항목               | 상세 내용                                  |
|--------------------|---------------------------------------------|
| 생성 모델           | **GPT (챗봇)** / **Claude (기능 3종)**        |
| 프레임워크          | FastAPI, LangChain                         |
| 임베딩 모델         | OpenAI `text-embedding-3-large`            |
| 벡터DB             | ChromaDB (법령 / 판례 분리 구축)           |
| 배포 방식           | Docker + AWS EC2                          |
| CI/CD 자동화 도구   | GitHub Actions                            |
| 문서 Chunking 방식  | RecursiveCharacterTextSplitter + 커스텀 필터링 |

---

### 💡 RAG 기반 처리 구조
```
[사용자 입력]
↓
[ChromaDB 검색 (법령 + 판례)]
↓
[관련 context 구성]
↓
[LLM에게 Prompt 전달]
↓
[문서 생성: GPT 또는 Claude]
```

---

> "MLOps 팀은 특약생성, 계약서 검토, 내용증명서 자동 생성의 3가지 주요 기능을 Claude 모델로 구현하고,  
> 사용자 친화형 GPT 챗봇도 함께 개발했습니다.  
> 판례와 법령은 각각 ChromaDB에 구축하고, RAG 기반으로 유사 문서를 검색해 LLM에 context로 전달합니다.  
> 또한 GitHub Actions 기반 CI/CD 파이프라인을 구축해, 코드 푸시만으로 Docker 이미지 빌드 및 EC2 자동 배포가 이루어지도록 설정했습니다."
