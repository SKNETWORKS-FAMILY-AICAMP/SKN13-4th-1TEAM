# csv_loader.py
"""
본 파일은 dataset에 있는 csv파일을 모두 읽고,
chroma_db를 구축하는 파일입니다.
chroma_db를 구축했으면 이 파일을 실행시키지 마시오.
중간에 설치에 실패했을 경우, 
chroma_db 폴더를 삭제 후, 다시 이 파일을 실행시키시오.
"""


import os
import glob
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma

load_dotenv()

def build_chroma_vector_store(data_dir: str = "dataset",
                              persist_dir: str = "chroma_db",
                              chunk_size: int = 100):

    pattern = os.path.join(data_dir, "*.csv")
    csv_file_paths = glob.glob(pattern)

    all_csv_docs = []
    for path in csv_file_paths:
        loader = CSVLoader(
            file_path=path,
            csv_args={'delimiter': ","},
            encoding='utf-8',
            content_columns=["질문","본문"]
        )
        docs = loader.load()
        all_csv_docs.extend(docs)

    embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

    # Chroma 생성 or 불러오기
    vector_store = Chroma(
        embedding_function=embedding_model,
        collection_name="QnA",
        persist_directory=persist_dir
        )

    # 문서 삽입
    for i in range(0, len(all_csv_docs), chunk_size):
        chunk = all_csv_docs[i:i+chunk_size]
        vector_store.add_documents(chunk)
        print(f"🔹{i+1}~{min(i+chunk_size, len(all_csv_docs))} 문서 Chroma에 저장 완료")    # 14637

    # 디스크에 저장
    print(f"✅ 저장 완료 → {persist_dir}")

build_chroma_vector_store()