import zipfile
import xml.etree.ElementTree as ET
from langchain_core.tools import tool
import os # os 모듈 추가

@tool
def read_hwpx(file_path: str) -> str:
    """
    .hwpx 파일에서 본문 텍스트 추출하는 도구
    Args:
        file_path: .hwpx 파일 경로

    Returns:
        본문 텍스트 전체
    """

    print(f"read_hwpx tool called with file_path: {file_path}")

    try:
        # 파일 경로 정규화 (..\.. 같은 상대 경로 제거)
        normalized_file_path = os.path.normpath(file_path)
        print(f"Normalized file_path: {normalized_file_path}")

        with zipfile.ZipFile(normalized_file_path, 'r') as z:
            # 일반적으로 Contents/section0.xml 에 본문 내용이 있음
            target_xml_path = 'Contents/section0.xml'
            if target_xml_path not in z.namelist():
                return f"Error: .hwpx 파일 내부에 예상되는 본문 XML 파일({target_xml_path})이 없습니다."

            with z.open(target_xml_path) as xml_file:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                texts = []
                # 한글 문서의 텍스트는 보통 <hp:t> 태그 내에 있음
                # 네임스페이스를 고려하여 태그를 찾아야 함
                # 예: {http://www.hancom.co.kr/hwpml/2011/core}t
                for elem in root.iter():
                    # 태그 이름이 't'로 끝나고, 텍스트가 있는 경우
                    if elem.tag.endswith('}t') and elem.text:
                        texts.append(elem.text)
                
                if not texts:
                    return f"Error: .hwpx 파일({os.path.basename(normalized_file_path)})에서 텍스트를 추출하지 못했습니다. 본문 내용이 없거나 XML 구조가 예상과 다릅니다."
                
                return '\n'.join(texts)
    except FileNotFoundError:
        return f"Error: 파일을 찾을 수 없습니다: {os.path.basename(file_path)}"
    except zipfile.BadZipFile:
        return f"Error: 유효하지 않은 .hwpx 파일입니다 (손상되었거나 ZIP 형식이 아님): {os.path.basename(file_path)}"
    except ET.ParseError as e:
        return f"Error: .hwpx 파일 내부 XML 파싱 오류: {e} (파일: {os.path.basename(file_path)}"
    except Exception as e:
        return f"Error: .hwpx 파일 처리 중 알 수 없는 오류 발생: {e} (파일: {os.path.basename(file_path)})"
