# 경우의 수 · 채점 연습 (Streamlit)

코드스튜디오 입시연구소 · 확률과 통계 경우의 수 기출 35문항 O/X 채점 앱.

## 로컬 실행
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud 배포
1. 이 폴더를 GitHub 저장소에 올립니다 (`app.py`, `requirements.txt`).
2. share.streamlit.io → New app → 저장소·브랜치·`app.py` 선택 → Deploy.
3. 생성된 링크를 학생에게 공유하면 끝.

## AI 힌트 기능 켜기 (선택)
오답일 때 "AI 힌트 받기" 버튼은 API 키가 있을 때만 나타납니다.
- 로컬: 프로젝트에 `.streamlit/secrets.toml` 파일을 만들고 아래 한 줄 추가
  ```toml
  ANTHROPIC_API_KEY = "sk-ant-..."
  ```
- 클라우드: 앱 설정 → Secrets 에 같은 내용을 붙여넣기.
- 키를 코드나 GitHub에 올리지 마세요.

## 확장 포인트 (app.py 안에 표시됨)
| 기능 | 함수 | 하는 일 |
|------|------|---------|
| ① 해설 | `show_explanation()` | 각 문항 `"sol"` 값만 채우면 자동 표시 |
| ② AI 피드백 | `get_ai_feedback()` | 학생 오답에 힌트 생성 (키 필요) |
| ③ 기록 저장 | `save_result()` | SQLite / Google Sheets 연결 자리 |
| ④ 인증 | `check_license()` | 라이선스키 검증 자리 |

새 문제는 `PROBLEMS` 리스트에 dict 하나만 추가하면 됩니다.
