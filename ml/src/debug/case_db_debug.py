"""
Description: 
판례 Chroma 벡터 DB의 상태를 상세히 점검하고, 컬렉션 연결 여부 및 검색 가능 여부를 확인하는 로컬 디버깅 스크립트입니다.  
ChromaDB에 직접 연결하거나 LangChain-Chroma wrapper를 통해 접근하여 상태 정보를 출력합니다.
[추가] 벡터스토어 컬렉션명 전용 확인 기능

Author: ooheunsu  
Date: 2025-06-16  
Requirements: chromadb, langchain_openai, langchain_chroma, python-dotenv
"""

import os

import chromadb
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# 환경변수 로드
load_dotenv()


def get_all_collection_names(db_path):
    """벡터스토어의 모든 컬렉션명 반환"""
    print("🏷️ === 컬렉션명 확인 ===")

    try:
        client = chromadb.PersistentClient(path=db_path)
        collections = client.list_collections()

        collection_names = [col.name for col in collections]

        print(f"📊 총 컬렉션 수: {len(collection_names)}")
        if collection_names:
            print("📋 발견된 컬렉션명 목록:")
            for i, name in enumerate(collection_names, 1):
                print(f"  {i}. '{name}'")
        else:
            print("❌ 컬렉션이 존재하지 않습니다.")

        return collection_names

    except Exception as e:
        print(f"❌ 컬렉션명 확인 실패: {e}")
        print("💡 가능한 원인:")
        print("  - DB 경로가 잘못됨")
        print("  - ChromaDB 파일이 손상됨")
        print("  - 권한 문제")
        return []


def find_matching_collections(db_path, pattern=""):
    """특정 패턴과 일치하는 컬렉션명 검색"""
    print(f"🔍 === '{pattern}' 패턴 컬렉션 검색 ===")

    try:
        client = chromadb.PersistentClient(path=db_path)
        collections = client.list_collections()

        matching = []
        for col in collections:
            if pattern.lower() in col.name.lower():
                matching.append(
                    {"name": col.name, "count": col.count(), "metadata": col.metadata}
                )

        if matching:
            print(f"✅ '{pattern}' 패턴과 일치하는 컬렉션 {len(matching)}개 발견:")
            for match in matching:
                print(f"  📋 '{match['name']}' - {match['count']}개 데이터")
        else:
            print(f"❌ '{pattern}' 패턴과 일치하는 컬렉션이 없습니다.")

        return matching

    except Exception as e:
        print(f"❌ 패턴 검색 실패: {e}")
        return []


def debug_case_db():
    """판례 DB 상태 상세 확인"""
    print("🔍 === 판례 DB 디버깅 시작 ===")

    # 1. 환경변수 확인
    case_db_path = os.getenv(
        "CHROMA_CASE_DB_PATH", "./vectordb/chroma_case/chroma_openai_case"
    )
    case_collection_name = os.getenv("CASE_COLLECTION_NAME", "case_collection")

    print(f"📁 판례 DB 경로: {case_db_path}")
    print(f"📋 판례 컬렉션명: {case_collection_name}")
    print(f"🗂️ 경로 존재 여부: {os.path.exists(case_db_path)}")

    if not os.path.exists(case_db_path):
        print("❌ DB 경로가 존재하지 않습니다!")
        return None, 0

    # 2. 경로 내 파일들 확인
    print(f"\n📂 경로 내 파일/폴더 목록:")
    try:
        items = os.listdir(case_db_path)
        for item in items:
            item_path = os.path.join(case_db_path, item)
            if os.path.isdir(item_path):
                print(f"  📁 {item}/")
                # 하위 폴더도 확인
                try:
                    sub_items = os.listdir(item_path)
                    for sub_item in sub_items[:5]:  # 처음 5개만
                        print(f"    📄 {sub_item}")
                    if len(sub_items) > 5:
                        print(f"    ... 및 {len(sub_items)-5}개 더")
                except:
                    pass
            else:
                file_size = os.path.getsize(item_path)
                print(f"  📄 {item} ({file_size} bytes)")
    except Exception as e:
        print(f"❌ 파일 목록 읽기 실패: {e}")

    # 3. 컬렉션명 전용 확인
    print(f"\n" + "=" * 50)
    collection_names = get_all_collection_names(case_db_path)
    print("=" * 50)

    # 4. 'case' 패턴 검색
    if collection_names:
        print(f"\n" + "=" * 50)
        case_collections = find_matching_collections(case_db_path, "case")
        print("=" * 50)

    # 5. ChromaDB 직접 연결 상세 정보
    print(f"\n🔗 ChromaDB 직접 연결 상세 정보...")
    try:
        client = chromadb.PersistentClient(path=case_db_path)
        collections = client.list_collections()

        print(f"📊 발견된 컬렉션 수: {len(collections)}")
        for i, collection in enumerate(collections):
            print(f"  {i+1}. 컬렉션명: '{collection.name}'")
            print(f"     데이터 개수: {collection.count()}")
            print(f"     메타데이터: {collection.metadata}")

            # 샘플 데이터 확인 (첫 3개)
            if collection.count() > 0:
                try:
                    sample = collection.peek(limit=3)
                    print(
                        f"     샘플 ID: {sample['ids'][:3] if sample['ids'] else 'None'}"
                    )
                    if sample["metadatas"]:
                        print(
                            f"     샘플 메타데이터: {sample['metadatas'][0] if sample['metadatas'][0] else 'None'}"
                        )
                except Exception as e:
                    print(f"     샘플 데이터 확인 실패: {e}")
            print()

    except Exception as e:
        print(f"❌ ChromaDB 직접 연결 실패: {e}")

    # 6. LangChain Chroma로 연결 시도 (실제 발견된 컬렉션명들 + 예상 이름들)
    print(f"\n🔗 LangChain Chroma 연결 시도...")
    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

        # 실제 발견된 컬렉션명들 + 예상되는 이름들
        possible_names = list(
            set(
                collection_names
                + [
                    case_collection_name,  # 환경변수 값
                    "case_collection",  # 기본값
                    "case_chunks_openai",  # 법령과 유사한 패턴
                    "cases",  # 간단한 이름
                    "판례",  # 한글
                ]
            )
        )

        for name in possible_names:
            try:
                print(f"  📋 '{name}' 컬렉션으로 연결 시도...")
                case_db = Chroma(
                    persist_directory=case_db_path,
                    embedding_function=embeddings,
                    collection_name=name,
                )

                count = case_db._collection.count()
                print(f"  ✅ 연결 성공! 데이터 개수: {count}개")

                if count > 0:
                    print(f"  🎯 판례 DB 발견! 컬렉션명: '{name}'")

                    # 샘플 검색 테스트
                    try:
                        sample_results = case_db.similarity_search("계약", k=2)
                        print(f"  📝 샘플 검색 결과: {len(sample_results)}개")
                        if sample_results:
                            print(
                                f"  📄 첫 번째 결과 (처음 100자): {sample_results[0].page_content[:100]}..."
                            )
                    except Exception as e:
                        print(f"  ⚠️ 샘플 검색 실패: {e}")

                    return name, count  # 성공한 컬렉션 정보 반환

            except Exception as e:
                print(f"  ❌ '{name}' 연결 실패: {e}")

    except Exception as e:
        print(f"❌ LangChain Chroma 연결 실패: {e}")

    print(f"\n🔍 === 판례 DB 디버깅 완료 ===")
    return None, 0


def quick_collection_check(db_path):
    """빠른 컬렉션명 확인 (단순 출력용)"""
    print("⚡ === 빠른 컬렉션명 확인 ===")
    try:
        client = chromadb.PersistentClient(path=db_path)
        collections = client.list_collections()

        if collections:
            names = [col.name for col in collections]
            print(f"컬렉션명: {names}")
            return names
        else:
            print("컬렉션 없음")
            return []
    except Exception as e:
        print(f"확인 실패: {e}")
        return []


if __name__ == "__main__":
    # 기본 디버깅 실행
    result_name, result_count = debug_case_db()

    # 빠른 확인도 실행
    print(f"\n" + "=" * 50)
    case_db_path = os.getenv(
        "CHROMA_CASE_DB_PATH", "./vectordb/chroma_case/chroma_openai_case"
    )
    quick_collection_check(case_db_path)
