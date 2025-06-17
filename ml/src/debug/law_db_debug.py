#!/usr/bin/env python3
"""
debug_vectordb_search.py - 벡터DB 법령 검색 디버깅 전용 파일

DocumentSearchService를 사용하여 벡터DB에서 메타데이터 기반으로 법령을 검색하고 분석하는 완전 독립적인 디버깅 스크립트

사용법:
    python debug_vectordb_search.py

목적:
    1. DocumentSearchService를 통한 벡터스토어 로드 테스트
    2. 벡터DB에 주택임대차보호법이 있는지 확인
    3. 벡터DB에 주민등록법이 있는지 확인  
    4. 벡터DB에 부동산 거래신고 법령이 있는지 확인
    5. 벡터 검색 vs 메타데이터 검색 결과 비교
    6. 전체 법령 데이터 통계 확인
"""

import sys
import os
import asyncio
from typing import List, Dict, Any

# 프로젝트 루트 경로 추가 (필요시 조정)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from services.shared.document_search import DocumentSearchService
    print("✅ DocumentSearchService 임포트 성공")
except ImportError as e:
    print(f"❌ DocumentSearchService 임포트 실패: {e}")
    print("💡 services.shared.document_search 경로를 확인하세요")
    sys.exit(1)


class VectorDBDebugger:
    """벡터DB 디버깅 전용 클래스 (DocumentSearchService 사용)"""
    
    def __init__(self):
        self.search_service = DocumentSearchService()
        self.total_docs = 0
        self.all_metadatas = []
        self.all_documents = []
    
    async def load_vectorstore(self):
        """벡터스토어 로드 (DocumentSearchService 사용)"""
        print("🔄 벡터스토어 로딩 중...")
        try:
            await self.search_service.load_vectorstores()
            
            if self.search_service.law_vectorstore:
                print("✅ 법령 벡터스토어 로드 성공")
            if self.search_service.case_vectorstore:
                print("✅ 판례 벡터스토어 로드 성공")
            
            return True
        except Exception as e:
            print(f"❌ 벡터스토어 로드 실패: {e}")
            return False
    
    async def get_all_data(self):
        """전체 데이터 조회"""
        print("\n🔄 전체 데이터 조회 중...")
        try:
            # DocumentSearchService를 통해 전체 데이터 가져오기
            if not self.search_service.law_vectorstore:
                await self.search_service.load_vectorstores()
            
            # 전체 데이터 가져오기
            results = self.search_service.law_vectorstore.get(include=["metadatas", "documents"])
            
            self.all_metadatas = results['metadatas']
            self.all_documents = results['documents'] 
            self.total_docs = len(self.all_documents)
            
            print(f"✅ 전체 문서 조회 성공: {self.total_docs:,}개")
            print(f"✅ 전체 메타데이터 조회 성공: {len(self.all_metadatas):,}개")
            return True
            
        except Exception as e:
            print(f"❌ 전체 데이터 조회 실패: {e}")
            return False
    
    def search_by_keyword(self, keyword: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """키워드로 법령명 검색"""
        results = []
        
        for i, metadata in enumerate(self.all_metadatas):
            law_name = metadata.get("법령명", "")
            if keyword in law_name:
                results.append({
                    'index': i,
                    'metadata': metadata,
                    'content': self.all_documents[i] if i < len(self.all_documents) else "",
                    'law_name': law_name
                })
        
        return results[:max_results]
    
    def print_search_results(self, keyword: str, results: List[Dict[str, Any]], show_content: bool = False):
        """검색 결과 출력"""
        print(f"\n🔍 '{keyword}' 검색 결과: {len(results)}개")
        print("-" * 60)
        
        if not results:
            print("❌ 검색 결과가 없습니다.")
            return
        
        for i, result in enumerate(results, 1):
            metadata = result['metadata']
            law_name = metadata.get('법령명', '미상')
            article = metadata.get('조문번호', '?')
            clause = metadata.get('항번호', '')
            law_id = metadata.get('법령ID', '?')
            
            clause_text = f" 제{clause}항" if clause else ""
            print(f"{i:2}. [{law_id}] {law_name} 제{article}조{clause_text}")
            
            if show_content:
                content = result['content'][:200].replace('\n', ' ').strip()
                if content:
                    print(f"    📄 {content}...")
                else:
                    print("    📄 (내용 없음)")
            print()
    
    def analyze_law_statistics(self):
        """법령 통계 분석"""
        print("\n📊 법령 데이터 통계 분석")
        print("=" * 60)
        
        # 법령명별 조문 수 통계
        law_counts = {}
        law_ids = set()
        
        for metadata in self.all_metadatas:
            law_name = metadata.get("법령명", "미상")
            law_id = metadata.get("법령ID", "")
            
            law_counts[law_name] = law_counts.get(law_name, 0) + 1
            if law_id:
                law_ids.add(law_id)
        
        print(f"📈 총 문서 수: {self.total_docs:,}개")
        print(f"📈 고유 법령 수: {len(law_counts)}개")
        print(f"📈 고유 법령ID 수: {len(law_ids)}개")
        
        # 조문 수가 많은 법령 TOP 10
        print(f"\n📋 조문 수 상위 10개 법령:")
        sorted_laws = sorted(law_counts.items(), key=lambda x: x[1], reverse=True)
        for i, (law_name, count) in enumerate(sorted_laws[:10], 1):
            print(f"  {i:2}. {law_name}: {count}개 조문")
    
    def test_specific_laws(self):
        """특정 법령들 상세 테스트"""
        print("\n🎯 특정 법령 상세 검색 테스트")
        print("=" * 60)
        
        # 테스트할 키워드들
        test_keywords = [
            "주택임대차",
            "부동산"
        ]
        
        for keyword in test_keywords:
            results = self.search_by_keyword(keyword, max_results=10)
            self.print_search_results(keyword, results, show_content=True)
    
    def test_article_16_laws(self):
        """제16조 관련 법령 검색"""
        print("\n🔍 제16조 관련 법령 검색")
        print("=" * 60)
        
        article_16_laws = []
        
        for i, metadata in enumerate(self.all_metadatas):
            article = metadata.get('조문번호', '')
            if article == "16":
                article_16_laws.append({
                    'index': i,
                    'metadata': metadata,
                    'content': self.all_documents[i] if i < len(self.all_documents) else ""
                })
        
        print(f"📊 제16조 법령 총 {len(article_16_laws)}개")
        
        for i, law in enumerate(article_16_laws[:20], 1):  # 처음 20개만
            metadata = law['metadata']
            law_name = metadata.get('법령명', '미상')
            clause = metadata.get('항번호', '')
            law_id = metadata.get('법령ID', '?')
            
            clause_text = f" 제{clause}항" if clause else ""
            print(f"  {i:2}. [{law_id}] {law_name} 제16조{clause_text}")
            
            # 주민등록법이면 내용도 출력
            if "주민등록" in law_name:
                content = law['content'][:300].replace('\n', ' ').strip()
                print(f"      📄 {content}...")
            print()
    
    async def test_vector_search_comparison(self):
        """벡터 검색 vs 메타데이터 검색 비교 테스트"""
        print("\n🔍 벡터 검색 vs 메타데이터 검색 비교")
        print("=" * 60)
        
        test_queries = [
            "저는 전입신고를 하고 싶은데 집주인이 안 해준대요",
            "주택임대차보호법",
            "주민등록법",
            "부동산 거래신고"
        ]
        
        for query in test_queries:
            print(f"\n🔍 쿼리: '{query}'")
            print("-" * 40)
            
            try:
                # 벡터 검색 결과
                vector_results = await self.search_service.search_laws_only(query, limit=10)
                print(f"📊 벡터 검색 결과: {len(vector_results)}개")
                
                for i, doc in enumerate(vector_results[:5], 1):
                    law_name = doc.metadata.get('법령명', '미상')
                    article = doc.metadata.get('조문번호', '?')
                    law_id = doc.metadata.get('법령ID', '?')
                    print(f"  {i}. [{law_id}] {law_name} 제{article}조")
                
                # 메타데이터 검색 결과 (키워드 포함)
                keywords = query.split()
                metadata_results = []
                for keyword in keywords:
                    if len(keyword) > 1:  # 한 글자 키워드 제외
                        keyword_results = self.search_by_keyword(keyword, max_results=5)
                        metadata_results.extend(keyword_results)
                
                # 중복 제거
                unique_metadata = []
                seen_ids = set()
                for result in metadata_results:
                    law_id = result['metadata'].get('법령ID', '')
                    article = result['metadata'].get('조문번호', '')
                    unique_key = f"{law_id}_{article}"
                    if unique_key not in seen_ids:
                        unique_metadata.append(result)
                        seen_ids.add(unique_key)
                
                print(f"📊 메타데이터 검색 결과: {len(unique_metadata)}개")
                for i, result in enumerate(unique_metadata[:5], 1):
                    metadata = result['metadata']
                    law_name = metadata.get('법령명', '미상')
                    article = metadata.get('조문번호', '?')
                    law_id = metadata.get('법령ID', '?')
                    print(f"  {i}. [{law_id}] {law_name} 제{article}조")
                
            except Exception as e:
                print(f"❌ 검색 실패: {e}")

    def search_full_law_names(self):
        """정확한 법령명으로 검색"""
        print("\n🎯 정확한 법령명 검색 테스트")
        print("=" * 60)
        
        target_laws = [
            "주택임대차보호법",
            "주민등록법", 
            "부동산 거래신고 등에 관한 법률",
            "부동산거래신고등에관한법률",
            "부동산 실거래가 신고 등에 관한 특례법"
        ]
        
        for target_law in target_laws:
            print(f"\n🔍 '{target_law}' 정확 매칭 검색:")
            
            exact_matches = []
            partial_matches = []
            
            for i, metadata in enumerate(self.all_metadatas):
                law_name = metadata.get("법령명", "")
                
                if law_name == target_law:
                    exact_matches.append({
                        'metadata': metadata,
                        'content': self.all_documents[i] if i < len(self.all_documents) else ""
                    })
                elif target_law in law_name or law_name in target_law:
                    partial_matches.append({
                        'metadata': metadata,
                        'content': self.all_documents[i] if i < len(self.all_documents) else ""
                    })
            
            print(f"  ✅ 정확 매칭: {len(exact_matches)}개")
            print(f"  🔸 부분 매칭: {len(partial_matches)}개")
            
            # 결과 출력
            all_matches = exact_matches + partial_matches
            for match in all_matches[:5]:  # 처음 5개만
                metadata = match['metadata']
                law_name = metadata.get('법령명', '미상')
                article = metadata.get('조문번호', '?')
                law_id = metadata.get('법령ID', '?')
                print(f"    - [{law_id}] {law_name} 제{article}조")


async def main():
    """메인 실행 함수 (비동기)"""
    print("🚀 벡터DB 법령 검색 디버깅 시작")
    print("=" * 60)
    
    # 디버거 초기화
    debugger = VectorDBDebugger()
    
    # 1. 벡터스토어 로드
    if not await debugger.load_vectorstore():
        print("❌ 벡터스토어 로드 실패로 종료")
        return
    
    # 2. 전체 데이터 조회
    if not await debugger.get_all_data():
        print("❌ 전체 데이터 조회 실패로 종료")
        return
    
    # 3. 통계 분석
    debugger.analyze_law_statistics()
    
    # 4. 키워드 검색 테스트
    debugger.test_specific_laws()
    
    # 5. 제16조 관련 법령 검색
    debugger.test_article_16_laws()
    
    # 6. 벡터 검색 vs 메타데이터 검색 비교
    await debugger.test_vector_search_comparison()
    
    # 7. 정확한 법령명 검색
    debugger.search_full_law_names()
    
    print("\n✅ 벡터DB 법령 검색 디버깅 완료")
    print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  사용자에 의해 중단됨")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류 발생: {e}")
        import traceback
        traceback.print_exc()