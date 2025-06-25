import os
import time

import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv
from google.api_core import exceptions

load_dotenv()
# ✅ Gemini API 키 설정 (주의: 보안 필수)
genai.configure(
    api_key=os.getenv("GEMINI_KEY")
)  # <-- 실 서비스 시 환경변수 등으로 보호 권장
model = genai.GenerativeModel("gemini-1.5-flash")


def easy_explanation_with_retry(term, max_retries=3, delay_seconds=5):
    prompt = f"""
    [역할]
    당신은 주어진 법령 용어에 대해 신속하고 명확한 정보를 제공하는 법률 전문가 역할을 합니다. 부동산/임대차 계약 관련 분야에 특화된 전문가입니다.

    [지침]
    복잡한 법률 용어를 쉽게 풀어서 설명합니다.
    주어진 부동산/임대차 관련 용어 '{term}'의 정의를 초등학생도 이해할 수 있을 정도로 쉽게 1~2문장 이내로 설명해주세요. 
    {term}이 부동산/임대차와 관련된 용어가 아니라면, 최대한 부동산/임대차 분야에서 활용될 수 있는 상황을 예로 들어 설명해주세요. 
    """

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            if hasattr(response, "_error") and response._error:
                raise Exception(response._error)
            if not response.text.strip():
                if not response.candidates:
                    raise ValueError("API 응답에 내용이 없거나 유효한 후보가 없습니다.")
                raise ValueError("API 응답 텍스트가 비어있습니다.")
            return response.text.strip()

        except exceptions.ResourceExhausted as e:
            print(
                f"[{term}] Rate limit exceeded (Attempt {attempt + 1}/{max_retries}). Retrying in {delay_seconds}s..."
            )
            time.sleep(delay_seconds)
            delay_seconds *= 2
        except Exception as e:
            print(
                f"[{term}] Error generating explanation (Attempt {attempt + 1}/{max_retries}): {e}"
            )
            if attempt < max_retries - 1:
                print(f"Retrying in {delay_seconds}s...")
                time.sleep(delay_seconds)
                delay_seconds *= 2
            else:
                print(f"[{term}] Max retries reached. Skipping.")
                return "설명 생성 실패 (오류 발생)."
    return "설명 생성 실패 (재시도 한도 초과)."


def process_and_continue_from_index(
    input_filename,
    term_column="용어",
    start_index=10200,
    output_filename="gemini_final_terms_explained.csv",
    chunk_size=50,
):
    temp_output_filename = output_filename + ".temp"

    try:
        df = pd.read_csv(input_filename, encoding="utf-8-sig")
        print(f"'{input_filename}' 파일 로드 완료. 총 {len(df)}개 용어.")
    except Exception as e:
        print(f"[오류] 파일 로드 실패: {e}")
        return

    if term_column not in df.columns:
        print(f"[오류] '{term_column}' 컬럼이 없습니다.")
        return

    if "쉬운 설명" not in df.columns:
        df["쉬운 설명"] = ""

    total_terms = len(df)

    print(
        f"\n👉 {start_index+1}번째 용어부터 설명 생성 시작합니다. 총 {total_terms - start_index}개 처리 예정.\n"
    )

    for i in range(start_index, total_terms):
        term = df.loc[i, term_column]
        print(f"[{i+1}/{total_terms}] 용어 '{term}' 설명 생성 중...")

        explanation = easy_explanation_with_retry(term)
        df.loc[i, "쉬운 설명"] = explanation

        if (i + 1) % chunk_size == 0 or (i + 1) == total_terms:
            df.to_csv(temp_output_filename, index=False, encoding="utf-8-sig")
            os.replace(temp_output_filename, output_filename)
            print(f"✅ {i+1}개 완료 → '{output_filename}'에 중간 저장됨")
            time.sleep(10)

    print("\n🎉 모든 설명 생성 완료!")
    print("📄 최종 결과 미리보기:")
    print(df.tail())
    print(
        f"총 설명된 용어 수: {df['쉬운 설명'].apply(lambda x: isinstance(x, str) and x.strip() != '').sum()}개"
    )


# --- 실행부 ---
input_file = "onlyterm.csv"  # ← ✅ 새로운 입력 파일명 반영
output_file = "D:/뉴gemini_final_terms_explained.csv"  # ← ✅ 결과 파일 안전 저장

process_and_continue_from_index(
    input_filename=input_file,
    term_column="용어",
    start_index=55912,
    output_filename=output_file,
    chunk_size=50,
)
