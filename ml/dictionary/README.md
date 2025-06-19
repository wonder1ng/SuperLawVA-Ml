# 📚 법령용어집 구축 프로젝트
복잡한 법령 용어를 누구나 쉽게 이해할 수 있도록 하는 법령용어집 자동 구축 시스템
<br>
<br>
## 🎯 프로젝트 개요
법제처 공공 API를 활용하여 법령 용어를 수집하고, AI(Gemini)를 통해 쉬운 설명을 생성하는 자동화 시스템입니다. <br>
특히 부동산/임대차 계약 관련 용어에 특화되어 있습니다.
<br>
<br>

<div>
<h2>🏗️ 폴더 구조</h2>
<pre>
📁 dictionary
├── 📄 crawling_definition.py    # 1단계: 법제처 API 크롤링
├── 📄 easy_term.py             # 2단계: AI를 통한 쉬운 설명 생성
└── 📄 README.md                # 프로젝트 문서
</pre>
</div>
<br>

## 🚀 사용 방법
### 1단계: 법령 용어 수집 (crawling_definition.py)
- 법제처 공공 API를 통해 모든 법령 용어와 정의를 수집합니다.
- python# API 키 설정 (법제처에서 발급받은 키 입력)
- MY_API_KEY = "your_api_key_here"
<br>

### 2단계: 쉬운 설명 생성 (easy_term.py)
- Gemini AI를 활용하여 수집된 법령 용어에 대한 쉬운 설명을 생성합니다.
- python# Gemini API 키 설정
- genai.configure(api_key="your_gemini_api_key")
<br>
<br>

## 🛠️ 기술 스택
- Python 3.x
- requests: HTTP API 통신
- BeautifulSoup4: XML 파싱
- pandas: 데이터 처리
- google-generativeai: Gemini AI 연동
- csv: 데이터 저장
<br>
<br>

## ⚙️ 설정 방법
### 1. 법제처 API 키 발급

- 법제처 공공데이터포털 접속
- API 이용 신청 및 키 발급
- crawling_definition.py의 MY_API_KEY 변수에 입력

### 2. Gemini API 키 설정

- Google AI Studio 접속
- API 키 생성
- easy_term.py의 API 키 설정 부분에 입력

<br>
