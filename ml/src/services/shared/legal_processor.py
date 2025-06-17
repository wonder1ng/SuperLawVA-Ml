"""
[services/shared/legal_processor.py] - 법령 처리 공통 서비스 (수정된 버전)

legal_basis 생성 문제 해결
"""

import re
from typing import List, Set, Optional, Dict
from services.schema.shared_schema import LegalReference, LegalBasis

class LegalProcessor:
    """법령 처리 공통 서비스 (수정된 버전)"""
    
    def __init__(self, llm):
        self.llm = llm
        # 기존 패턴 유지
        self.law_pattern = re.compile(
            r"(?:「)?(?P<law>[가-힣·\w\d\s]{2,}?(법|시행령|시행규칙))(?:」)?\s*제\s*(?P<article>\d+)\s*조(?:\s*제\s*(?P<clause>\d+)\s*항)?(?:\s*제\s*(?P<item>\d+)\s*호)?",
            re.UNICODE
        )
        
        # 개선된 패턴 추가 - 「」로 감싸진 모든 법령명 매칭
        self.improved_law_pattern = re.compile(
            r"「(?P<law>[^」]+)」\s*제\s*(?P<article>\d+)\s*조(?:\s*제\s*(?P<clause>\d+)\s*항)?(?:\s*제\s*(?P<item>\d+)\s*호)?",
            re.UNICODE
        )
    
    def extract_referenced_laws(self, text: str) -> Set[str]:
        """텍스트에서 인용된 법령 추출 (개선된 버전)"""
        referenced_laws = set()
        
        print(f"[DEBUG] 법령 추출 시작...")
        print(f"[DEBUG] 입력 텍스트 길이: {len(text)}")
        
        # 1. 개선된 패턴으로 먼저 매칭 (「」로 감싸진 법령)
        improved_matches = list(self.improved_law_pattern.finditer(text))
        print(f"[DEBUG] 개선된 패턴 매칭 결과: {len(improved_matches)}개")
        
        for match in improved_matches:
            law = match.group("law").strip()
            article = match.group("article")
            clause = match.group("clause")
            item = match.group("item")
            
            key = f"{law} 제{article}조"
            if clause:
                key += f" 제{clause}항"
            if item:
                key += f" 제{item}호"
                
            referenced_laws.add(key)
            print(f"[DEBUG] 개선된 패턴으로 추출: {key}")
        
        # 2. 기존 패턴으로 추가 매칭 (누락된 것들 찾기)
        original_matches = list(self.law_pattern.finditer(text))
        print(f"[DEBUG] 기존 패턴 매칭 결과: {len(original_matches)}개")
        
        for match in original_matches:
            law = match.group("law").strip()
            article = match.group("article")
            clause = match.group("clause")
            item = match.group("item")
            
            key = f"{law} 제{article}조"
            if clause:
                key += f" 제{clause}항"
            if item:
                key += f" 제{item}호"
                
            referenced_laws.add(key)
            print(f"[DEBUG] 기존 패턴으로 추출: {key}")
        
        print(f"[DEBUG] 최종 추출된 법령들: {referenced_laws}")
        print(f"[DEBUG] 총 {len(referenced_laws)}개 법령 추출됨")
        
        return referenced_laws
    
    async def generate_law_summary(self, full_text: str) -> str:
        """법령 요약 생성 (모든 기능에서 사용)"""
        summary_prompt = f"""
        다음 법령 조문이 사용자에게 제공하는 권리나 법적 보호를 1-2문장으로 요약해주세요:
        "{full_text}"
        """
        try:
            response = await self.llm.ainvoke(summary_prompt)
            return response.content.strip()
        except Exception as e:
            print(f"[DEBUG] 법령 요약 생성 오류: {e}")
            return "법령 요약 생성 중 오류가 발생했습니다."
    
    def find_law_document(self, reference: str, law_docs: list):
        """참조된 법령에 해당하는 문서 찾기 (완전 수정 버전)"""
        print(f"[DEBUG] *** 완전 수정된 find_law_document 함수 실행 ***")
        print(f"[DEBUG] 검색 대상: {reference}")
        print(f"[DEBUG] 검색할 문서 개수: {len(law_docs)}")
        
        # === 다양한 정규식 패턴들 ===
        patterns = [
            # 패턴 1: 「법령명」 제X조 제Y항 제Z호
            re.compile(r"「([^」]+)」\s*제\s*(\d+)\s*조(?:\s*제\s*(\d+)\s*항)?(?:\s*제\s*(\d+)\s*호)?", re.UNICODE),
            
            # 패턴 2: 법령명 제X조 제Y항 제Z호 (「」 없음)
            re.compile(r"(.+?)\s+제\s*(\d+)\s*조(?:\s*제\s*(\d+)\s*항)?(?:\s*제\s*(\d+)\s*호)?", re.UNICODE),
            
            # 패턴 3: 기존 패턴 (백업용)
            re.compile(r"(?:「)?([^」]*?(법|시행령|시행규칙))(?:」)?\s*제\s*(\d+)\s*조(?:\s*제\s*(\d+)\s*항)?(?:\s*제\s*(\d+)\s*호)?", re.UNICODE)
        ]
        
        # === 정규식 매칭 시도 ===
        law_name = None
        article = None
        clause = None
        item = None
        
        for i, pattern in enumerate(patterns):
            match = pattern.search(reference)
            if match:
                print(f"[DEBUG] 패턴 {i} 매칭 성공!")
                groups = match.groups()
                print(f"[DEBUG] 매칭 그룹들: {groups}")
                
                if i == 0:  # 패턴 1
                    law_name, article, clause, item = groups
                elif i == 1:  # 패턴 2
                    law_name, article, clause, item = groups
                elif i == 2:  # 패턴 3
                    law_name = groups[0]  # 첫 번째 그룹이 법령명
                    article = groups[2]   # 세 번째 그룹이 조문번호
                    clause = groups[3] if len(groups) > 3 else None
                    item = groups[4] if len(groups) > 4 else None
                
                law_name = law_name.strip() if law_name else ""
                print(f"[DEBUG] 파싱 결과 - 법령: '{law_name}', 조: '{article}', 항: '{clause}', 호: '{item}'")
                break
            else:
                print(f"[DEBUG] 패턴 {i} 매칭 실패")
        
        if not law_name or not article:
            print(f"[DEBUG] 정규식 매칭 완전 실패: {reference}")
            return None
        
        # === 1단계: 법령명으로 필터링 ===
        law_name_clean = law_name.replace(" ", "").strip()
        matching_law_docs = []
        
        print(f"[DEBUG] 1단계: 법령명 '{law_name_clean}' 필터링")
        for i, doc in enumerate(law_docs):
            doc_law_name = doc.metadata.get("법령명", "").replace(" ", "").strip()
            print(f"[DEBUG] 문서 {i}: '{doc_law_name}' vs '{law_name_clean}'")
            
            if doc_law_name == law_name_clean:
                matching_law_docs.append(doc)
                print(f"[DEBUG] ✅ 법령명 매칭: {doc.metadata}")
        
        if not matching_law_docs:
            print(f"[DEBUG] ❌ 법령명 매칭 실패: {law_name_clean}")
            return None
        
        print(f"[DEBUG] 1단계 결과: {len(matching_law_docs)}개 문서")
        
        # === 2단계: 조문번호로 필터링 ===
        matching_article_docs = []
        
        print(f"[DEBUG] 2단계: 조문번호 '{article}' 필터링")
        for doc in matching_law_docs:
            doc_article = str(doc.metadata.get("조문번호", "")).strip()
            print(f"[DEBUG] 조문 비교: '{doc_article}' vs '{article}'")
            
            if doc_article == article:
                matching_article_docs.append(doc)
                print(f"[DEBUG] ✅ 조문 매칭: {doc.metadata}")
        
        if not matching_article_docs:
            print(f"[DEBUG] ❌ 조문 매칭 실패: 제{article}조")
            return None
        
        print(f"[DEBUG] 2단계 결과: {len(matching_article_docs)}개 문서")
        
        # === 3단계: 항번호로 필터링 (선택적) ===
        final_docs = matching_article_docs
        
        if clause:
            print(f"[DEBUG] 3단계: 항번호 '{clause}' 필터링")
            clause_docs = []
            for doc in matching_article_docs:
                doc_clause = str(doc.metadata.get("항번호", "")).strip()
                print(f"[DEBUG] 항 비교: '{doc_clause}' vs '{clause}'")
                
                if doc_clause == clause:
                    clause_docs.append(doc)
                    print(f"[DEBUG] ✅ 항 매칭: {doc.metadata}")
            
            if clause_docs:
                final_docs = clause_docs
                print(f"[DEBUG] 3단계 결과: {len(final_docs)}개 문서")
            else:
                print(f"[DEBUG] ⚠️ 항 매칭 실패, 조문 레벨 유지")
        
        # === 4단계: 호번호로 필터링 (선택적) ===
        if item:
            print(f"[DEBUG] 4단계: 호번호 '{item}' 필터링")
            item_docs = []
            for doc in final_docs:
                doc_item = str(doc.metadata.get("호번호", "")).strip()
                print(f"[DEBUG] 호 비교: '{doc_item}' vs '{item}'")
                
                if doc_item == item:
                    item_docs.append(doc)
                    print(f"[DEBUG] ✅ 호 매칭: {doc.metadata}")
            
            if item_docs:
                final_docs = item_docs
                print(f"[DEBUG] 4단계 결과: {len(final_docs)}개 문서")
            else:
                print(f"[DEBUG] ⚠️ 호 매칭 실패, 상위 레벨 유지")
        
        # === 최종 반환 ===
        if final_docs:
            result_doc = final_docs[0]
            print(f"[DEBUG] 🎯 최종 선택 문서: {result_doc.metadata}")
            return result_doc
        else:
            print(f"[DEBUG] ❌ 최종 문서 없음")
            return None
    
    async def generate_legal_explanations(self, referenced_laws: Set[str], law_docs: list) -> List[LegalReference]:
        """법령 상세 설명 생성 (개선된 버전)"""
        print(f"[DEBUG] 법령 설명 생성 시작...")
        print(f"[DEBUG] 처리할 법령 개수: {len(referenced_laws)}")
        print(f"[DEBUG] 사용 가능한 law_docs 개수: {len(law_docs)}")
        
        legal_explanations = []
        
        for law_ref in referenced_laws:
            print(f"[DEBUG] 처리 중인 법령: {law_ref}")
            
            target_doc = self.find_law_document(law_ref, law_docs)
            if not target_doc:
                print(f"[DEBUG] 문서를 찾지 못함: {law_ref}")
                # 문서를 찾지 못해도 기본 정보는 추가
                legal_explanations.append(
                    LegalReference(
                        title=law_ref,
                        full_text=f"{law_ref}에 관한 내용",
                        summary=f"{law_ref}에 관한 법적 규정",
                        law_id="0"
                    )
                )
                continue
            
            full_text = target_doc.page_content.strip().replace("\n", " ")
            summary = await self.generate_law_summary(full_text)
            
            # 실제 법령ID 추출
            law_id = target_doc.metadata.get("법령ID", "") or target_doc.metadata.get("law_id", "")
            if not law_id:
                law_id = "0"
            
            print(f"[DEBUG] 법령 설명 생성 완료: {law_ref}")
            
            legal_explanations.append(
                LegalReference(
                    title=law_ref,
                    full_text=full_text,
                    summary=summary,
                    law_id=str(law_id)
                )
            )
        
        print(f"[DEBUG] 총 {len(legal_explanations)}개 법령 설명 생성됨")
        return legal_explanations
    
    async def analyze_law_for_review(self, law_doc, clause_text: str) -> Dict[str, str]:
        """계약서 검토용 법령 분석"""
        law_text = law_doc.page_content.strip().replace("\n", " ")
        
        analysis_prompt = f"""
        다음 계약 조항이 법령에 위배되는지 분석해주세요:
        
        계약 조항: {clause_text}
        관련 법령: {law_text}
        
        분석 결과를 다음 형식으로 작성해주세요:
        **위험도**: medium/low
        **문제점**: 구체적인 법적 문제
        **권장사항**: 수정 제안
        """
        
        try:
            response = await self.llm.ainvoke(analysis_prompt)
            content = response.content.strip()
            
            # 분석 결과 파싱
            risk_level = "medium"  # 기본값
            issues = ""
            recommendations = ""
            
            lines = content.split('\n')
            for line in lines:
                if '**위험도**' in line:
                    risk_level = line.split(':')[-1].strip()
                elif '**문제점**' in line:
                    issues = line.split(':')[-1].strip()
                elif '**권장사항**' in line:
                    recommendations = line.split(':')[-1].strip()
            
            return {
                "risk_level": risk_level,
                "issues": issues,
                "recommendations": recommendations,
                "law_summary": await self.generate_law_summary(law_text)
            }
            
        except Exception as e:
            print(f"[DEBUG] 법령 분석 오류: {e}")
            return {
                "risk_level": "unknown",
                "issues": "분석 중 오류 발생",
                "recommendations": "전문가 상담 권장",
                "law_summary": "법령 요약 실패"
            }
    
    def convert_to_legal_basis(self, legal_explanations: List[LegalReference]) -> List[LegalBasis]:
        """LegalReference를 LegalBasis로 변환 - 실제 법령ID 사용"""
        print(f"[DEBUG] LegalBasis 변환 시작: {len(legal_explanations)}개")
        
        legal_basis = []
        for ref in legal_explanations:
            # 실제 법령ID가 있으면 사용, 없으면 0
            law_id = int(ref.law_id) if ref.law_id and ref.law_id.isdigit() else 0
            
            legal_basis.append(
                LegalBasis(
                    law_id=law_id,
                    law=ref.title,
                    explanation=ref.summary or "법령 설명",
                    content=ref.full_text or "법령 내용"
                )
            )
            print(f"[DEBUG] 변환됨: {ref.title} -> law_id={law_id}")
        
        print(f"[DEBUG] LegalBasis 변환 완료: {len(legal_basis)}개")
        return legal_basis

    # 기존 함수명들 호환성 유지
    def _find_law_document(self, reference: str, law_docs: list):
        """기존 함수명 호환성 유지"""
        return self.find_law_document(reference, law_docs)
    
    async def _generate_law_summary(self, full_text: str) -> str:
        """기존 함수명 호환성 유지"""
        return await self.generate_law_summary(full_text)

# 데이터 변환 유틸리티 함수들 (개선된 버전)
def convert_to_legal_basis(legal_explanations: List[LegalReference]) -> List[LegalBasis]:
    """내용증명용 LegalBasis 변환 (독립 함수, 개선된 버전)"""
    print(f"[DEBUG] convert_to_legal_basis 함수 호출: {len(legal_explanations)}개")
    
    legal_basis = []
    for ref in legal_explanations:
        # 실제 법령ID가 있으면 사용, 없으면 0
        law_id = int(ref.law_id) if ref.law_id and ref.law_id.isdigit() else 0
        
        legal_basis.append(
            LegalBasis(
                law_id=law_id,
                law=ref.title,
                explanation=ref.summary or "법령 설명",
                content=ref.full_text or "법령 내용"
            )
        )
        print(f"[DEBUG] 독립함수 변환됨: {ref.title} -> law_id={law_id}")
    
    print(f"[DEBUG] 독립함수 변환 완료: {len(legal_basis)}개")
    return legal_basis

def convert_to_review_format(legal_explanations: List[LegalReference], analysis_results: List[Dict]) -> List[Dict]:
    """계약서 검토용 형식 변환"""
    review_results = []
    for ref, analysis in zip(legal_explanations, analysis_results):
        review_results.append({
            "law_title": ref.title,
            "law_summary": ref.summary,
            "risk_level": analysis.get("risk_level", "medium"),
            "issues": analysis.get("issues", ""),
            "recommendations": analysis.get("recommendations", ""),
            "law_id": ref.law_id
        })
    return review_results