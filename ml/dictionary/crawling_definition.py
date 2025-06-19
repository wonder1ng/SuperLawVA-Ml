import requests
from bs4 import BeautifulSoup
import csv
import time
import json # 디버깅 시 응답 구조 확인용
import os
from dotenv import load_dotenv

load_dotenv()

# --- API 설정 (!!! 반드시 본인의 유효한 API 키로 변경하세요 !!!) ---
LAW_API_KEY = os.getenv("LAW_API_KEY") # <<<<< 여기에 실제 발급받은 키를 넣으세요!

# 1단계: 법령용어 목록 조회 엔드포인트
LIST_API_BASE_URL = "http://www.law.go.kr/DRF/lawSearch.do"

# 2단계: 법령용어 상세 조회 엔드포인트 (각 용어의 정의를 가져옴)
DETAIL_API_BASE_URL = "http://www.law.go.kr/DRF/lawService.do"

# --- 1단계 함수: 모든 법령 용어의 메타데이터 (ID와 용어명) 수집 ---
def get_all_legal_term_metadata():
    """
    법제처 API에서 모든 법령 용어의 용어명과 ID를 페이지네이션으로 수집합니다.
    """
    all_term_metadata = []
    page_num = 1
    # API 문서에서 lstrm의 display 최대값 확인 후 설정 (일반적으로 100)
    per_page_display = 100 
    
    print(f"1단계: 법령 용어 메타데이터 수집 시작 (BASE_URL: {LIST_API_BASE_URL})")

    while True:
        params = {
            "OC": LAW_API_KEY,
            "target": "lstrm",     # 법령용어 목록 조회
            "type": "XML",         # 응답 형식 XML
            "display": per_page_display,
            "page": page_num
        }
        
        print(f"[1단계 수집 중] 페이지 {page_num} 요청...")
        
        try:
            response = requests.get(LIST_API_BASE_URL, params=params)
            response.raise_for_status()
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.content, "xml")

            # API 오류 메시지 확인
            error_message_tag = soup.find("ErrorMessage")
            if error_message_tag:
                print(f"[1단계 오류] API 응답: {error_message_tag.text}")
                break

            law_search_container = soup.find("LsTrmSearch")
            if not law_search_container:
                print("[1단계 오류] 'LsTrmSearch' 태그를 찾을 수 없습니다. 응답 구조를 확인해주세요.")
                print(response.text[:500]) # 디버깅용 응답 내용 출력
                break

            terms_elements = law_search_container.find_all("lstrm")

            if not terms_elements:
                print(f"[1단계 완료] 페이지 {page_num}에 더 이상 용어가 없습니다. 메타데이터 수집 종료.")
                break # 더 이상 데이터가 없으면 루프 종료

            for item_element in terms_elements:
                term_id = item_element.find("법령용어ID").get_text(strip=True) if item_element.find("법령용어ID") else "N/A_ID"
                term_name = item_element.find("법령용어명").get_text(strip=True) if item_element.find("법령용어명") else "N/A_NAME"
                
                all_term_metadata.append({
                    "법령용어ID": term_id,
                    "법령용어명": term_name
                })
            
            print(f"[1단계 진행] {page_num}페이지 완료. 현재까지 누적 용어 메타데이터: {len(all_term_metadata)}개")
            page_num += 1
            time.sleep(0.1) # 서버 부하를 줄이기 위해 잠시 대기

        except requests.exceptions.RequestException as e:
            print(f"[1단계 오류] 네트워크 요청 중 오류 발생: {e}")
            break
        except Exception as e:
            print(f"[1단계 오류] 데이터 파싱 또는 처리 중 알 수 없는 오류: {e}")
            print(f"오류 발생 페이지: {page_num}")
            # print(response.text[:1000]) # 디버깅용 응답 내용 출력
            break
            
    return all_term_metadata

# --- 2단계 함수: 특정 법령용어 ID로 상세 정의 가져오기 ---
def get_legal_term_definition_by_id(term_id):
    """
    주어진 법령용어ID를 사용하여 해당 용어의 상세 정의를 가져옵니다.
    """
    params = {
        "OC": LAW_API_KEY,
        "target": "lstrm", # 법령용어 상세 조회
        "trmSeqs": term_id,     # 조회할 법령용어ID
        "type": "XML"      # 응답 형식 XML
    }

    try:
        response = requests.get(DETAIL_API_BASE_URL, params=params)
        response.raise_for_status()
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.content, "xml")

        error_message_tag = soup.find("ErrorMessage")
        if error_message_tag:
            # print(f"[2단계 오류] ID {term_id} 상세 조회 오류: {error_message_tag.text}")
            return None # 오류 발생 시 None 반환

        ls_trm_service_container = soup.find("LsTrmService") 
        
        if ls_trm_service_container:
            definition = ls_trm_service_container.find("법령용어정의").get_text(strip=True) \
                         if ls_trm_service_container.find("법령용어정의") else "정의 없음"
            return definition
        else:
            print(f"[2단계 오류] ID {term_id}: 'LsTrmService' 태그를 찾을 수 없습니다. 응답 구조 확인 필요.")
            # print(response.text[:500]) # 디버깅용 응답 내용 출력
            return None # 예상치 못한 구조이므로 None 반환

    except requests.exceptions.RequestException as e:
        # print(f"[2단계 오류] ID {term_id} 네트워크 요청 오류: {e}") # 주석 해제하여 디버깅
        return None
    except Exception as e:
        # print(f"[2단계 오류] ID {term_id} 데이터 파싱 오류: {e}") # 주석 해제하여 디버깅
        # print(response.text[:500]) # 오류 시 원본 응답 확인
        return None

def save_to_csv(data, filename="legal_terms_with_definitions.csv"):
    """
    크롤링한 데이터를 CSV 파일로 저장합니다.
    """
    if not data:
        print("저장할 데이터가 없습니다.")
        return
    
    # CSV 필드명
    fieldnames = ["용어명", "용어정의", "법령용어ID"] # 용어명, 정의, ID 포함

    with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"\n[저장 완료] CSV 파일 생성: {filename}. 총 {len(data)}개의 용어 정의 저장.")

# --- 메인 실행 ---
if __name__ == "__main__":
    # 1단계: 모든 법령 용어의 ID와 이름을 가져옵니다.
    print("======== 1단계: 법령 용어 메타데이터 수집 ========")
    term_metadata_list = get_all_legal_term_metadata()
    
    if not term_metadata_list:
        print("메타데이터를 수집하지 못했습니다. 크롤링을 종료합니다.")
    else:
        print(f"\n총 {len(term_metadata_list)}개의 용어 메타데이터를 수집했습니다.")
        print("======== 2단계: 각 용어의 상세 정의 수집 ========")
        
        final_legal_terms_data = []
        
        for idx, term_meta in enumerate(term_metadata_list):
            term_id = term_meta["법령용어ID"]
            term_name = term_meta["법령용어명"]
            
            # 너무 많은 요청을 방지하기 위해 일정 간격으로 출력
            if (idx + 1) % 50 == 0 or idx == len(term_metadata_list) - 1:
                print(f"[2단계 수집 중] {idx+1}/{len(term_metadata_list)} 용어 처리 중: '{term_name}' (ID: {term_id})")

            definition = get_legal_term_definition_by_id(term_id)
            
            if definition is not None: # 정의를 가져오는 데 성공한 경우 (None은 오류 발생)
                final_legal_terms_data.append({
                    "법령용어명": term_name,
                    "용어정의": definition,
                    "법령용어ID": term_id
                })
            else:
                # 정의를 가져오지 못한 경우 (API 오류 등), 정의를 'N/A'로 표시하거나 스킵할 수 있습니다.
                print(f"[경고] 용어 '{term_name}' (ID: {term_id})의 정의를 가져오지 못했습니다. 스킵 또는 'N/A' 처리.")
                final_legal_terms_data.append({
                    "법령용어명": term_name,
                    "용어정의": "정의를 가져오지 못함 (오류)",
                    "법령용어ID": term_id
                })
            
            time.sleep(0.05) # 각 상세 요청 사이에 짧은 지연 시간 추가 (서버 부하 경감)
                            # 너무 많은 요청 시 API 제한에 걸릴 수 있으므로 조절 필요.

        # 최종 데이터 CSV 저장
        save_to_csv(final_legal_terms_data, "all_law_terms_with_definitions.csv")
    
    print("\n============= 모든 크롤링 프로세스 종료 =============")