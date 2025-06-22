"""
[services/shared/document_search.py] - 벡터 검색 공통 서비스 (디버깅 코드 추가)

기존 generate_letter_chain.py에서 추출한 DocumentSearchService
모든 기능(내용증명, 계약서검토, 특약생성)에서 사용
"""

import asyncio
import os
from typing import Tuple, List
from pathlib import Path

# config import 시도 및 디버깅
try:
    from config import (
        LAW_SEARCH_LIMIT,
        CASE_SEARCH_LIMIT, 
        CASE_SCORE_THRESHOLD,
        CASE_RESULT_LIMIT
    )
    print("✅ DocumentSearchService: config import 성공")
except Exception as e:
    print(f"❌ DocumentSearchService: config import 실패: {e}")
    # 기본값 설정
    LAW_SEARCH_LIMIT = 5
    CASE_SEARCH_LIMIT = 5
    CASE_SCORE_THRESHOLD = 1.5
    CASE_RESULT_LIMIT = 3

# 벡터DB 로더 import 시도 및 디버깅
try:
    from vectordb.loaders.load_law_db import load_law_vectorstore
    from vectordb.loaders.load_case_db import load_case_vectorstore
    print("✅ DocumentSearchService: 벡터DB 로더 import 성공")
except Exception as e:
    print(f"❌ DocumentSearchService: 벡터DB 로더 import 실패: {e}")
    print("🔍 현재 작업 디렉토리:", os.getcwd())
    print("🔍 Python 경로:", str(Path(__file__).parent))
    
    # 대안 import 시도
    try:
        from src.vectordb.loaders.load_law_db import load_law_vectorstore
        from src.vectordb.loaders.load_case_db import load_case_vectorstore
        print("✅ DocumentSearchService: 대안 경로로 벡터DB 로더 import 성공")
    except Exception as e2:
        print(f"❌ DocumentSearchService: 대안 경로로도 벡터DB 로더 import 실패: {e2}")
        raise ImportError("벡터DB 로더를 import할 수 없습니다.")

class DocumentSearchService:
    """벡터 검색 전담 (비동기) - 디버깅 기능 포함"""
    
    def __init__(self):
        self.law_vectorstore = None
        self.case_vectorstore = None
        self._loading = False
        print("🚀 DocumentSearchService 초기화 완료")
    
    async def load_vectorstores(self):
        """벡터스토어 로드 (비동기) - 디버깅 코드 포함"""
        print("📡 벡터스토어 로딩 시작...")
        
        if self.law_vectorstore and self.case_vectorstore:
            print("✅ 벡터스토어가 이미 로드되어 있음")
            return
            
        if self._loading:
            print("⏳ 다른 프로세스에서 로딩 중... 대기")
            while not (self.law_vectorstore and self.case_vectorstore):
                await asyncio.sleep(0.1)
            print("✅ 대기 완료 - 벡터스토어 로드됨")
            return

        self._loading = True
        print("🔄 벡터스토어 로딩 시작...")
        
        try:
            loop = asyncio.get_event_loop()
            
            # 법령 벡터스토어 로드
            print("📚 법령 벡터스토어 로딩 중...")
            self.law_vectorstore = await loop.run_in_executor(None, self._load_law_with_debug)
            print("✅ 법령 벡터스토어 로드 완료")
            
            # 판례 벡터스토어 로드  
            print("⚖️ 판례 벡터스토어 로딩 중...")
            self.case_vectorstore = await loop.run_in_executor(None, self._load_case_with_debug)
            print("✅ 판례 벡터스토어 로드 완료")
            
            self._loading = False
            print("🎉 모든 벡터스토어 로딩 완료!")
            
        except Exception as e:
            self._loading = False
            print(f"❌ 벡터스토어 로딩 실패: {e}")
            raise
    
    def _load_law_with_debug(self):
        """법령 벡터스토어 로드 (디버깅 포함)"""
        try:
            print("🔍 법령 벡터스토어 로딩 함수 호출...")
            vectorstore = load_law_vectorstore()
            print(f"✅ 법령 벡터스토어 객체 생성 성공: {type(vectorstore)}")
            
            # 벡터스토어 내 문서 개수 확인
            try:
                collection = vectorstore._collection
                doc_count = collection.count()
                print(f"📊 법령 벡터스토어 총 문서 개수: {doc_count}개")
                
                # 컬렉션 정보 추가
                print(f"🏷️ 컬렉션 이름: {collection.name}")
                
                # 몇 개 문서 샘플 확인
                if doc_count > 0:
                    sample = collection.get(limit=3)
                    print(f"📝 샘플 문서 ID들: {sample.get('ids', [])[:3]}")
                
            except Exception as e:
                print(f"⚠️ 문서 개수 확인 실패: {e}")
            
            # 간단한 테스트 검색
            test_results = vectorstore.similarity_search("임대차", k=1)
            print(f"🧪 법령 벡터스토어 테스트 검색 결과: {len(test_results)}개")
            
            return vectorstore
        except Exception as e:
            print(f"❌ 법령 벡터스토어 로딩 실패: {e}")
            raise
    
    def _load_case_with_debug(self):
        """판례 벡터스토어 로드 (디버깅 포함)"""
        try:
            print("🔍 판례 벡터스토어 로딩 함수 호출...")
            vectorstore = load_case_vectorstore()
            print(f"✅ 판례 벡터스토어 객체 생성 성공: {type(vectorstore)}")
            
            # 벡터스토어 내 문서 개수 확인
            try:
                collection = vectorstore._collection
                doc_count = collection.count()
                print(f"📊 판례 벡터스토어 총 문서 개수: {doc_count}개")
                
                # 컬렉션 정보 추가
                print(f"🏷️ 컬렉션 이름: {collection.name}")
                
                # 몇 개 문서 샘플 확인
                if doc_count > 0:
                    sample = collection.get(limit=3)
                    print(f"📝 샘플 문서 ID들: {sample.get('ids', [])[:3]}")
                
            except Exception as e:
                print(f"⚠️ 문서 개수 확인 실패: {e}")
            
            # 간단한 테스트 검색
            test_results = vectorstore.similarity_search("임대차", k=1)
            print(f"🧪 판례 벡터스토어 테스트 검색 결과: {len(test_results)}개")
            
            return vectorstore
        except Exception as e:
            print(f"❌ 판례 벡터스토어 로딩 실패: {e}")
            raise
    
    async def search_documents(self, user_query: str) -> Tuple[List, List]:
        """법령과 판례 문서 검색 (기본 - 내용증명용) - 디버깅 코드 포함"""
        print(f"🔍 문서 검색 시작 - 쿼리: '{user_query}'")
        
        if not self.law_vectorstore:
            print("⚠️ 벡터스토어가 로드되지 않음 - 로딩 시작")
            await self.load_vectorstores()
        
        # 벡터 검색을 별도 스레드에서 실행
        loop = asyncio.get_event_loop()
        
        try:
            # 법령 검색
            print(f"📚 법령 검색 중... (limit: {LAW_SEARCH_LIMIT})")
            law_docs = await loop.run_in_executor(
                None, 
                lambda: self.law_vectorstore.similarity_search(user_query, k=LAW_SEARCH_LIMIT)
            )
            print(f"✅ 법령 검색 완료: {len(law_docs)}개 결과")
            
            # 판례 검색 (유사도 필터링)
            print(f"⚖️ 판례 검색 중... (limit: {CASE_SEARCH_LIMIT})")
            case_docs_with_scores = await loop.run_in_executor(
                None,
                lambda: self.case_vectorstore.similarity_search_with_score(user_query, k=CASE_SEARCH_LIMIT)
            )
            
            print(f"📊 판례 검색 원본 결과: {len(case_docs_with_scores)}개")
            
            # 유사도 필터링
            case_docs = [
                doc for doc, score in case_docs_with_scores 
                if score <= CASE_SCORE_THRESHOLD
            ][:CASE_RESULT_LIMIT]
            
            print(f"🔽 판례 필터링 후 결과: {len(case_docs)}개 (threshold: {CASE_SCORE_THRESHOLD})")
            
            # 점수 정보 출력
            for i, (doc, score) in enumerate(case_docs_with_scores[:3]):
                print(f"   판례 {i+1}: 점수 {score:.3f}")
            
            print(f"🎯 최종 검색 결과: 법령 {len(law_docs)}개, 판례 {len(case_docs)}개")
            return law_docs, case_docs
            
        except Exception as e:
            print(f"❌ 문서 검색 실패: {e}")
            return [], []
    
    async def search_laws_only(self, query: str, limit: int = 10) -> List:
        """법령만 검색 (계약서 검토에서 사용) - 디버깅 코드 포함"""
        print(f"📚 법령 전용 검색: '{query}' (limit: {limit})")
        
        if not self.law_vectorstore:
            await self.load_vectorstores()
        
        try:
            loop = asyncio.get_event_loop()
            law_docs = await loop.run_in_executor(
                None,
                lambda: self.law_vectorstore.similarity_search(query, k=limit)
            )
            print(f"✅ 법령 전용 검색 완료: {len(law_docs)}개 결과")
            return law_docs
        except Exception as e:
            print(f"❌ 법령 전용 검색 실패: {e}")
            return []
    
    async def search_cases_by_issue(self, issue_description: str, limit: int = 5) -> List:
        """문제 상황 기반 판례 검색 (계약서 검토에서 사용) - 디버깅 코드 포함"""
        print(f"⚖️ 판례 이슈 검색: '{issue_description}' (limit: {limit})")
        
        if not self.case_vectorstore:
            await self.load_vectorstores()
        
        try:
            loop = asyncio.get_event_loop()
            case_docs_with_scores = await loop.run_in_executor(
                None,
                lambda: self.case_vectorstore.similarity_search_with_score(issue_description, k=limit)
            )
            
            # 문제 판례는 더 엄격한 유사도 기준 적용
            case_docs = [
                doc for doc, score in case_docs_with_scores 
                if score < CASE_SCORE_THRESHOLD
            ][:limit]
            
            print(f"✅ 판례 이슈 검색 완료: {len(case_docs)}개 결과 (필터링 전: {len(case_docs_with_scores)}개)")
            return case_docs
        except Exception as e:
            print(f"❌ 판례 이슈 검색 실패: {e}")
            return []