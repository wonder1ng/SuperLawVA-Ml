"""
[analyze_contract_chain.py] - 계약서 검토 생성 체인 (조항별 개별 분석 + 즉시 요약)

조항별로 RAG 검색 → LLM 판단 → 즉시 요약 → 결과 조립 방식
"""

import time
import asyncio
from datetime import datetime
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# 공통 모듈들 import
from services.shared.document_search import DocumentSearchService
from services.shared.contract_parser import extract_contract_clauses, extract_key_contract_info
from services.shared.legal_processor import LegalProcessor, convert_to_legal_basis
from services.shared.case_processor import CaseProcessor, convert_to_case_basis
from services.shared.formatters import DocumentFormatter
from services.shared.llm_config import get_claude_llm_for_review

# 스키마 import
from services.schema.analyze_schema import (
    ContractAnalysisInput,
    ContractAnalysisOutput,
    ClauseAnalysis,
    RecommendedAgreement,
    AnalysisMetadata,
    ClauseLegalBasis,
    ClauseCaseBasis
)

# 조항별 분석용 스키마
from pydantic import BaseModel, Field
from typing import Optional, List

class SingleClauseAnalysisResult(BaseModel):
    """단일 조항 분석 결과 (LLM 출력용)"""
    result: bool = Field(description="적절 여부 (true: 적절, false: 부적절)")
    reason: str = Field(description="판단 이유 (1-2줄)")
    suggested_revision: Optional[str] = Field(default=None, description="수정안 (부적절시만)")
    negotiation_points: Optional[str] = Field(default=None, description="협상 포인트 (부적절시만)")
    selected_law: Optional[str] = Field(default=None, description="가장 관련성 높은 법령 1개 (부적절시만)")
    selected_cases: List[str] = Field(default_factory=list, description="가장 관련성 높은 판례 3개 (부적절시만)")

# 계약서 검토 전용 LLM 설정
llm = get_claude_llm_for_review()
output_parser = PydanticOutputParser(pydantic_object=SingleClauseAnalysisResult)

# 조항별 분석 프롬프트 템플릿 (근본적 수정)
clause_analysis_prompt = ChatPromptTemplate.from_template("""
당신은 25년 경력의 임대차 전문 변호사입니다.
다음 계약 조항을 **계약서 전체 맥락**을 고려하여 객관적으로 검토해주세요.

【계약서 정보】
{contract_context}

【검토 대상 조항】
{clause_content}

【중요한 판단 원칙】
1. **계약서는 여러 조항이 함께 작동하는 유기적 전체입니다**
2. **위의 계약서 기본 정보에 필요한 내용이 이미 명시되어 있다면 해당 조항은 적절한 것입니다**
3. **일반적이고 표준적인 조항은 적절한 것으로 판단하세요**
4. **명백하고 심각한 문제가 있을 때만 부적절로 판단하세요**

【예시】
✅ 적절한 경우:
- "매월 5일까지 월세 지급" → 일반적인 월세 납부 조항으로 적절
- "에어컨 설치 후 철거" → 표준적인 원상복구 조항으로 적절

❌ 부적절한 경우:
- "임차인이 모든 손해를 무제한 배상" → 명백히 과도한 책임
- "임대인이 언제든 계약 해지 가능" → 명백한 법령 위반
- "보증금 없이 월세만 지급" → 임차인에게 심각한 불이익

【관련 법령 (10개)】
{related_laws_str}

【관련 판례 (10개)】
{related_cases_str}

**검토 기준 (매우 중요!):**
    - **주의**(result=false): 모호한 표현, 불균형한 권리관계, 협상이 필요한 조항, 업계 표준을 벗어난 조항, 임대차보호법 위반 소지, 임차인에게 과도한 불이익, 법적 분쟁 가능성 높음, 강제집행 시 문제 발생 가능
    - **적절(result=true)**: 법령에 부합하고 균형잡힌 조항, 양 당사자의 권리가 적절히 보호됨

[검토 영역]
다음 3가지 영역을 반드시 검토하세요:

1. **형식 검토**
   - 필수 계약 요소의 누락 여부
   - 용어 사용의 일관성
   - 참조 조항의 정확성

2. **내용 검토**
   - 책임과 의무의 균형성
   - 모호하거나 해석의 여지가 있는 조항
   - 당사자의 권리 보호 수준
   - 업계 표준 대비 적정성

3. **법적 위험 검토**
   - 법규 위반 가능성
   - 집행 가능성 문제
   - 잠재적 분쟁 유발 조항

[중점 검토 사항]
다음 7가지 사항에 특히 주의하여 검토하세요:
1. 임대차보호법 위반 소지가 있는 조항
2. 임대료 및 보증금 관련 불공정 조항
3. 임대인의 의무를 약화시키는 조항
4. 임차인에게 과도한 책임을 부과하는 조항
5. 계약 갱신 및 해지 관련 불리한 조항
6. 수선 및 유지보수 책임 분배의 불균형
7. 원상복구 의무의 범위가 모호하거나 과도한 조항

[각 문제 조항별 분석 요구사항]
각 문제가 있는 조항에 대해 다음을 포함하세요:
1. 문제점 지적 및 법적 위험 설명
2. 임대차보호법 등 관련법령 인용
3. 구체적인 수정안 제시
4. 수정 전/후 조항 비교
5. 협상 포인트 제시
6. 특정 조항의 의미, 법적 효력, 당사자에게 미치는 영향 분석
                                                          
**reason은 1-2줄로 간결하게 작성하세요.**

**부적절한 경우에만:**
- 위 법령 목록에서 가장 관련성 높은 법령 1개를 selected_law에 정확히 기재
- 위 판례 목록에서 가장 관련성 높은 서로 다른 사건의 판례 3개를 selected_cases에 정확히 기재
- 수정안과 협상 포인트 제시

{format_instructions}
""").partial(format_instructions=output_parser.get_format_instructions())

# 법령 요약 프롬프트
law_summary_prompt = ChatPromptTemplate.from_template("""
다음 법령 조문을 1문장으로 간단히 설명해주세요.

법령명: {law_title}
법령 내용: {law_content}

핵심 내용만 1문장으로 간결하게 설명하세요.
""")

# 판례 요약 프롬프트  
case_summary_prompt = ChatPromptTemplate.from_template("""
다음 판례가 해당 계약 조항과 어떤 관련성이 있는지 1-2문장으로 설명해주세요.

계약 조항: {clause_content}
판례 정보: {case_info}
판례 내용: {case_content}

이 판례가 해당 조항의 문제점과 어떤 연관이 있는지 간단히 설명하세요.
""")

# 조항별 분석 체인들
clause_analysis_chain = clause_analysis_prompt | llm | output_parser
law_summary_chain = law_summary_prompt | llm
case_summary_chain = case_summary_prompt | llm

class ContractAnalysisOrchestrator:
    """계약서 검토 오케스트레이터 (조항별 개별 분석 + 즉시 요약)"""
    
    def __init__(self):
        self.llm = llm
        self.clause_analysis_chain = clause_analysis_chain
        self.law_summary_chain = law_summary_chain
        self.case_summary_chain = case_summary_chain
        
        # 공통 서비스들 조립
        self.search_service = DocumentSearchService()
        self.legal_processor = LegalProcessor(self.llm)
        self.case_processor = CaseProcessor(self.llm)
        self.formatter = DocumentFormatter()
        
        # 🔧 별도 저장소 제거 (더 이상 필요 없음)
        # self.law_summaries = {}
        # self.case_summaries = {}  # {case_id: {"case": "...", "explanation": "..."}}
    
    def create_contract_summary(self, contract_data: dict) -> str:
        """계약서 요약 생성"""
        contract_info = extract_key_contract_info(contract_data)
        
        return f"""
계약유형: {contract_info.get('contract_type', '')}
부동산: {contract_info.get('address', '')}
보증금: {contract_info.get('deposit', 0):,}원
월세: {contract_info.get('monthly_rent', 0):,}원
계약기간: {contract_info.get('start_date', '')} ~ {contract_info.get('end_date', '')}
임대인: {contract_info.get('lessor_name', '')}
임차인: {contract_info.get('lessee_name', '')}
"""
    
    async def search_for_clause(self, clause_content: str) -> tuple:
        """개별 조항에 대한 RAG 검색 (법령 10개, 판례 10개)"""
        if not self.search_service.law_vectorstore:
            await self.search_service.load_vectorstores()
        
        # 조항 내용을 기반으로 검색 쿼리 생성
        search_query = f"임대차계약 조항 검토: {clause_content}"
        
        # 별도 스레드에서 벡터 검색 실행
        loop = asyncio.get_event_loop()
        
        # 법령 10개 검색
        law_docs = await loop.run_in_executor(
            None,
            lambda: self.search_service.law_vectorstore.similarity_search(search_query, k=10)
        )
        
        # 판례 10개 검색
        case_docs = await loop.run_in_executor(
            None,
            lambda: self.search_service.case_vectorstore.similarity_search(search_query, k=10)
        )
        
        return law_docs, case_docs
    
    def extract_case_id_from_doc_id(self, doc_id: str, case_name: str = "") -> int:
        """해시 기반으로 안전한 case_id 생성"""
        # case_name + doc_id 조합으로 고유성 최대화
        unique_str = f"{case_name}_{doc_id}".strip("_")
        
        # 해시 기반 ID 생성 (5자리 숫자)
        hash_value = abs(hash(unique_str)) % 100000
        
        # 0이 나오는 것을 방지 (최소 1000)
        return max(hash_value, 1000)

    def flexible_case_match(self, selected_case: str, doc_id: str, case_name: str) -> bool:
        """유연한 판례 매칭"""
        selected_case = selected_case.lower().strip()
        doc_id = doc_id.lower().strip()
        case_name = case_name.lower().strip()
        
        # 직접 매칭
        if (doc_id in selected_case or case_name in selected_case or
            selected_case in doc_id or selected_case in case_name):
            return True
        
        # 단어별 매칭 (더 유연함)
        selected_words = selected_case.split()
        doc_words = doc_id.split() + case_name.split()
        
        # 선택된 케이스의 주요 단어가 문서에 포함되는지
        matches = sum(1 for word in selected_words if any(word in doc_word for doc_word in doc_words))
        
        return matches >= max(1, len(selected_words) // 2)  # 절반 이상 매칭

    def extract_selected_documents(self, llm_result: SingleClauseAnalysisResult, law_docs: list, case_docs: list) -> tuple:
        """LLM이 선택한 법령/판례 문서 추출 + 중복 제거 + 개선된 매칭"""
        selected_law_doc = None
        selected_case_docs = []
        seen_case_names = set()
        
        # 선택된 법령 찾기
        if llm_result.selected_law:
            for doc in law_docs:
                law_name = doc.metadata.get('법령명', '')
                article = doc.metadata.get('조문번호', '')
                clause = doc.metadata.get('항번호', '')
                
                # 법령 문자열 매칭 (유연한 매칭 적용)
                doc_identifier = f"{law_name} 제{article}조"
                if clause:
                    doc_identifier += f" 제{clause}항"
                
                if doc_identifier in llm_result.selected_law or law_name in llm_result.selected_law:
                    selected_law_doc = doc
                    break
        
        # 선택된 판례들 찾기 (개선된 매칭 + 중복 제거)
        for selected_case in llm_result.selected_cases:
            if len(selected_case_docs) >= 3:  # 최대 3개
                break
                
            for doc in case_docs:
                doc_id = doc.metadata.get('doc_id', '')
                case_name = doc.metadata.get('case_name', '')
                
                # 사건명으로 중복 체크
                case_identifier = f"{case_name}_{doc_id}"
                if case_identifier in seen_case_names:
                    continue
                
                # 개선된 유연한 매칭
                if self.flexible_case_match(selected_case, doc_id, case_name):
                    selected_case_docs.append(doc)
                    seen_case_names.add(case_identifier)
                    break
        
        return selected_law_doc, selected_case_docs
    
    async def summarize_selected_documents(self, clause_content: str, selected_law_doc, selected_case_docs) -> tuple:
        """선택된 법령/판례 즉시 요약"""
        law_explanation = "법령 설명"
        law_content = "법령 내용"
        case_explanations = []
        
        # 법령 요약
        if selected_law_doc:
            try:
                law_name = selected_law_doc.metadata.get('법령명', '')
                article = selected_law_doc.metadata.get('조문번호', '')
                clause = selected_law_doc.metadata.get('항번호', '')
                
                law_title = f"{law_name} 제{article}조"
                if clause:
                    law_title += f" 제{clause}항"
                
                law_content = selected_law_doc.page_content.strip()
                
                law_response = await self.law_summary_chain.ainvoke({
                    "law_title": law_title,
                    "law_content": law_content
                })
                law_explanation = law_response.content.strip()
                
            except Exception as e:
                print(f"❌ 법령 요약 에러: {e}")
                law_explanation = "법령 요약 중 오류가 발생했습니다."
        
        # 판례 요약들
        for case_doc in selected_case_docs:
            try:
                case_name = case_doc.metadata.get('case_name', '')
                doc_id = case_doc.metadata.get('doc_id', '')
                case_content = case_doc.page_content.strip()[:500]  # 처음 500자만
                
                case_info = f"{case_name} ({doc_id})" if case_name else doc_id
                
                case_response = await self.case_summary_chain.ainvoke({
                    "clause_content": clause_content,
                    "case_info": case_info,
                    "case_content": case_content
                })
                case_explanation = case_response.content.strip()
                case_explanations.append(case_explanation)
                
            except Exception as e:
                print(f"❌ 판례 요약 에러: {e}")
                case_explanations.append("판례 요약 중 오류가 발생했습니다.")
        
        return law_explanation, law_content, case_explanations
    async def analyze_single_clause(self, clause_content: str, clause_type: str, contract_info: dict) -> ClauseAnalysis:
        """단일 조항 분석 + 상세 정보 바로 포함"""
        try:
            # 1. RAG 검색 (법령 10개, 판례 10개)
            law_docs, case_docs = await self.search_for_clause(clause_content)
            
            # 2. 검색 결과를 프롬프트용 문자열로 포맷팅
            related_laws_str = self.formatter.format_law_documents_detailed(law_docs)
            related_cases_str = self.formatter.format_case_documents_detailed(case_docs)
            
            # 3. 계약서 맥락 정보 생성
            contract_context = f"""
【계약서 기본 정보】
- 계약 기간: {contract_info.get('start_date', '미상')} ~ {contract_info.get('end_date', '미상')}
- 계약 유형: {contract_info.get('contract_type', '미상')}
- 보증금: {contract_info.get('deposit', 0):,}원
- 월세: {contract_info.get('monthly_rent', 0):,}원 (0원인 경우 전세)
- 부동산: {contract_info.get('address', '미상')}
"""
            
            # 4. LLM 분석 실행
            llm_result = await self.clause_analysis_chain.ainvoke({
                "clause_content": clause_content,
                "contract_context": contract_context,
                "related_laws_str": related_laws_str,
                "related_cases_str": related_cases_str
            })
            
            # 5. 결과 구성 - 🔧 상세 정보 바로 포함
            legal_basis = None
            case_basis = []
            
            if not llm_result.result:  # 부적절한 경우에만
                # LLM이 선택한 문서들 추출
                selected_law_doc, selected_case_docs = self.extract_selected_documents(llm_result, law_docs, case_docs)
                
                # 6. 선택된 문서들 즉시 요약
                law_explanation, law_content, case_explanations = await self.summarize_selected_documents(
                    clause_content, selected_law_doc, selected_case_docs
                )
                
                # 🔧 법령 정보 - 상세 정보 바로 포함
                if selected_law_doc:
                    law_id = selected_law_doc.metadata.get("법령ID", "") or selected_law_doc.metadata.get("law_id", "")
                    law_id_int = int(law_id) if law_id and law_id.isdigit() else 0
                    
                    legal_basis = ClauseLegalBasis(
                        law_id=law_id_int,
                        law=llm_result.selected_law or "관련 법령",
                        explanation=law_explanation,  # 🔧 바로 포함
                        content=law_content          # 🔧 바로 포함
                    )
                
                # 🔧 판례 정보 - 상세 정보 바로 포함
                for i, case_doc in enumerate(selected_case_docs):
                    doc_id = case_doc.metadata.get("doc_id", "")
                    case_name = case_doc.metadata.get("case_name", "")
                    
                    case_id_int = self.extract_case_id_from_doc_id(doc_id, case_name)
                    case_display = f"{case_name} ({doc_id})" if case_name else doc_id
                    case_explanation = case_explanations[i] if i < len(case_explanations) else "판례 요약 없음"
                    
                    case_basis.append(ClauseCaseBasis(
                        case_id=case_id_int,
                        case=case_display,
                        explanation=case_explanation,  # 🔧 바로 포함
                        link=f"data/case/{case_id_int}"  # 🔧 바로 포함
                    ))
            
            return ClauseAnalysis(
                result=llm_result.result,
                content=clause_content,
                reason=llm_result.reason,
                suggested_revision=llm_result.suggested_revision,
                negotiation_points=llm_result.negotiation_points,
                legal_basis=legal_basis,
                case_basis=case_basis
            )
            
        except Exception as e:
            print(f"❌ 조항 분석 에러: {e}")
            return ClauseAnalysis(
                result=True,  # 에러시 안전하게 적절로 처리
                content=clause_content,
                reason="분석 중 오류가 발생했습니다. 전문가 상담을 권장합니다.",
                suggested_revision=None,
                negotiation_points=None,
                legal_basis=None,
                case_basis=[]
            )
    
    async def analyze_contract(self, input_data: ContractAnalysisInput) -> ContractAnalysisOutput:
        """메인 실행 함수 - 🔧 전체 요약 제거"""
        start_time = time.time()
        
        try:
            # 1. 계약서 파싱
            contract_summary = self.create_contract_summary(input_data.contract_data)
            contract_info = extract_key_contract_info(input_data.contract_data)
            
            clauses = extract_contract_clauses(input_data.contract_data)
            articles = clauses.get("articles", [])
            agreements = clauses.get("agreements", [])
            
            # 2. 조항별 개별 분석 (병렬 처리)
            article_tasks = [
                self.analyze_single_clause(article, "article", contract_info) 
                for article in articles
            ]
            agreement_tasks = [
                self.analyze_single_clause(agreement, "agreement", contract_info) 
                for agreement in agreements
            ]
            
            # 병렬 실행
            article_results = await asyncio.gather(*article_tasks)
            agreement_results = await asyncio.gather(*agreement_tasks)
            
            # 3. 🔧 전체 요약 제거 - 이제 조항별로 상세 정보가 포함됨
            # (별도 저장소 관련 코드 제거)
            
            # 4. 추가 권고 특약 (임시로 빈 리스트)
            recommended_agreements = []
            
            # 5. 최종 결과 조립
            generation_time = round(time.time() - start_time, 2)
            
            return ContractAnalysisOutput(
                id=200,
                user_id=input_data.contract_data.get("user_id", 0),
                contract_id=input_data.contract_data.get("_id", 0),
                created_date=datetime.now().isoformat(),
                articles=article_results,
                agreements=agreement_results,
                recommended_agreements=recommended_agreements,
                # 🔧 전체 요약 제거
                # legal_basis=[],
                # case_basis=[],
                analysis_metadata=AnalysisMetadata(generation_time=generation_time)
            )
            
        except Exception as e:
            print(f"❌ 계약서 분석 에러: {e}")
            return self._create_fallback_result(input_data, start_time, e)
    
    def _create_fallback_result(self, input_data, start_time, error) -> ContractAnalysisOutput:
        """에러 시 안전한 폴백 결과 생성"""
        generation_time = round(time.time() - start_time, 2)
        
        return ContractAnalysisOutput(
            id=200,
            user_id=input_data.contract_data.get("user_id", 0),
            contract_id=input_data.contract_data.get("_id", 0),
            created_date=datetime.now().isoformat(),
            articles=[],
            agreements=[],
            recommended_agreements=[],
            # 🔧 전체 요약 제거
            # legal_basis=[],
            # case_basis=[],
            analysis_metadata=AnalysisMetadata(generation_time=generation_time)
        )

# 외부 API 호출용 함수
async def run_analysis_chain(input_data: ContractAnalysisInput) -> ContractAnalysisOutput:
    """계약서 검토 체인 실행"""
    orchestrator = ContractAnalysisOrchestrator()
    return await orchestrator.analyze_contract(input_data)