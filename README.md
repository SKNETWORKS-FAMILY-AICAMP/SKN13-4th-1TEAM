<h1 style="all:unset; font-size:2em;">지금 서울 (SKN13-4TH-1TEAM)</h1>

## 목차
1. [팀 소개](#1-팀-소개)  
2. [프로젝트 개요](#2-프로젝트-개요)  
3. [요구사항 명세서](#3-요구사항-명세서)  
4. [WBS](#4-wbs)  
5. [전체 구조 개요](#5-전체-구조-개요)  
6. [주요 컴포넌트 및 역할](#6-주요-컴포넌트-및-역할)  
7. [데이터 및 서비스 흐름](#7-데이터-및-서비스-흐름)  
8. [기술 스택](#8-기술-스택)  
9. [인프라/운영 구조](#9-인프라운영-구조)  
10. [보안 및 확장성](#10-보안-및-확장성)  
11. [기타 참고](#11-기타-참고)

# 1. 팀 소개
### 1) 팀명 : 지금 서울
### 2) 개발 기간
> 2025.07.21 ~ 2025.07.22
### 3) 팀원

<table width="100%">
  <tr>
    <td align="center" width="20%">
      <img src="chatbot_web/main/static/main/images/남궁건우_사진.png" width="150"/>
    </td>
    <td align="center" width="20%">
      <img src="chatbot_web/main/static/main/images/우지훈_사진.png" width="150"/>
    </td>
    <td align="center" width="20%">
      <img src="chatbot_web/main/static/main/images/이명인_사진.png" width="150"/>
    </td>
    <td align="center" width="20%">
      <img src="chatbot_web/main/static/main/images/홍채우_사진.png" width="150"/>
    </td>
    <td align="center" width="20%">
      <img src="chatbot_web/main/static/main/images/김승호_사진.png" width="150"/>
    </td>
  <tr>

  <tr>
    <td align="center" width="20%">
      <b>남궁건우</b>
    </td>
    <td align="center" width="20%">
      <b>우지훈</b>
    </td>
    <td align="center" width="20%">
      <b>이명인</b>
    </td>
    <td align="center" width="20%">
      <b>홍채우</b>
    </td>
    <td align="center" width="20%">
      <b>김승호</b>
    </td>
  </tr>

  <tr>
    <td align="center" width="20%">
      <a href="https://github.com/NGGW519">
        <img src="https://img.shields.io/badge/GitHub-NGGW519-1F1F1F?logo=github" alt="남궁건우 GitHub"/>
      </a>
    </td>
    <td align="center" width="20%">
      <a href="https://github.com/WooZhoon">
        <img src="https://img.shields.io/badge/GitHub-WooZhoon-1F1F1F?logo=github" alt="우지훈 GitHub"/>
      </a>
    </td>
    <td align="center" width="20%">
      <a href="https://github.com/leemyeongin2416">
        <img src="https://img.shields.io/badge/GitHub-leemyeongin2416-1F1F1F?logo=github" alt="이명인 GitHub"/>
      </a>
    </td>
    <td align="center" width="20%">
      <a href="https://github.com/HCWDDD">
        <img src="https://img.shields.io/badge/GitHub-HCWDDD-1F1F1F?logo=github" alt="홍채우 GitHub"/>
      </a>
    </td>
    <td align="center" width="20%">
      <a href="https://github.com/qqqppma">
        <img src="https://img.shields.io/badge/GitHub-qqqppma-1F1F1F?logo=github" alt="김승호 GitHub"/>
      </a>
    </td>
  </tr>
</table>

### 4) 팀원 역할 및 담당 업무

| 이름     | 역할              | 주요 담당 업무                                        |
|----------|-------------------|-------------------------------------------------------|
| 남궁건우 | 팀장 / 기획        | 프로젝트 총괄, 기획 및 발표, 요구사항 명세 작성, 데이터 수집 |
| 김승호   | 프론트엔드 개발        | 화면 설계 및 UI 구현       |
| 우지훈   | LLM/AI 엔지니어   | LangChain 기반 RAG 설계, 프롬프트 최적화 및 LLM 연동        |
| 이명인   | 데이터 운영     | FAQ/민원 데이터 분석, 임베딩 전처리                |
| 홍채우   | 프론트엔드 개발        | 데이터 수집, UI설계     |


<br/>

---

# 2. 프로젝트 개요

### 1) 프로젝트 명  
**서울시 스마트 통합 정보 서비스**


### 2) 주제  
**서울시 열린데이터 및 120다산콜 FAQ를 활용한 시민 맞춤형 챗봇 개발**


### 3) 프로젝트 필요성(주제 선정 이유)  

- **시민 중심의 정보 수요 증가**: 서울시민의 미세먼지, 따릉이, 날씨, 주차 등 생활 전반의 실시간 정보에 대한 높은 수요
- **정보 접근의 비효율성**: 일반 시민이 해당 정보를 직접 탐색하거나 활용하기에는 절차가 복잡하고 접근성이 낮음
- **반복적인 행정 상담 수요**: 서울시 120다산콜센터에는 동일하거나 유사한 질문이 지속적으로 반복 접수되고 있으며, 이로 인해 행정 자원의 낭비가 발생
- **자연어 기반 서비스의 필요**: 기존 시스템은 키워드 검색 기반이 대부분으로, 자연어로 질문하고 바로 응답받을 수 있는 인터페이스가 부족


### 4) 주요 기능 요약  

| 분류       | 주요 기능 |
|------------|-----------|
| 실시간 데이터 | 열린데이터광장의 API를 통해 실시간 인구, 날씨, 주차, 대중교통 등 정보 제공 |
| FAQ 응답     | 120다산콜 FAQ 데이터를 기반으로 반복 질문에 자동 응답 |
| 질문 분류     | 입력된 질문을 실시간/FAQ/기타로 분류해 적절한 응답 경로 연결 |
| 관리자 기능  | 응답 로그 관리 기능 포함 |


### 5) 기대 효과  

- 시민의 정보 접근성 향상
- 재난 대응 속도 및 정확도 개선
- 행정 서비스의 디지털 전환 가속화
- 데이터 기반 정책 피드백 수단 확보

---

# 3. 요구사항 명세서


| 요구사항 ID | 요구유형 | 요구 주체 | 요구사항명           | 요구사항 내용 | 중요도 |
|-------------|----------|-------------|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| REQ-F01     | 기능     | 사용자        | 실시간 데이터 응답   | 사용자가 “여의도 주차 상황 알려줘”, “광화문 날씨 어때?”와 같은 질문 시, 열린데이터광장([link](https://data.seoul.go.kr/dataVisual/seoul/guide.do)) API를 통해 실시간 정보 제공 | 상     |
| REQ-F02     | 기능     | 사용자        | FAQ 자동 응답       | 사용자가 "기후동행카드는 어떻게 써?" 등 질문 시, 서울시 정보공개포털 FAQ([link](https://opengov.seoul.go.kr/civilappeal/list?page=27)) 데이터 기반 자동 응답 | 상     |
| REQ-F04     | 기능     | 사용자        | 챗봇 대화 UI         | 챗 인터페이스를 통해 사용자가 직관적으로 질문하고 응답을 받을 수 있어야 함 | 중     |
| REQ-F03     | 기능     | 시스템        | 질문 분류 기능       | 입력된 질문을 실시간 정보, FAQ, 일반 문의로 자동 분류하여 처리 경로를 결정 | 상     |
| REQ-F05     | 기능     | 시스템        | 관리자 기능          | 관리자 페이지를 통해 FAQ 등록/수정, 응답 기록 확인, 인기 질문 통계 등을 제공 | 중     |
| REQ-NF02    | 비기능   | 사용자        | 반응형 웹 지원       | PC, 모바일, 태블릿 등 다양한 기기에서 UI가 자동으로 최적화되어야 함 | 상     |
| REQ-NF05    | 비기능   | 사용자        | 개인정보 비수집 고지 | 사용자 개인정보를 저장하지 않으며, 이를 명확히 고지해야 함 | 중     |
| REQ-NF01    | 비기능   | 시스템        | 응답 속도            | 전체 응답 처리 시간이 평균 2초 이내여야 함 | 상     |
| REQ-NF03    | 비기능   | 시스템        | API 오류 처리        | 외부 API 오류 발생 시 사용자에게 안내 메시지를 제공해야 함 | 상     |
| REQ-NF04    | 비기능   | 시스템        | 보안 정책 적용       | HTTPS 사용 및 Django 보안 설정을 적용해야 함 | 중     |

---

# 4. WBS

### 1. 프로젝트 기획 및 요구사항 정의
| 작업 ID | 작업 항목             | 상세 설명                                                   | 담당자     |
|--------|----------------------|-------------------------------------------------------------|------------|
| 1.1    | 주제 선정 및 기획안 작성 | 프로젝트 목적 및 배경 정의, 핵심 기능 기획                   | 남궁건우   |
| 1.2    | 요구사항 명세        | 기능/비기능 요구사항 목록화 및 우선순위 지정                 | 남궁건우   |


### 2. 백엔드 개발 (Django)
| 작업 ID | 작업 항목                | 상세 설명                                                         | 담당자     |
|--------|-------------------------|-------------------------------------------------------------------|------------|
| 2.1    | Django 환경 구축         | 프로젝트 세팅, DB 연결, API 기본 구조 설정                         | 우지훈     |
| 2.2    | 실시간 정보 API 연동     | 서울 열린데이터광장 API 연동 (주차, 날씨 등)                       | 김승호     |
| 2.3    | FAQ 데이터 자동 응답     | FAQ 크롤링 및 응답 API 개발                                       | 우지훈     |
| 2.4    | 관리자 페이지 기능 구현   | FAQ 등록/수정, 통계 확인 페이지 구현                              | 우지훈     |


### 3. 데이터 수집 및 전처리
| 작업 ID | 작업 항목                 | 상세 설명                                                         | 담당자           |
|--------|--------------------------|-------------------------------------------------------------------|------------------|
| 3.1    | FAQ/민원 데이터 수집        | 120다산콜 FAQ 및 시민 민원 크롤링                                 | 남궁건우, 이명인, 홍채우 |
| 3.2    | 서울시 API 연계 데이터 조사  | 열린데이터광장 API 문서 확인 및 활용 가능한 데이터 확인            | 남궁건우, 이명인, 홍채우           |
| 3.3    | 텍스트 전처리 및 정제        | 수집된 텍스트 정제, 불용어 제거, 형식 표준화 등                   | 이명인           |


### 4. 프론트엔드 개발 (Django Template)
| 작업 ID | 작업 항목               | 상세 설명                                                     | 담당자         |
|--------|------------------------|---------------------------------------------------------------|----------------|
| 4.0    | 와이어프레임 설계   | 메인 페이지, 챗봇, 관리자 페이지 등 전체 UI 구조 설계 및 공유       | 김승호, 홍채우 |
| 4.1    | 메인/챗봇 UI 디자인       | 사용자 메인 페이지 및 챗봇 대화 UI 구현                           | 김승호 |
| 4.2    | 반응형 웹 적용            | PC/모바일/태블릿에 맞게 CSS 및 JS 반영                            | 김승호 |
| 4.3    | 관리자 페이지 UI 구현      | 관리자 전용 인터페이스 (FAQ 등록/통계 시각화 등)                   | 김승호 |


### 5. 챗봇/AI 모듈 개발 (LangChain, LLM)
| 작업 ID | 작업 항목             | 상세 설명                                                       | 담당자     |
|--------|----------------------|-----------------------------------------------------------------|------------|
| 5.1    | LangChain 기반 챗봇 구성 | 프롬프트 설계, 에이전트 워크플로우 설정                         | 우지훈     |
| 5.2    | ChromaDB 구축 및 벡터화 | FAQ 데이터 벡터화 및 검색 구조 구성                             | 우지훈     |
| 5.3    | 외부 API 툴 통합       | 네이버 검색, 날씨, 공공 API 툴 통합 및 호출 테스트              | 우지훈     |


### 6. 배포 및 운영
| 작업 ID | 작업 항목           | 상세 설명                                                       | 담당자     |
|--------|--------------------|-----------------------------------------------------------------|------------|
| 6.1    | AWS EC2 서버 세팅   | Django 배포 환경 세팅, EC2 인스턴스 생성                        | 우지훈, 남궁건우   |
| 6.2    | Chroma 벡터스토어 반영 | Git에 포함되지 않은 DB 직접 업로드 및 연결 확인                 | 우지훈, 남궁건우   |
| 6.3    | .env, 보안 설정 정리 | 환경변수 분리, Django 보안 설정 적용                           | 우지훈, 남궁건우   |


### 7. 발표자료 및 마무리
| 작업 ID | 작업 항목         | 상세 설명                                           | 담당자     |
|--------|------------------|---------------------------------------------------|------------|
| 7.1    | PPT/README 작성    | 팀 소개, 시스템 구조, 기대 효과 등 발표자료 작성   | 남궁건우, 김승호, 이명인   |


---

# 5. UI 시안

---

# 6. 전체 구조 개요

본 프로젝트는 **행정 QnA 및 실시간 생활 정보 챗봇 서비스**로, Django 기반 웹 백엔드와 LLM·RAG 기반 AI, MySQL·ChromaDB 등 다양한 데이터 소스와 연동되는 구조입니다.

```
[사용자] ⇄ [Django 웹서버] ⇄ [챗봇 에이전트/LLM] ⇄ [DB/벡터스토어/API]
```

### Directory Structure

```python
SKN13-4th-1TEAM/
├── chat_agent.py
├── chatbot_web/
│   ├── chatbot_web
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   ├── main/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── migrations
│   │   ├── mock_data
│   │   ├── models.py
│   │   ├── static/
│   │   │   └── main/
│   │   │       ├── board_detail.css
│   │   │       ├── board_form.css
│   │   │       └── ...
│   │   ├── templates/
│   │   │   └── main
│   │   │       ├── base.html
│   │   │       ├── chatbot.html
│   │   │       ├── login.html
│   │   │       ├── js/
│   │   │       │   ├── chatbot.js
│   │   │       │   ├── job_page.js
│   │   │       │   └── ...
│   │   │       └── ...
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── manage.py
│   └── staticfiles/
│       ├── admin
│       └── main
├── create_engine.py
├── dataset
├── Drafts
├── llm_tools/
│   ├── chat_history_manager.py
│   ├── get_weather.py
│   ├── google_places.py
│   ├── naver_search.py
│   ├── retriever.py
│   └── sEOUl.py
├── README.md
├── requirements.txt
├── system_prompt.py
├── SYSTEM_ARCHITECTURE.md
└── chromadb_dataset.py
```

---

# 7. 주요 컴포넌트 및 역할

### 1) 프론트엔드 (Django Template)
- 사용자 로그인/회원가입, 챗봇 UI, 지도 기반 정보 조회, 게시판 등 제공
- 파일 업로드, 실시간 채팅, 추천/알림 등 인터랙션 지원

### 2) 백엔드 (Django)
- RESTful API 및 웹페이지 라우팅
- 사용자 인증/세션 관리
- 챗봇 요청 처리 및 대화 이력 관리
- 파일 업로드/다운로드, 알림 등 부가 기능

### 3) 챗봇 에이전트 (LangChain + LangGraph)
- 사용자 메시지 수신 → 프롬프트/도구 조합 → LLM 호출 및 응답 생성
- 다양한 툴(RAG, 네이버검색, 서울시 실시간 도시데이터 등)과 연동
- 대화 상태(State) 관리 및 히스토리 저장

### 4) 데이터베이스
- **MySQL**: 사용자, 게시글, 댓글, 알림, 챗봇 세션 등 구조적 데이터 저장
- **ChromaDB**: 120다산콜센터에서 관리하고 있는 '자주 묻는 질문' QnA 임베딩 벡터 저장(RAG 검색용)

### 5) 외부 API/데이터
- **OpenAI API**: LLM(예: GPT-4) 호출
- **공공데이터포털/서울시 열린데이터광장 API**: 실시간 인구,실시간 교통, 날씨, 문화행사 등 정보
- **네이버/구글 API**: 장소, 뉴스, 블로그 등 검색

### 6) 크롤러/데이터 파이프라인
- Selenium, BeautifulSoup 등으로 행정 QnA/뉴스/민원 데이터 수집 및 전처리
- Pandas 등으로 데이터 정제 및 저장

---

# 8. 데이터 및 서비스 흐름

```mermaid
graph TD
  A[User] --> B[Django Server]
  B -->|Chat Msg/File Upload| C[Chatbot Agent]
  C -->|Query/Command| D1[MySQL]
  C -->|Embedding Search| D2[ChromaDB]
  C -->|External API Call| D3[OpenAI / Public API / Naver]
  D1 --> C
  D2 --> C
  D3 --> C
  C --> B
  B -->|Result/Notification| A
```
## 1) 서비스 플로우

### 1. 사용자 요청 (User → Django Server)
- 사용자는 웹 UI를 통해 질문을 입력 및 요청은 Django 서버로 전달

### 2. Django 서버 → 챗봇 에이전트 연결
- Django 서버는 입력 데이터를 **챗봇 에이전트(Chatbot Agent)**로 전달  
- 챗봇 에이전트는 입력 내용을 분석하여 다음 중 하나로 분기:
  - 일반 질의 (FAQ, 도시데이터 등)
  - 외부 API 호출이 필요한 요청

### 3. 챗봇 에이전트 내부 처리

#### A. 데이터 저장 및 조회 (MySQL 연동)
- 요청이 사용자 세션, 질문 이력, 파일 로그 저장과 관련된 경우 MySQL DB에 기록되거나 조회

#### B. 임베딩 기반 검색 (ChromaDB 연동)
- 사용자의 질문이 RAG 기반 질의일 경우, 챗봇은 질문을 임베딩하고 ChromaDB 벡터DB에서 관련 문서를 유사도 검색  
- 예: "광화문 공영주차장 자리 있나요?" → 관련 FAQ나 문서 검색 후 응답 구성

#### C. 외부 API 호출
- 실시간 도시정보, OpenAI 응답 생성, 네이버 검색 등 외부 리소스가 필요할 경우:
  - **서울 열린데이터광장(OpenAPI)**: 실시간 도시 데이터 요청
  - **OpenAI**: GPT 응답 생성
  - **Naver API 등**: 기타 기능 수행
- 결과는 챗봇 에이전트로 다시 전달

### 4. 응답 구성 및 반환
- 챗봇 에이전트는 데이터베이스, 벡터DB, 외부 API에서 받은 정보를 통합해 응답을 생성 후 Django 서버를 통해 다시 사용자에게 전달

### 5. 사용자 응답 수신 (Django Server → User)
- 사용자는 웹 화면에서 응답 메시지을 실시간으로 확인

---

# 9. 기술 스택

| 구분         | 주요 기술/서비스                      |
| ------------ | ------------------------------------- |
| 백엔드       | ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
| 프론트엔드   | ![Django Template](https://img.shields.io/badge/Django%20Template-092E20?style=for-the-badge) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) ![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![HTML](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white)
| 챗봇/AI      | ![LangChain](https://img.shields.io/badge/LangChain-000000?style=for-the-badge&logo=LangChain&logoColor=white) ![LangGraph](https://img.shields.io/badge/LangGraph-4B0082?style=for-the-badge) ![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
| DB           | ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white) ![ChromaDB](https://img.shields.io/badge/ChromaDB-FF8C00?style=for-the-badge)
| 크롤링/ETL   | ![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white) ![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4B0082?style=for-the-badge) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
| 배포/운영     | ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) ![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white) ![dotenv](https://img.shields.io/badge/.env-8B0000?style=for-the-badge)

---

# 10. 인프라/운영 구조
- 리눅스 서버(AWS EC2 등)에 Python/Django 환경 구축
- MySQL, ChromaDB 등 데이터베이스 별도 운영
- .env 파일로 API KEY, DB 정보 등 환경변수 관리
- requirements.txt로 패키지 일괄 설치
- 크롬드라이버 등 외부 바이너리 별도 설치 필요

---

# 11. 보안 및 확장성
- CSRF, 세션, 인증 등 Django 기본 보안 적용
- API KEY, DB 비밀번호 등은 .env로 분리 관리
- 벡터스토어/LLM/외부API 등 모듈화로 기능 확장 용이

---

# 12. 기타 참고
- 상세 UI/UX, 데이터 파이프라인, 정책 보고서 자동화 등은 Drafts/ 폴더 내 문서 참고
- 실제 배포 시 requirements.txt, .env, DB 마이그레이션 등 필수 적용 
