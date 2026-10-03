# 여행 기록문 - Streamlit 앱

Streamlit으로 만든 AI 기반 여행 기록 및 계획 애플리케이션입니다.

## 🎯 주요 기능

### 1. 🤖 AI와 대화
- AI 여행 가이드와 실시간 대화
- 여행 관련 정보 및 팁 제공
- 첫 대화 시 "안녕하세요"로 인사

### 2. 📝 여행 기록
- 다녀온 여행 기록 저장
- 위치, 날짜, 좋았던 점 기록
- 저장된 기록은 자동으로 JSON 파일에 저장

### 3. 🗺️ 여행 계획
- AI와 함께 여행 계획 짜기
- 여행지, 일정, 예산 등 상담
- 완료 시 "여행 잘 갔다오세요!" 메시지

## 🎨 디자인 특징

- 배경: 하얀색에서 하늘색으로의 그라데이션
- 직관적인 버튼 기반 네비게이션
- 색상 코드:
  - 초록색 버튼: AI 대화
  - 파란색 버튼: 여행 기록
  - 빨간색 버튼: 여행 계획

## 📋 설치 및 실행

### 1. 필수 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env.example`을 `.env`로 복사하고 API 키 입력:
```bash
cp .env.example .env
```

`.env` 파일 수정:
```
ANTHROPIC_API_KEY=your_actual_api_key
ANTHROPIC_BASE_URL=https://api.anthropic.com/v1
```

### 3. Streamlit 앱 실행
```bash
streamlit run app.py
```

앱이 브라우저에서 자동으로 열립니다 (기본값: `http://localhost:8501`)

## 📁 파일 구조

```
project2_travel_app/
├── app.py                 # 메인 Streamlit 앱
├── ai_helper.py           # AI API 헬퍼 함수
├── ai.helper.py           # 기존 헬퍼 파일 (ai_helper.py와 동일)
├── requirements.txt       # Python 패키지 의존성
├── .env.example          # 환경 변수 템플릿
├── travels_data.json     # 여행 기록 저장 파일 (자동 생성)
├── PLAN.md               # 프로젝트 계획
└── APP_README.md         # 이 파일
```

## 🔐 보안 주의사항

- `.env` 파일은 절대 Git에 커밋하지 마세요
- `travels_data.json`은 개인 정보가 포함되어 있으므로 주의하세요
- API 키는 항상 안전하게 관리하세요

## 🚀 사용 예시

### AI와 대화
1. 홈페이지에서 "🤖 AI와 대화" 버튼 클릭
2. AI가 "안녕하세요!"로 인사합니다
3. 여행에 관한 질문을 입력합니다
4. AI가 친절한 조언을 제공합니다

### 여행 기록
1. 홈페이지에서 "📝 여행 기록" 버튼 클릭
2. 여행지, 날짜, 좋았던 점 입력
3. "기록 저장" 버튼 클릭
4. 홈페이지의 "최근 여행 기록" 섹션에서 확인

### 여행 계획
1. 홈페이지에서 "🗺️ 여행 계획" 버튼 클릭
2. AI와 대화형으로 여행을 계획합니다
3. "완료" 버튼을 누르면 AI가 "여행 잘 갔다오세요!"라고 말합니다

## 💡 팁

- 여행 기록은 브라우저를 닫아도 `travels_data.json`에 저장됩니다
- Streamlit 앱은 코드 변경 시 자동으로 재로드됩니다
- 대화 히스토리는 페이지를 떠나면 초기화됩니다

## 🐛 문제 해결

### "ModuleNotFoundError: No module named 'anthropic'"
→ `pip install -r requirements.txt` 실행

### "ANTHROPIC_API_KEY not found"
→ `.env` 파일이 존재하고 올바르게 설정되었는지 확인

### 앱이 시작되지 않음
→ `streamlit run app.py` 명령어가 올바른 디렉토리에서 실행되는지 확인

## 📞 지원

문제가 있거나 기능 요청이 있으시면 이슈를 등록해주세요!
