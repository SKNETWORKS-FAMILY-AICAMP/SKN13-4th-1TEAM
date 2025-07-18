import time
from typing import Optional, Dict, Any
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import tool

@tool
def RAG_tool(query: str, filter: Optional[Dict[str, Any]] = None) -> str:
    """
    [Instruction]
    한국 문화유산 검색을 위한 RAG 툴입니다.
    이 툴은 Chroma vector DB에서 관련 문화유산 설명을 검색하여 반환합니다.
    사용자의 질문에 답변하기 위해 문화유산 데이터베이스에 접근이 필요할 때 호출하세요.
    
    [Args]
    content는 다음과 같은 컬럼으로 이루어져 있습니다:

    - 종목: 문화유산의 법적 구분 (예: 국보, 보물, 등록문화재 등)
    - 명칭: 문화유산의 이름 또는 제목
    - 소재지: 문화유산이 위치한 지역 또는 주소 (예: 서울특별시 종로구)
    - 관리자: 문화유산을 관리하는 기관 또는 담당자
    - 분류: 문화유산의 유형 분류 (예: 사적, 기념물, 중요민속자료 등)
    - 수량/면적: 문화유산의 규모 또는 수량 정보 (예: 1기, 3동, 153㎡ 등)
    - 지정(등록)일: 문화유산로 지정되거나 등록된 날짜
    - 소재지(상세): 문화유산의 상세 주소 또는 세부 위치 정보
    - 시대: 문화유산이 만들어지거나 사용된 역사적 시기 (예: 고려, 조선 후기, 삼국시대 등)
    - 소유자(소유단체): 해당 문화유산의 소유자나 소유 기관
    - 관리자(관리단체): 해당 문화유산의 실질적인 관리 책임을 지는 기관 또는 단체
    - 설명: 문화유산에 대한 상세한 설명, 역사적 배경, 가치, 특징 등을 포함한 본문 정보
    """
    vector_store = Chroma(
        collection_name="heritage_collection", 
        embedding_function=OpenAIEmbeddings(model="text-embedding-3-large"), 
        persist_directory="../chroma_db"
    )

    retriever = vector_store.as_retriever(search_kwargs={"k":10})
    print(f"retiever tool called: {query}")
    docs = retriever.invoke(query)

    result = "\n\n".join([doc.page_content for doc in docs])
    return result[:3000]  # 너무 길어지는 것 방지
