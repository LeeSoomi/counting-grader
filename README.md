# 경우의 수 · 채점 연습 (Streamlit)

코드스튜디오 입시연구소 · 확률과 통계 경우의 수 기출 35문항 O/X 채점 앱.
학번을 입력하면 풀이 기록이 구글 시트에 저장되어 **이어서** 풀 수 있습니다.

## 로컬 실행
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud 배포
1. 이 폴더를 GitHub 저장소에 올립니다 (`app.py`, `requirements.txt`).
2. share.streamlit.io → New app → 저장소·브랜치·`app.py` 선택 → Deploy.
3. 생성된 링크를 학생에게 공유.

## 학생별 기록 저장 켜기 (구글 시트)
설정하지 않으면 앱은 '이번 세션만 유지' 모드로 동작합니다. 영구 저장을 켜려면:

**1) 구글 클라우드에서 서비스 계정 만들기**
- console.cloud.google.com → 프로젝트 생성
- **Google Sheets API**와 **Google Drive API**를 사용 설정(Enable)
- IAM → 서비스 계정 생성 → 키(JSON) 발급 → JSON 파일 다운로드

**2) 저장할 구글 시트 준비**
- 구글 시트를 새로 만들고, 주소창의 스프레드시트 ID를 복사
  (`https://docs.google.com/spreadsheets/d/`**`이 부분`**`/edit`)
- ⚠️ **가장 흔한 실수**: 그 시트를 서비스 계정 이메일(`...@...iam.gserviceaccount.com`)에
  **편집자(Editor)로 공유**해야 합니다. 안 하면 권한 오류가 납니다.
- (워크시트 탭은 앱이 처음 저장할 때 `records`라는 이름으로 자동 생성합니다.)

**3) secrets 등록**
- 로컬: 프로젝트에 `.streamlit/secrets.toml` 생성
- 클라우드: 앱 Settings → Secrets 에 붙여넣기
```toml
sheet_id = "여기에_스프레드시트_ID"

[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "...@....iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```
> JSON 파일 내용을 그대로 옮기면 됩니다. `private_key`의 줄바꿈(`\n`)은 그대로 두세요.

**4) 사용**
- 학생이 사이드바에 **학번**을 입력 → 이전 풀이가 있으면 자동으로 불러와 이어서 풀이.
- 채점할 때마다 (학번, 문항, 유형, 정답여부, 학생답, 시각)이 시트에 자동 기록.
- **선생님은 그 구글 시트를 열어 학번별 진도·정답률을 바로 확인**할 수 있습니다.

> 개인정보 주의: 학번 대신 출석번호·별칭을 쓰거나, "연습 기록용으로만 저장된다"고 안내하는 것이 안전합니다.

## AI 힌트 기능 (선택)
오답일 때 "AI 힌트 받기" 버튼은 API 키가 있을 때만 나타납니다.
secrets에 `ANTHROPIC_API_KEY = "sk-ant-..."` 를 추가하세요.

## 확장 포인트 (app.py 안에 표시됨)
| 기능 | 함수 | 상태 |
|------|------|------|
| ① 해설 | `show_explanation()` | 각 문항 `"sol"` 채우면 표시 |
| ② AI 피드백 | `get_ai_feedback()` | 키 있으면 동작 |
| ③ 기록 저장 | `save_result()` / `load_progress()` | **구글 시트 연동 완료** |
| ④ 인증 | `check_license()` | 라이선스키 검증 자리 |

새 문제는 `PROBLEMS` 리스트에 dict를 추가하고 `_PROBLEM_IDS`에 문항번호를 더하면 됩니다.
