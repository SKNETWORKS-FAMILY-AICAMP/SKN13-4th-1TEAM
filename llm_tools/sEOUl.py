# seoul.py

import os
from langchain_core.tools import tool
import requests
import xml.etree.ElementTree as ET

SEOUL_OPEN_API_KEY=os.getenv("SEOUL_OPEN_API_KEY")

@tool
def get_data_seoul(AREA_NM:str):
    """
[Instructions]
서울 실시간 도시데이터 MCP 도구 설명서
서울 실시간 도시데이터 도구는 서울의 주요 장소 120곳에 대해 인구, 상권, 교통, 환경 등 11개 실시간 데이터를 제공합니다. 각 도구는 공통적으로 아래 인자들을 사용합니다.

[Input]
다음 장소만 조회 가능합니다. 잘못된 장소명을 입력하면 오류가 발생합니다:

강남 MICE 관광특구
동대문 관광특구
명동 관광특구
이태원 관광특구
잠실 관광특구
종로·청계 관광특구
홍대 관광특구
경복궁
광화문·덕수궁
보신각
서울 암사동 유적
창덕궁·종묘
가산디지털단지역
강남역
건대입구역
고덕역
고속터미널역
교대역
구로디지털단지역
구로역
군자역
대림역
동대문역
뚝섬역
미아사거리역
발산역
사당역
삼각지역
서울대입구역
서울식물원·마곡나루역
서울역
선릉역
성신여대입구역
수유역
신논현역·논현역
신도림역
신림역
신촌·이대역
양재역
역삼역
연신내역
오목교역·목동운동장
왕십리역
용산역
이태원역
장지역
장한평역
천호역
총신대입구(이수)역
충정로역
합정역
혜화역
홍대입구역(2호선)
회기역
가락시장
가로수길
광장(전통)시장
김포공항
노량진
덕수궁길·정동길
북촌한옥마을
서촌
성수카페거리
쌍문역
압구정로데오거리
여의도
연남동
영등포 타임스퀘어
용리단길
이태원 앤틱가구거리
인사동
창동 신경제 중심지
청담동 명품거리
청량리 제기동 일대 전통시장
해방촌·경리단길
DDP(동대문디자인플라자)
DMC(디지털미디어시티)
강서한강공원
고척돔
광나루한강공원
광화문광장
국립중앙박물관·용산가족공원
난지한강공원
남산공원
노들섬
뚝섬한강공원
망원한강공원
반포한강공원
북서울꿈의숲
서리풀공원·몽마르뜨공원
서울광장
서울대공원
서울숲공원
아차산
양화한강공원
어린이대공원
여의도한강공원
월드컵공원
응봉산
이촌한강공원
잠실종합운동장
잠실한강공원
잠원한강공원
청계산
청와대
북창동 먹자골목
남대문시장
익선동
신정네거리역
잠실새내역
잠실역
잠실롯데타워 일대
송리단길·호수단길
신촌 스타광장
보라매공원
서대문독립공원
안양천
여의서로
올림픽공원
홍제폭포

[Output]
■ 공통 정보
list_total_count : 총 데이터 건수 (정상 조회 시 출력됨)
RESULT.CODE : 요청 결과 코드 (성공/실패 여부 등)
RESULT.MESSAGE : 요청 결과 메시지 (상세 설명 포함)

■ 핫스팟 인구 및 혼잡도 정보
AREA_NM : 핫스팟 장소명
AREA_CD : 핫스팟 코드명
LIVE_PPLTN_STTS : 실시간 인구 현황
AREA_CONGEST_LVL : 장소 혼잡도 지표 (1~4단계 등급)
AREA_CONGEST_MSG : 장소 혼잡도 관련 메시지
AREA_PPLTN_MIN : 실시간 인구 지표 최소값
AREA_PPLTN_MAX : 실시간 인구 지표 최대값
MALE_PPLTN_RATE : 남성 인구 비율 (%)
FEMALE_PPLTN_RATE : 여성 인구 비율 (%)
PPLTN_RATE_0 : 0~10세 인구 비율
PPLTN_RATE_10 : 10대 인구 비율
PPLTN_RATE_20 : 20대 인구 비율
PPLTN_RATE_30 : 30대 인구 비율
PPLTN_RATE_40 : 40대 인구 비율
PPLTN_RATE_50 : 50대 인구 비율
PPLTN_RATE_60 : 60대 인구 비율
PPLTN_RATE_70 : 70대 이상 인구 비율
RESNT_PPLTN_RATE : 상주 인구 비율
NON_RESNT_PPLTN_RATE : 비상주 인구 비율
REPLACE_YN : 대체 데이터 여부
PPLTN_TIME : 실시간 인구 데이터 업데이트 시간
FCST_YN : 예측값 제공 여부
FCST_PPLTN : 인구 예측값
FCST_TIME : 인구 예측 시점
FCST_CONGEST_LVL : 장소 예측 혼잡도 지표
FCST_PPLTN_MIN : 예측 인구 지표 최소값
FCST_PPLTN_MAX : 예측 인구 지표 최대값

■ 도로 소통 정보
ROAD_TRAFFIC_STTS : 도로 소통 현황
ROAD_TRAFFIC_SPD : 전체 도로 평균 속도
ROAD_TRAFFIC_IDX : 전체 도로 소통 지표
ROAD_TRAFFIC_TIME : 도로 소통 데이터 업데이트 시간
ROAD_MSG : 도로 소통 관련 메시지
LINK_ID : 도로 구간 링크 ID
ROAD_NM : 도로명
START_ND_CD : 도로 시작 노드 코드
START_ND_NM : 도로 시작 노드명
START_ND_XY : 도로 시작 노드 좌표
END_ND_CD : 도로 종료 노드 코드
END_ND_NM : 도로 종료 노드명
END_ND_XY : 도로 종료 노드 좌표
DIST : 도로 구간 길이
SPD : 도로 구간 평균 속도
IDX : 도로 구간 소통 지표
XYLIST : 링크 ID 좌표 목록

■ 주차장 정보
PRK_STTS : 주차장 현황
PRK_NM : 주차장명
PRK_CD : 주차장 코드
PRK_TYPE : 주차장 구분
CPCTY : 주차장 수용 가능 면수
CUR_PRK_CNT : 현재 주차 가능 면수
CUR_PRK_TIME : 주차장 데이터 업데이트 시간
CUR_PRK_YN : 실시간 주차 정보 제공 여부
PAY_YN : 유무료 여부
RATES : 기본 주차 요금
TIME_RATES : 기본 주차 단위 시간
ADD_RATES : 추가 주차 요금
ADD_TIME_RATES : 추가 주차 단위 시간
ROAD_ADDR : 도로명 주소
ADDRESS : 지번 주소
LAT : 위도
LNG : 경도

■ 지하철 정보
SUB_STTS : 지하철 실시간 도착 현황
SUB_STN_NM : 지하철역명
SUB_STN_LINE : 지하철역 호선
SUB_STN_RADDR : 지하철역 도로명 주소
SUB_STN_JIBUN : 지하철역 지번 주소
SUB_STN_X : 지하철역 X 좌표
SUB_STN_Y : 지하철역 Y 좌표
SUB_NT_STN : 다음역 코드
SUB_BF_STN : 이전역 코드
SUB_ROUTE_NM : 지하철 노선명
SUB_LINE : 지하철 호선
SUB_ORD : 도착 예정 열차 순번
SUB_DIR : 지하철 방향
SUB_TERMINAL : 종착역
SUB_ARVTIME : 열차 도착 시간
SUB_ARMG1 : 열차 도착 메시지 1
SUB_ARMG2 : 열차 도착 메시지 2
SUB_ARVINFO : 열차 도착 코드 정보
SUB_FACINFO : 교통약자 이용시설 현황
ELVTR_NM : 승강기명
OPR_SEC : 운행 구간
INSTL_PSTN : 설치 위치
USE_YN : 운행 상태
ELVTR_SE : 승강기 구분
LIVE_SUB_PPLTN : 실시간 승하차 인원
SUB_ACML_GTON_PPLTN_MIN : 누적 승차 인원 최소값
SUB_ACML_GTON_PPLTN_MAX : 누적 승차 인원 최대값
SUB_ACML_GTOFF_PPLTN_MIN : 누적 하차 인원 최소값
SUB_ACML_GTOFF_PPLTN_MAX : 누적 하차 인원 최대값
SUB_30WTHN_GTON_PPLTN_MIN : 30분 이내 승차 인원 최소값
SUB_30WTHN_GTON_PPLTN_MAX : 30분 이내 승차 인원 최대값
SUB_30WTHN_GTOFF_PPLTN_MIN : 30분 이내 하차 인원 최소값
SUB_30WTHN_GTOFF_PPLTN_MAX : 30분 이내 하차 인원 최대값
SUB_10WTHN_GTON_PPLTN_MIN : 10분 이내 승차 인원 최소값
SUB_10WTHN_GTON_PPLTN_MAX : 10분 이내 승차 인원 최대값
SUB_10WTHN_GTOFF_PPLTN_MIN : 10분 이내 하차 인원 최소값
SUB_10WTHN_GTOFF_PPLTN_MAX : 10분 이내 하차 인원 최대값
SUB_5WTHN_GTON_PPLTN_MIN : 5분 이내 승차 인원 최소값
SUB_5WTHN_GTON_PPLTN_MAX : 5분 이내 승차 인원 최대값
SUB_5WTHN_GTOFF_PPLTN_MIN : 5분 이내 하차 인원 최소값
SUB_5WTHN_GTOFF_PPLTN_MAX : 5분 이내 하차 인원 최대값
SUB_STN_CNT : 장소 내 지하철역 개수
SUB_STN_TIME : 지하철역 개수 기준 년월

■ 버스 정보
BUS_STN_STTS : 버스 정류소 현황
BUS_RESULT_MSG : 버스 데이터 호출 메시지
BUS_STN_ID : 정류소 ID
BUS_ARS_ID : 정류소 고유번호
BUS_STN_NM : 정류소명
BUS_STN_X : 정류소 X 좌표
BUS_STN_Y : 정류소 Y 좌표
RTE_STN_NM : 노선 기준 정류장명
RTE_NM : 노선명
RTE_ID : 노선 ID
RTE_SECT : 노선 구간
RTE_CONGEST : 노선 혼잡도
RTE_ARRV_TM : 노선 예상 도착 시간
RTE_ARRV_STN : 최근 도착 정류장
LIVE_BUS_PPLTN : 실시간 승하차 인원
BUS_ACML_GTON_PPLTN_MIN : 누적 승차 인원 최소값
BUS_ACML_GTON_PPLTN_MAX : 누적 승차 인원 최대값
BUS_ACML_GTOFF_PPLTN_MIN : 누적 하차 인원 최소값
BUS_ACML_GTOFF_PPLTN_MAX : 누적 하차 인원 최대값
BUS_30WTHN_GTON_PPLTN_MIN : 30분 이내 승차 인원 최소값
BUS_30WTHN_GTON_PPLTN_MAX : 30분 이내 승차 인원 최대값
BUS_30WTHN_GTOFF_PPLTN_MIN : 30분 이내 하차 인원 최소값
BUS_30WTHN_GTOFF_PPLTN_MAX : 30분 이내 하차 인원 최대값
BUS_10WTHN_GTON_PPLTN_MIN : 10분 이내 승차 인원 최소값
BUS_10WTHN_GTON_PPLTN_MAX : 10분 이내 승차 인원 최대값
BUS_10WTHN_GTOFF_PPLTN_MIN : 10분 이내 하차 인원 최소값

■ 따릉이(공공자전거) 정보
SBIKE_STTS : 따릉이 현황
SBIKE_SPOT_NM : 따릉이 대여소 이름
SBIKE_SPOT_ID : 따릉이 대여소 ID
SBIKE_SHARED : 따릉이 거치율 (%)
SBIKE_PARKING_CNT : 따릉이 주차 건수
SBIKE_RACK_CNT : 따릉이 거치대 개수
SBIKE_X : 따릉이 대여소 X 좌표 (경도)
SBIKE_Y : 따릉이 대여소 Y 좌표 (위도)

■ 날씨 및 환경 정보
WEATHER_STTS : 날씨 현황 요약
TEMP : 현재 기온 (℃)
SENSIBLE_TEMP : 체감 온도 (℃)
MAX_TEMP : 일 최고 기온
MIN_TEMP : 일 최저 기온
HUMIDITY : 습도 (%)
WIND_DIRCT : 풍향 (예: 북풍, 남서풍 등)
WIND_SPD : 풍속 (m/s)
PRECIPITATION : 강수량 (mm)
PRECPT_TYPE : 강수 형태 (예: 비, 눈, 소나기 등)
PCP_MSG : 강수 관련 메시지
SUNRISE : 일출 시각
SUNSET : 일몰 시각
UV_INDEX_LVL : 자외선 지수 단계 (낮음~매우 높음)
UV_INDEX : 자외선 지수 수치
UV_MSG : 자외선 관련 메시지
PM25_INDEX : 초미세먼지 지표 단계
PM25 : 초미세먼지 농도 (㎍/㎥)
PM10_INDEX : 미세먼지 지표 단계
PM10 : 미세먼지 농도 (㎍/㎥)
AIR_IDX : 통합 대기환경 등급
AIR_IDX_MVL : 통합 대기환경 지수 수치
AIR_IDX_MAIN : 대기질 결정 주요 물질
AIR_MSG : 대기질 관련 메시지
WEATHER_TIME : 날씨 데이터 업데이트 시간

■ 기상 특보 정보
NEWS_LIST : 기상 관련 특보 목록
WARN_VAL : 기상 특보 종류
WARN_STRESS : 기상 특보 강도
ANNOUNCE_TIME : 기상 특보 발효 시각
COMMAND : 기상 특보 발표 코드
CANCEL_YN : 기상 특보 취소 여부
WARN_MSG : 기상 특보별 행동 요령

■ 24시간 예보 정보
FCST24HOURS : 24시간 예보 데이터
FCST_DT : 예보 시간
TEMP : 예보 기온
PRECIPITATION : 예보 강수량
PRECPT_TYPE : 예보 강수 형태
RAIN_CHANCE : 강수 확률 (%)
SKY_STTS : 하늘 상태 (맑음, 흐림 등)

■ 사고 통제 정보
ACDNT_CNTRL_STTS : 사고 통제 현황
ACDNT_OCCR_DT : 사고 발생 일시
EXP_CLR_DT : 통제 종료 예정 일시
ACDNT_TYPE : 사고 발생 유형
ACDNT_DTYPE : 사고 발생 세부 유형
ACDNT_INFO : 사고 통제 내용
ACDNT_X : 사고 지점 X 좌표 (경도)
ACDNT_Y : 사고 지점 Y 좌표 (위도)
ACDNT_TIME : 사고 통제 정보 업데이트 시간

■ 전기차 충전소 정보
CHARGER_STTS : 전기차 충전소 현황
STAT_NM : 충전소 이름
STAT_ID : 충전소 ID
STAT_ADDR : 충전소 주소
STAT_X : 충전소 X 좌표 (경도)
STAT_Y : 충전소 Y 좌표 (위도)
STAT_USETIME : 충전소 운영 시간
STAT_PARKPAY : 주차료 유무료 여부
STAT_LIMITYN : 이용자 제한 여부
STAT_LIMITDETAIL : 이용 제한 사유
STAT_KINDDETAIL : 충전소 상세 유형
CHARGER_ID : 충전기 ID
CHARGER_TYPE : 충전기 타입
CHARGER_STAT : 충전기 상태
STATUPDDT : 충전기 상태 갱신 일시
LASTTSDT : 마지막 충전 시작 일시
LASTTEDT : 마지막 충전 종료 일시
NOWTSDT : 현재 충전 시작 일시
OUTPUT : 충전기 출력 용량 (kW)
METHOD : 충전 방식 (예: 급속, 완속 등)

■ 문화행사 정보
CULTURALEVENTINFO : 문화행사 현황
EVENT_NM : 행사 이름
EVENT_PERIOD : 행사 기간
EVENT_PLACE : 행사 장소
EVENT_X : 행사 위치 X 좌표 (경도)
EVENT_Y : 행사 위치 Y 좌표 (위도)
PAY_YN : 행사 유무료 여부
THUMBNAIL : 행사 대표 이미지 URL
URL : 행사 상세 정보 URL
EVENT_ETC_DETAIL : 기타 행사 세부 정보

■ 실시간 상권 정보
LIVE_CMRCL_STTS : 실시간 상권 현황
AREA_CMRCL_LVL : 장소별 상권 수준
AREA_SH_PAYMENT_CNT : 장소별 신한카드 결제 건수
AREA_SH_PAYMENT_AMT_MIN : 장소별 결제 금액 최소값
AREA_SH_PAYMENT_AMT_MAX : 장소별 결제 금액 최대값

■ 업종별 상권 정보
RSB_LRG_CTGR : 업종 대분류
RSB_MID_CTGR : 업종 중분류
RSB_PAYMENT_LVL : 업종별 상권 수준
RSB_SH_PAYMENT_CNT : 업종별 결제 건수
RSB_SH_PAYMENT_AMT_MIN : 업종별 결제 금액 최소값
RSB_SH_PAYMENT_AMT_MAX : 업종별 결제 금액 최대값
RSB_MCT_CNT : 업종별 가맹점 수
RSB_MCT_TIME : 업종별 가맹점 수 기준 월

■ 소비자 특성 정보
CMRCL_MALE_RATE : 남성 소비 비율
CMRCL_FEMALE_RATE : 여성 소비 비율
CMRCL_10_RATE : 10대 이하 소비 비율
CMRCL_20_RATE : 20대 소비 비율
CMRCL_30_RATE : 30대 소비 비율
CMRCL_40_RATE : 40대 소비 비율
CMRCL_50_RATE : 50대 소비 비율
CMRCL_60_RATE : 60대 이상 소비 비율
CMRCL_PERSONAL_RATE : 개인 소비 비율
CMRCL_CORPORATION_RATE : 법인 소비 비율
CMRCL_TIME : 상권 데이터 업데이트 시간
"""
    url = f"http://openapi.seoul.go.kr:8088/{SEOUL_OPEN_API_KEY}/xml/citydata/1/5/{AREA_NM}"
    params = {
        "KEY":SEOUL_OPEN_API_KEY,
        "TYPE":"xml",
        "SEVICE":"citydata",
        "START_INDEX":1,
        "END_INDEX":5,
        "AREA_NM":AREA_NM
    }
    print(f"get_data_seoul tool called: {AREA_NM}")
    response = requests.get(url, params=params, timeout=5)
    root = ET.fromstring(response.content)

    result = []
    for elem in root.iter():
        tag = elem.tag
        text = elem.text.strip() if elem.text and elem.text.strip() else "null"
        result.append(f"{tag}\t{text}")
    
    return '\n'.join(result)