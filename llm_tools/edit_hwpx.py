import base64
import zipfile
import os
import tempfile
import xml.etree.ElementTree as ET
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

@tool
def edit_hwpx(hwpx_base64: str, instruction: str) -> str:
    """
    HWPX 파일을 base64 인코딩으로 받아, LangChain LLM을 통해 텍스트를 수정하고,
    수정된 내용을 반영한 새 HWPX 파일을 base64로 반환합니다.
    """
    
    print(f"edit_hwpx tool called: ")

    # 1. 임시 폴더 생성
    with tempfile.TemporaryDirectory() as tmpdir:
        hwpx_path = os.path.join(tmpdir, "input.hwpx")

        # 2. base64 → 바이너리 저장
        with open(hwpx_path, "wb") as f:
            f.write(base64.b64decode(hwpx_base64))

        # 3. 압축 해제
        unzip_dir = os.path.join(tmpdir, "unzipped")
        with zipfile.ZipFile(hwpx_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_dir)

        # 4. section*.xml 텍스트 추출
        content_dir = os.path.join(unzip_dir, "Contents")
        texts = []
        section_path = None

        for fname in os.listdir(content_dir):
            if fname.startswith("section") and fname.endswith(".xml"):
                section_path = os.path.join(content_dir, fname)
                tree = ET.parse(section_path)
                root = tree.getroot()

                for elem in root.iter():
                    if elem.tag.endswith("t") and elem.text:
                        texts.append(elem.text.strip())

                break  # 첫 section만 처리

        if not section_path or not texts:
            return "❌ 유효한 텍스트가 포함된 HWPX section 파일을 찾을 수 없습니다."

        full_text = "\n".join(texts)

        # 5. LLM 호출
        prompt = f"""다음은 한글 문서 내용입니다.

[원문]
{full_text}

[요청]
{instruction}

[결과]
"""
        response = llm.invoke(prompt).strip()

        # 6. 수정된 텍스트로 다시 삽입
        new_lines = response.splitlines()
        new_tree = ET.parse(section_path)
        new_root = new_tree.getroot()
        line_idx = 0

        for elem in new_root.iter():
            if elem.tag.endswith("t") and elem.text and line_idx < len(new_lines):
                elem.text = new_lines[line_idx].strip()
                line_idx += 1

        # 7. XML 저장
        new_tree.write(section_path, encoding="utf-8", xml_declaration=True)

        # 8. 다시 압축
        new_hwpx_path = os.path.join(tmpdir, "output.hwpx")
        with zipfile.ZipFile(new_hwpx_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root_dir, _, files in os.walk(unzip_dir):
                for file in files:
                    full_path = os.path.join(root_dir, file)
                    rel_path = os.path.relpath(full_path, unzip_dir)
                    zipf.write(full_path, rel_path)

        # 9. base64로 인코딩
        with open(new_hwpx_path, "rb") as f:
            encoded_result = base64.b64encode(f.read()).decode("utf-8")

        return encoded_result
