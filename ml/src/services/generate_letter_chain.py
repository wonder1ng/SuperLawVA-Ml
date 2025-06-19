"""
[generate_letter_chain.py] - 내용증명 생성 체인 (수정된 버전)

공통 서비스들을 조립하여 내용증명 생성 기능을 구현
당사자 주소 정보 매칭 문제 해결
"""

import time
from datetime import datetime
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
#from langchain.output_parsers import PydanticOutputParser

# 공통 모듈들 import
from services.shared.document_search import DocumentSearchService
from services.shared.contract_parser import summarize_contract_for_letter, extract_parties_info
from services.shared.legal_processor import LegalProcessor, convert_to_legal_basis
from services.shared.case_processor import CaseProcessor, convert_to_case_basis
from services.shared.formatters import DocumentFormatter
from services.shared.llm_config import get_claude_llm_for_letter

# 스키마 import
from services.schema.letter_schema import (
    LetterGenerationInput, 
    LetterGenerationOutput,
    TempLetterOutput
)
from services.schema.shared_schema import PersonInfo, CertificationMetadata

# 내용증명 전용 LLM 설정
llm = get_claude_llm_for_letter()
output_parser = PydanticOutputParser(pydantic_object=TempLetterOutput)

# 내용증명 전용 프롬프트 템플릿 (수정됨)
letter_prompt = ChatPromptTemplate.from_template("""
당신은 25년 경력의 분쟁 해결 전문 변호사로, 내용증명을 통한 분쟁 조기 해결 성공률이 80%에 달하는 전문가입니다.  
법적 효력과 심리적 설득력을 모두 갖춘 전략적인 내용증명 문서를 작성해 주세요.                                                

관련 법령:
{related_laws_str}

관련 판례:
{related_cases_str}

계약 정보:
{contract_summary}

당사자 정보:
{parties_info}

🔍 **먼저 사용자 요청을 분석하세요:**

사용자 요청: {user_query}

**⚠️ 중요: 임대차 관련성 검증 필수**

위 사용자 요청이 임대차(주택임대, 상가임대, 보증금, 월세, 전세, 집주인, 세입자, 계약해지, 수리 등)와 관련이 없다면, 
아래 형식으로 안내 메시지를 JSON 형식으로 작성하세요:

```json
{{
  "title": "임대차 관련 질문 요청",
  "receiver_name": "시스템 안내",
  "receiver_address": "해당 없음",
  "receiver_detail_address": "",
  "sender_name": "내용증명 생성 시스템", 
  "sender_address": "해당 없음",
  "sender_detail_address": "",
  "body": "🚫 시스템 알림\\n\\n이 기능은 **임대차 관련 내용증명 생성 전용**입니다.\\n\\n현재 요청하신 \\"{user_query}\\"는 임대차와 관련이 없어 보입니다.\\n\\n**다시 임대차와 관련된 상황을 말씀해주세요:**\\n- 보증금/전세금을 안 돌려주는 문제\\n- 집주인이 수리를 안 해주는 문제\\n- 임대차 계약을 해지하고 싶은 문제\\n- 월세/관리비 관련 분쟁\\n- 기타 임대차 계약 위반 문제\\n\\n예시: \\"임차인인데 계약 끝났는데 보증금 500만원을 안 돌려줘서 내용증명 보내고 싶어요\\"",
  "strategy_summary": "임대차 관련 질문을 요청드립니다.",
  "followup_strategy": "임대차와 관련된 구체적인 상황을 다시 설명해주세요."
}}
```
**✅ 임대차 관련 요청인 경우에만 아래 정보로 실제 내용증명을 작성하세요:**

위 정보를 바탕으로 법적 효력이 있는 내용증명을 작성해주세요.                                                

**⚠️ 당사자 정보 작성 시 필수 준수사항:**
1. **수신인 정보**: 위 "당사자 정보"에서 "임대인" 이름, "임대인 주소", "임대인 상세주소"를 정확히 사용하세요
2. **발신인 정보**: 위 "당사자 정보"에서 "임차인" 이름, "임차인 주소", "임차인 상세주소"를 정확히 사용하세요  
3. **주소 분리**: receiver_address에는 기본 주소만, receiver_detail_address에는 상세주소만 입력하세요
4. **주소 정확성**: 임대부동산 주소와 당사자 실제 주소를 절대 혼동하지 마세요
5. **완전한 정보**: 이름, 주소, 상세주소를 모두 정확히 매칭하여 입력하세요                                                

**📝 어조 및 강도 설정:**
- 협력적, 정중한 어조
- 단호하지만 합리적 어조  
- 공식적, 객관적 어조

**📋 작성 필수 요소:**
1. 정확한 당사자 정보 (수신인/발신인 이름, 실제 주소)
2. 상황에 맞는 명확한 제목 (예: 보증금 반환 촉구서, 수리 요청서, 계약 해지 통보서)
3. 육하원칙 기반 구체적 사실관계 기술
4. 법적 근거를 포함한 명확한 요구사항
5. 합리적 이행 기한 명시
6. 상호 이익을 고려한 해결책 제안 (협의형인 경우)
7. 미이행시 후속 조치 안내 (강도에 따라 조절)
8. 발송 날짜 및 서명

**⚖️ 법적 안정성 확보:**
- 제시된 관련 법령이 있는 경우에만 해당 법령의 구체적 내용을 정확히 반영
- 관련 법령이 없거나 부족한 경우, 일반적인 법리와 상식선에서 논리적으로 작성
- 과도한 위협이나 불가능한 요구사항 배제
- 실제 우체국 내용증명 우편 발송 가능한 형식과 문체
- 객관적이고 감정적 표현 배제

**📋 법령 인용 필수 규칙 (Law Citation Rules):**
1. **완전한 법령명 사용 의무**: 법령을 인용할 때는 반드시 완전한 법령명을 「」 안에 명시하세요
   - ✅ 올바른 예: "「조세특례제한법 시행령」 제97조", "「주택임대차보호법」 제16조"
   - ❌ 잘못된 예: "같은 법 제97조", "동법 제16조", "상기 법률 제20조", "위 법령"

2. **축약 표현 금지**: 다음과 같은 축약 표현을 절대 사용하지 마세요
   - ❌ "같은 법", "동법", "상기 법률", "위 법령", "해당 법", "이 법"
   - ❌ "앞서 언급한 법률", "전술한 법령", "상기한 법"

3. **반복 인용 시에도 전체 법령명 사용**: 같은 법령을 여러 번 인용할 때도 매번 완전한 법령명을 사용하세요
   - ✅ 올바른 예: "「조세특례제한법」 제96조... 또한 「조세특례제한법」 제97조..."
   - ❌ 잘못된 예: "「조세특례제한법」 제96조... 또한 같은 법 제97조..."

4. **🚨 제시된 법령만 사용 (절대 준수)**: 
   - **반드시 위에 제시된 "관련 법령: {related_laws_str}" 목록에 있는 법령만 인용하세요**
   - **절대로 법령을 임의로 생성하거나 추가하지 마세요**
   - **관련 법령 목록이 "관련 법령을 찾을 수 없습니다"인 경우, 법령을 인용하지 마세요**
   - **검색되지 않은 법령은 존재하지 않는 것으로 간주하고 절대 언급 금지**

5. **법령명 정확성**: 법령명은 반드시 한국 법령 체계에 따라 정확하게 명시하세요
   - 기본: "「○○법」 제○조"
   - 항 포함: "「○○법」 제○조 제○항" 
   - 호 포함: "「○○법」 제○조 제○항 제○호"
   - 예시: "「주택임대차보호법」 제16조 제1항 제2호"
                       
🔴 **반드시 피해야 할 것들**:
- **🚨 절대 금지: 관련 법령 목록에 없는 법령 언급**
- **🚨 절대 금지: 법령 임의 생성 또는 추가**
- **🚨 절대 금지: "동법", "같은 법", "상기 법률" 등 축약 표현 사용**
- **🚨 절대 금지: 검색되지 않은 법령의 존재 가정**
- 임대부동산 주소와 당사자 주소 혼동
- 과도한 법적 위협
- 감정적이거나 주관적 표현

{format_instructions}
""").partial(format_instructions=output_parser.get_format_instructions())

# 내용증명 전용 체인
letter_chain = letter_prompt | llm | output_parser

class LetterGenerationOrchestrator:
    """내용증명 생성 오케스트레이터 (수정된 버전)"""
    
    def __init__(self):
        self.llm = llm
        self.letter_chain = letter_chain
        
        # 공통 서비스들 조립
        self.search_service = DocumentSearchService()
        self.legal_processor = LegalProcessor(self.llm)
        self.case_processor = CaseProcessor(self.llm)
        self.formatter = DocumentFormatter()
    
    def format_parties_info(self, lessor: dict, lessee: dict) -> str:
        """당사자 정보를 프롬프트용 문자열로 포맷팅"""
        return f"""
【임대인 정보】
- 이름: {lessor.get('name', '미상')}
- 주소: {lessor.get('address', '미상')}
- 상세주소: {lessor.get('detail_address', '')}
- 연락처: {lessor.get('mobile_number', lessor.get('phone_number', '미상'))}

【임차인 정보】
- 이름: {lessee.get('name', '미상')}
- 주소: {lessee.get('address', '미상')}
- 상세주소: {lessee.get('detail_address', '')}
- 연락처: {lessee.get('mobile_number', lessee.get('phone_number', '미상'))}

⚠️ 주의: 위 주소는 당사자들의 실제 거주지 주소입니다. 임대부동산 주소와 혼동하지 마세요!
⚠️ 출력 시 주소와 상세주소를 분리하여 기록하세요!
"""
    
    async def generate_letter(self, input_data: LetterGenerationInput) -> LetterGenerationOutput:
        """메인 실행 함수 (수정된 버전)"""
        start_time = time.time()
        
        try:
            # 1. 공통 유틸 사용 - 계약서 파싱
            contract_summary = summarize_contract_for_letter(input_data.contract_data)
            lessor, lessee = extract_parties_info(input_data.contract_data)
            user_query = input_data.user_query
            
            # 2. 당사자 정보 포맷팅
            parties_info = self.format_parties_info(lessor, lessee)
            
            # 3. 공통 서비스 사용 - 문서 검색
            law_docs, case_docs = await self.search_service.search_documents(user_query)

            # 4. 공통 유틸 사용 - 프롬프트용 포맷팅
            related_laws_str = self.formatter.format_law_documents(law_docs)
            related_cases_str = self.formatter.format_case_documents(case_docs)
            
            # 5. 내용증명 특화 - LLM 체인 실행
            temp_result = await self.letter_chain.ainvoke({
                "related_laws_str": related_laws_str,
                "related_cases_str": related_cases_str,
                "contract_summary": contract_summary,
                "parties_info": parties_info,
                "user_query": user_query
            })
            
            # ✅ 핵심 수정: 시스템 안내 메시지 체크 후 조기 반환
            if self._is_system_guidance_message(temp_result):
                return self._create_guidance_result(input_data, temp_result, start_time)
            
            # 6. 실제 내용증명인 경우에만 법령/판례 분석 진행
            referenced_laws = self.legal_processor.extract_referenced_laws(temp_result.body)
            
            # 7. 공통 서비스 사용 - 법령 분석
            legal_explanations = await self.legal_processor.generate_legal_explanations(
                referenced_laws, law_docs
            )
            legal_basis = convert_to_legal_basis(legal_explanations)
            
            # 8. 공통 서비스 사용 - 판례 분석 (내용증명용)
            case_summaries = await self.case_processor.generate_case_summaries_for_letter(
                case_docs, user_query, contract_summary
            )
            case_basis = convert_to_case_basis(case_summaries)
            
            # 9. 최종 결과 조립
            generation_time = round(time.time() - start_time, 2)
            
            return LetterGenerationOutput(
                id=100,
                user_id=input_data.contract_data.get("user_id"),
                contract_id=input_data.contract_data.get("_id"),
                created_date=datetime.now().isoformat(),
                title=temp_result.title,
                receiver=PersonInfo(
                    name=temp_result.receiver_name,
                    address=temp_result.receiver_address,
                    detail_address=temp_result.receiver_detail_address or ""
                ),
                sender=PersonInfo(
                    name=temp_result.sender_name,
                    address=temp_result.sender_address,
                    detail_address=temp_result.sender_detail_address or ""
                ),
                body=temp_result.body,
                strategy_summary=temp_result.strategy_summary,
                followup_strategy=temp_result.followup_strategy,
                legal_basis=legal_basis,
                case_basis=case_basis,
                certification_metadata=CertificationMetadata(
                    generation_time=generation_time
                ),
                user_query=user_query
            )
            
        except Exception as e:
            return self._create_fallback_result(input_data, start_time, e)

    def _is_system_guidance_message(self, temp_result: TempLetterOutput) -> bool:
        """시스템 안내 메시지인지 확인"""
        # 방법 1: receiver_name으로 판단
        if temp_result.receiver_name == "시스템 안내":
            return True
        
        # 방법 2: body 내용으로 판단 (더 안전한 방법)
        if "🚫 시스템 알림" in temp_result.body:
            return True
        
        # 방법 3: title로 판단
        if temp_result.title == "임대차 관련 질문 요청":
            return True
        
        return False

    def _create_guidance_result(self, input_data: LetterGenerationInput, temp_result: TempLetterOutput, start_time: float) -> LetterGenerationOutput:
        """시스템 안내 메시지 전용 결과 생성 (법령/판례 분석 없음)"""
        generation_time = round(time.time() - start_time, 2)
        
        return LetterGenerationOutput(
            id=100,
            user_id=input_data.contract_data.get("user_id"),
            contract_id=input_data.contract_data.get("_id"),
            created_date=datetime.now().isoformat(),
            title=temp_result.title,
            receiver=PersonInfo(
                name=temp_result.receiver_name,
                address=temp_result.receiver_address,
                detail_address=temp_result.receiver_detail_address or ""
            ),
            sender=PersonInfo(
                name=temp_result.sender_name,
                address=temp_result.sender_address,
                detail_address=temp_result.sender_detail_address or ""
            ),
            body=temp_result.body,
            strategy_summary=temp_result.strategy_summary,
            followup_strategy=temp_result.followup_strategy,
            legal_basis=[],  # ✅ 빈 배열로 설정
            case_basis=[],   # ✅ 빈 배열로 설정
            certification_metadata=CertificationMetadata(
                generation_time=generation_time
            ),
            user_query=input_data.user_query
        )
    
    def _create_fallback_result(self, input_data, start_time, error):
        """에러 시 안전한 폴백 결과 생성"""
        generation_time = round(time.time() - start_time, 2)
        
        return LetterGenerationOutput(
            id=None,
            user_id=None,
            contract_id=None,
            created_date=datetime.now().isoformat(),
            title="내용증명서",
            receiver=PersonInfo(name="수신자", address="주소 확인 필요"),
            sender=PersonInfo(name="발신인", address="주소 확인 필요"),
            body=f"사용자 요청: {input_data.user_query}\n\n시스템 오류로 기본 형식 생성됨",
            strategy_summary="시스템 오류 발생",
            followup_strategy="담당자 문의 바람",
            legal_basis=[],
            case_basis=[],
            certification_metadata=CertificationMetadata(
                generation_time=generation_time
            ),
            user_query=input_data.user_query
        )

# 외부 API 호출용 함수 (기존 호환성 유지)
async def run_letter_chain(input_data: LetterGenerationInput) -> LetterGenerationOutput:
    """기존 함수를 비동기로 변경 (수정된 버전)"""
    orchestrator = LetterGenerationOrchestrator()
    return await orchestrator.generate_letter(input_data)