# -*- coding: utf-8 -*-
"""
경우의 수 · 채점 연습 앱   |   코드스튜디오 입시연구소
============================================================
Streamlit 단일 파일 앱.

■ 지금 되는 것
   - 유형(분류 / 소제목) 선택
   - 학생이 정답(자연수)을 입력 → 즉시 O/X 채점
   - 유형별 · 전체 정답률 집계

■ 확장 포인트  (아래 함수 자리를 채우면 기능이 켜집니다)
   ①  해설 표시        →  show_explanation()   : PROBLEMS의 "sol" 값만 채우면 자동 동작
   ②  AI 풀이 피드백    →  get_ai_feedback()    : ANTHROPIC_API_KEY 필요
   ③  학생 기록 저장    →  save_result()        : SQLite / Google Sheets
   ④  라이선스키 인증   →  check_license()

실행:  streamlit run app.py
"""

import streamlit as st
import datetime as _dt


# ============================================================
# 1) 유형 정의  (cat = 교과서 대분류,  sub = 세부 소제목)
# ============================================================
TYPES = [
    {"cat": "중복순열", "sub": "함수의 개수"},
    {"cat": "같은 것이 있는 순열", "sub": "일렬 나열"},
    {"cat": "같은 것이 있는 순열", "sub": "택하여 나열"},
    {"cat": "같은 것이 있는 순열", "sub": "정수·함수의 개수"},
    {"cat": "중복조합", "sub": "나누어 주기"},
    {"cat": "중복조합", "sub": "함수의 개수"},
    {"cat": "중복조합", "sub": "부정방정식"},
]


# ============================================================
# 2) 문제 은행
#    새 문제를 추가하려면 dict 하나를 리스트에 더 넣으면 됩니다.
#      t     : TYPES의 인덱스(0~6)
#      ans   : 정답(정수)          src : 출처        jum : 배점
#      lead  : 문제 본문           conds : 조건 리스트
#      sol   : 해설(비워두면 '미등록'으로 표시)
# ============================================================
PROBLEMS = [
    {
        "t": 0, "ans": 128, "src": "2021 평가원 고3 11월 확통 28", "jum": "4점",
        "lead": "두 집합 X={1,2,3,4,5}, Y={1,2,3,4}에 대하여 다음 조건을 만족시키는 X에서 Y로의 함수 f의 개수를 구하시오.",
        "conds": [
            "(가) 집합 X의 모든 원소 x에 대하여 f(x) ≥ √x 이다.",
            "(나) 함수 f의 치역의 원소의 개수는 3이다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 0, "ans": 180, "src": "2025 교육청 고3 10월 확통 29", "jum": "4점",
        "lead": "집합 X={2,3,5,7,11}과 함수 f:X→X에 대하여 f의 치역을 A, 합성함수 f∘f의 치역을 B라 할 때, 다음 조건을 만족시키는 함수 f의 개수를 구하시오.",
        "conds": [
            "(가) n(B)=2",
            "(나) 집합 A의 모든 원소의 곱은 집합 B의 모든 원소의 곱의 2배이다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 0, "ans": 165, "src": "2024 교육청 고3 5월 확통 26", "jum": "",
        "lead": "두 집합 X={1,2,3,4,5}, Y={1,2,3,4}에 대하여 다음 조건을 만족시키는 함수 f:X→Y의 개수를 구하시오.",
        "conds": [
            "(가) f(1)+f(2)=4",
            "(나) 1은 함수 f의 치역의 원소이다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 0, "ans": 104, "src": "2021 교육청 고3 3월 확통 28", "jum": "4점",
        "lead": "두 집합 X={1,2,3,4,5}, Y={2,4,6,8,10,12}에 대하여 X에서 Y로의 함수 f 중에서 다음 조건을 만족시키는 함수의 개수를 구하시오.",
        "conds": [
            "(가) f(2)<f(3)<f(4)",
            "(나) f(1)>f(3)>f(5)",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 0, "ans": 414, "src": "2022학년도 평가원 고3 9월 확통 28", "jum": "4점",
        "lead": "집합 X={1,2,3,4,5,6}에 대하여 다음 조건을 만족시키는 함수 f:X→X의 개수를 구하시오.",
        "conds": [
            "(가) f(3)+f(4)는 5의 배수이다.",
            "(나) f(1)<f(3)이고 f(2)<f(3)이다.",
            "(다) f(4)<f(5)이고 f(4)<f(6)이다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 1, "ans": 144, "src": "2028학년도 평가원 수능 예시문항 21", "jum": "4점",
        "lead": "숫자 0이 적힌 카드 2장, 1이 적힌 카드 5장, 2가 적힌 카드 3장이 있다. 이 10장을 모두 한 번씩 사용하여 10개의 자리에 다음 조건을 만족시키도록 한 장씩 놓는 경우의 수를 구하시오. (단, 같은 숫자 카드끼리는 구별하지 않는다.)",
        "conds": [
            "n(1≤n≤10)번째 자리 카드의 수를 aₙ이라 할 때, |aₖ₊₁ − aₖ| = 2를 만족시키는 자연수 k(1≤k≤9)의 개수는 3이다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 1, "ans": 18, "src": "2023 교육청 고3 7월 확통 27", "jum": "3점",
        "lead": "숫자 0,0,0,1,1,2,2가 하나씩 적힌 7장의 카드를 모두 한 번씩 사용하여 일렬로 나열할 때, 이웃하는 두 카드에 적힌 수의 곱이 모두 1 이하가 되도록 나열하는 경우의 수를 구하시오. (단, 같은 숫자 카드끼리는 구별하지 않는다.)",
        "conds": [],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 1, "ans": 192, "src": "2024 교육청 고3 3월 확통 27", "jum": "3점",
        "lead": "문자 A,A,A,B,B,C,D가 하나씩 적힌 7장의 카드와 1부터 7까지 적힌 7개의 빈 상자가 있다. 각 상자에 한 장씩 들어가도록 나누어 넣을 때, A가 들어간 3개 상자에 적힌 수의 합이 홀수가 되도록 넣는 경우의 수를 구하시오. (단, 같은 문자 카드끼리는 구별하지 않는다.)",
        "conds": [],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 1, "ans": 376, "src": "2025 교육청 고3 5월 확통 30", "jum": "4점",
        "lead": "1부터 6까지 적힌 6개의 전구가 모두 꺼져 있고, 각 전구는 버튼을 누를 때마다 켜짐↔꺼짐이 바뀐다. 주사위를 던져 나온 눈이 n이면 n 이하 번호의 모든 전구 버튼을 한 번씩 누른다. 이 시행을 5번 반복해 나온 눈을 차례로 a,b,c,d,e라 하자. 5번째 시행 후 전구가 모두 켜져 있도록 하는 순서쌍 (a,b,c,d,e)의 개수를 구하시오.",
        "conds": [],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 1, "ans": 846, "src": "2020 교육청 고3 4월 19 (과정형)", "jum": "4점",
        "lead": "4주 동안 월~수 하루 한 종류씩 봉사활동 A,B,C를 각각 3·3·6회 신청한다. 첫째 주엔 A,B,C를 모두 신청하고, 같은 요일에는 두 종류 이상 신청한다. 아래 (가)=p, (나)=q일 때 p+q의 값을 구하시오.",
        "conds": [
            "(가) 첫째 주 제외 3주간 A,B,C를 각각 2·2·5회 신청하는 경우의 수",
            "(나) 첫째 주 C 요일과 같은 요일에 4주 모두 C를 신청하는 경우의 수",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 2, "ans": 708, "src": "2022 교육청 고3 3월 확통 30", "jum": "4점",
        "lead": "흰색 원판 4개와 검은색 원판 4개에 각각 A,B,C,D가 하나씩 적혀 있다. 이 8개 중 4개를 택하여 다음 규칙으로 원기둥 모양으로 쌓는 경우의 수를 구하시오. (단, 원판 크기는 모두 같고, 각 원판의 두 밑면은 구별하지 않는다.)",
        "conds": [
            "(가) 선택된 4개 중 같은 문자 원판이 있으면, 그 문자끼리는 검은색이 흰색보다 아래에 놓이도록 쌓는다.",
            "(나) 선택된 4개 중 같은 문자 원판이 없으면, D 원판이 맨 아래에 놓이도록 쌓는다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 2, "ans": 146, "src": "2021학년도 경찰대 7월 8", "jum": "4점",
        "lead": "모든 자리의 수의 합이 10인 다섯 자리 자연수 중, 숫자 1,2,3을 각각 한 번 이상 사용하는 자연수의 개수를 구하시오.",
        "conds": [],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 2, "ans": 544, "src": "2026학년도 사관학교 7월 확통 27", "jum": "3점",
        "lead": "숫자 0,1,2,3,4 중 중복을 허락하여 5개를 선택한 후 일렬로 나열하여 다섯 자리 자연수를 만든다. 숫자 1과 3을 각각 홀수 개씩(각각 1개 이상) 선택하여 만들 수 있는 모든 다섯 자리 자연수의 개수를 구하시오.",
        "conds": [],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 2, "ans": 30, "src": "2020 교육청 고3 10월 10", "jum": "3점",
        "lead": "A,B,B,C,C,C가 하나씩 적힌 6장의 카드 중 5장을 택해 왼쪽부터 일렬로 나열할 때, C 카드가 왼쪽에서 두 번째에 놓이도록 나열하는 경우의 수를 구하시오. (단, 같은 문자 카드끼리는 구별하지 않는다.)",
        "conds": [],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 2, "ans": 199, "src": "2022학년도 평가원 고3 6월 확통 28", "jum": "4점",
        "lead": "주사위를 던져 나온 눈이 3 이하이면 그 눈의 수를 점수로 얻고, 4 이상이면 0점을 얻는다. 주사위를 네 번 던져 나온 눈을 차례로 a,b,c,d라 할 때, 얻은 네 점수의 합이 4가 되는 순서쌍 (a,b,c,d)의 개수를 구하시오.",
        "conds": [],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 3, "ans": 930, "src": "2026 교육청 고3 3월 확통 28", "jum": "4점",
        "lead": "두 집합 X={x | x는 9 이하의 자연수}, Y={1,2,4}에 대하여 다음 조건을 만족시키는 함수 f:X→Y의 개수를 구하시오.",
        "conds": [
            "(가) f(x)=1인 x는 3개, f(x)=2인 x는 2개, f(x)=4인 x는 4개이다.",
            "(나) 7 이하의 모든 자연수 x에 대하여 f(x)+f(x+1) ≠ f(x+2)이다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 3, "ans": 110, "src": "2025학년도 사관학교 7월 확통 28", "jum": "4점",
        "lead": "숫자 1,1,2,2,4,4,4가 하나씩 적힌 7장의 카드를 모두 한 번씩 사용하여 일렬로 나열할 때, 이웃한 두 카드 수의 차를 차례로 a,b,c,d,e,f라 하자. a+b+c+d+e+f의 값이 짝수가 되도록 나열하는 경우의 수를 구하시오. (단, 같은 숫자 카드끼리는 구별하지 않는다.)",
        "conds": [],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 3, "ans": 158, "src": "2023학년도 경찰대 7월 9", "jum": "4점",
        "lead": "집합 A={1,2,3,4,5}에서 A로의 함수 중 다음 조건을 만족시키는 함수 f의 개수를 구하시오.",
        "conds": [
            "(가) log f(x)는 일대일함수가 아니다.",
            "(나) log{f(1)+f(2)+f(3)} = 2log2 + log3",
            "(다) log f(4) + log f(5) ≤ 1",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 3, "ans": 720, "src": "2022 교육청 고3 4월 확통 30", "jum": "4점",
        "lead": "집합 X={1,2,3,4,5}에 대하여 다음 조건을 만족시키는 함수 f:X→X의 개수를 구하시오.",
        "conds": [
            "(가) f(1)+f(2)+f(3)+f(4)+f(5)는 짝수이다.",
            "(나) 함수 f의 치역의 원소의 개수는 3이다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 3, "ans": 176, "src": "2020 교육청 고3 4월 20 (과정형)", "jum": "4점",
        "lead": "집합 X={1,2,3,4,5}, 함수 f:X→X의 치역을 A, f∘f의 치역을 B라 하자. n(A)≥3, A의 모든 원소의 합이 3의 배수, n(A)>n(B)를 만족시킨다. 과정 중 (가)=p, (나)=q, (다)=r일 때 p+q+r의 값을 구하시오.",
        "conds": [
            "(가) A={1,2,3}, B={1}일 때 함수 f의 개수",
            "(나) A={1,2,3}, B={1,2}일 때 함수 f의 개수",
            "(다) A={1,2,4,5}, n(B)<4일 때 함수 f의 개수",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 4, "ans": 201, "src": "2021학년도 평가원 고3 11월 29", "jum": "4점",
        "lead": "네 학생 A,B,C,D에게 검은색 모자 6개와 흰색 모자 6개를 다음 규칙에 따라 남김없이 나누어 주는 경우의 수를 구하시오. (단, 같은 색 모자끼리는 구별하지 않는다.)",
        "conds": [
            "(가) 각 학생은 1개 이상의 모자를 받는다.",
            "(나) 학생 A가 받은 검은색 모자의 개수는 4 이상이다.",
            "(다) 흰색보다 검은색을 더 많이 받는 학생은 A를 포함하여 2명뿐이다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 4, "ans": 33, "src": "2022 교육청 고3 3월 확통 27", "jum": "",
        "lead": "같은 종류의 책 8권과, 각 칸에 최대 5권·5권·8권을 꽂을 수 있는 3개의 칸으로 된 책장이 있다. 이 책 8권을 남김없이 나누어 꽂는 경우의 수를 구하시오. (단, 비어 있는 칸이 있을 수 있다.)",
        "conds": [],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 4, "ans": 117, "src": "2024 교육청 고3 3월 확통 29", "jum": "4점",
        "lead": "세 학생에게 서로 다른 종류의 초콜릿 3개와 같은 종류의 사탕 5개를 다음 규칙에 따라 남김없이 나누어 주는 경우의 수를 구하시오. (단, 사탕을 받지 못하는 학생이 있을 수 있다.)",
        "conds": [
            "(가) 적어도 한 명의 학생은 초콜릿을 받지 못한다.",
            "(나) 각 학생이 받는 초콜릿 수와 사탕 수의 합은 2 이상이다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 4, "ans": 330, "src": "2025 교육청 고3 3월 확통 30", "jum": "4점",
        "lead": "검은 공 4개와 흰 공 4개를 5명 A,B,C,D,E에게 다음 규칙으로 남김없이 나누어 주는 경우의 수를 구하시오. (단, 같은 색 공끼리는 구별하지 않고, 공을 받지 못하는 학생이 있을 수 있다.)",
        "conds": [
            "(가) 세 학생 A,B,C가 받는 공 개수의 합은 홀수이다.",
            "(나) 학생 D가 받는 공의 개수는 학생 E가 받는 공의 개수의 2배이다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 4, "ans": 120, "src": "2025 교육청 고3 5월 확통 26", "jum": "3점",
        "lead": "흰 공 5개와 검은 공 10개를 네 주머니 A,B,C,D에 다음 규칙으로 남김없이 나누어 넣는 경우의 수를 구하시오. (단, 같은 색 공끼리는 구별하지 않고, 검은 공을 넣지 않는 주머니가 있을 수 있다.)",
        "conds": [
            "(가) 각 주머니에 흰 공을 1개 이상씩 넣는다.",
            "(나) A,B,C에 넣는 흰 공 개수의 합은 D에 넣는 검은 공 개수와 같다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 5, "ans": 108, "src": "2025학년도 평가원 고3 6월 확통 30", "jum": "4점",
        "lead": "집합 X={-2,-1,0,1,2}에 대하여 다음 조건을 만족시키는 함수 f:X→X의 개수를 구하시오.",
        "conds": [
            "(가) X의 모든 원소 x에 대하여 x+f(x) ∈ X 이다.",
            "(나) x=-2,-1,0,1일 때 f(x) ≥ f(x+1)이다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 5, "ans": 65, "src": "2022 교육청 고3 3월 확통 29", "jum": "4점",
        "lead": "두 집합 X={1,2,3,4,5}, Y={-1,0,1,2,3}에 대하여 다음 조건을 만족시키는 함수 f:X→Y의 개수를 구하시오.",
        "conds": [
            "(가) f(1) ≤ f(2) ≤ f(3) ≤ f(4) ≤ f(5)",
            "(나) f(a)+f(b)=0을 만족시키는 X의 서로 다른 두 원소 a,b가 존재한다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 5, "ans": 115, "src": "2023학년도 평가원 고3 6월 확통 29", "jum": "4점",
        "lead": "집합 X={1,2,3,4,5}에 대하여 다음 조건을 만족시키는 함수 f:X→X의 개수를 구하시오.",
        "conds": [
            "(가) f(f(1))=4",
            "(나) f(1) ≤ f(3) ≤ f(5)",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 5, "ans": 48, "src": "2024 교육청 고3 10월 확통 29", "jum": "4점",
        "lead": "두 집합 X={1,2,3,4}, Y={0,1,2,3,4,5}에 대하여 다음 조건을 만족시키는 함수 f:X→Y의 개수를 구하시오.",
        "conds": [
            "(가) x=1,2,3일 때 f(x) ≤ f(x+1)이다.",
            "(나) f(a)=a인 X의 원소 a의 개수는 1이다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 5, "ans": 80, "src": "2025학년도 사관학교 7월 확통 27", "jum": "3점",
        "lead": "집합 X={1,2,3,4,5}에 대하여 다음 조건을 만족시키는 함수 f:X→X의 개수를 구하시오.",
        "conds": [
            "(가) x=1,2,3일 때 f(x) ≤ f(x+1)이다.",
            "(나) 함수 f의 치역의 원소의 개수는 2이다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 6, "ans": 206, "src": "2021 교육청 고3 4월 확통 30", "jum": "4점",
        "lead": "다음 조건을 만족시키는 14 이하의 네 자연수 x₁,x₂,x₃,x₄의 모든 순서쌍 (x₁,x₂,x₃,x₄)의 개수를 구하시오.",
        "conds": [
            "(가) x₁+x₂+x₃+x₄ = 34",
            "(나) x₁과 x₃은 홀수이고 x₂와 x₄는 짝수이다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 6, "ans": 74, "src": "2021학년도 평가원 고3 6월 27", "jum": "4점",
        "lead": "다음 조건을 만족시키는 음이 아닌 정수 a,b,c,d의 모든 순서쌍 (a,b,c,d)의 개수를 구하시오.",
        "conds": [
            "(가) a+b+c+d = 6",
            "(나) a,b,c,d 중에서 적어도 하나는 0이다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 6, "ans": 332, "src": "2021학년도 평가원 예시문항 확통 29", "jum": "4점",
        "lead": "다음 조건을 만족시키는 음이 아닌 정수 a,b,c,d의 모든 순서쌍 (a,b,c,d)의 개수를 구하시오.",
        "conds": [
            "(가) a+b+c+d = 12",
            "(나) a≠2이고 a+b+c≠10이다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 6, "ans": 31, "src": "2021학년도 경찰대 7월 24", "jum": "4점",
        "lead": "다음 조건을 만족시키는 자연수 a,b,c,d,e의 모든 순서쌍 (a,b,c,d,e)의 개수를 구하시오.",
        "conds": [
            "(가) ab(c+d+e) = 12",
            "(나) a,b,c,d,e 중에서 적어도 2개는 짝수이다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
    {
        "t": 6, "ans": 75, "src": "2024 교육청 고3 5월 확통 29", "jum": "4점",
        "lead": "다음 조건을 만족시키는 자연수 a,b,c,d,e의 모든 순서쌍 (a,b,c,d,e)의 개수를 구하시오.",
        "conds": [
            "(가) a+b+c+d+e = 11",
            "(나) a+b는 짝수이다.",
            "(다) a,b,c,d,e 중에서 짝수의 개수는 2 이상이다.",
        ],
        "sol": "",   # ← 해설을 여기에 채우면 자동으로 표시됩니다
    },
]


# ============================================================
# 3) 문항 고유번호 부여  (구글 시트 기록의 안전한 키)
#    PROBLEMS 순서에 맞는 원본 문항번호. 새 문제를 추가하면 여기에도 번호를 더하세요.
# ============================================================
_PROBLEM_IDS = [4, 5, 6, 7, 8, 15, 16, 17, 18, 19, 23, 24, 25, 26, 27,
                32, 33, 34, 35, 36, 40, 41, 42, 43, 44, 57, 58, 59, 60, 61,
                78, 79, 80, 81, 82]
for _p, _pid in zip(PROBLEMS, _PROBLEM_IDS):
    _p["id"] = _pid
for _i, _p in enumerate(PROBLEMS):          # 번호가 모자라면 인덱스로 보완
    _p.setdefault("id", 1000 + _i)


# ============================================================
# 4) 채점 로직
#    경우의 수 문제는 정답이 '정수 하나' → 정확히 일치하면 정답.
# ============================================================
def is_correct(problem, user_answer):
    return int(user_answer) == problem["ans"]


# ============================================================
# 확장 포인트 ③  구글 시트 저장 / 이어서 하기
#    .streamlit/secrets.toml 에 sheet_id 와 [gcp_service_account] 를 넣으면 동작.
#    설정이 없으면 자동으로 '이번 세션만 유지' 모드가 됩니다.
# ============================================================
def sheets_available():
    try:
        return "gcp_service_account" in st.secrets and "sheet_id" in st.secrets
    except Exception:
        return False


@st.cache_resource(show_spinner=False)
def _sheet():
    import gspread
    from google.oauth2.service_account import Credentials
    scopes = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]), scopes=scopes)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(st.secrets["sheet_id"])
    try:
        ws = sh.worksheet("records")
    except Exception:
        ws = sh.add_worksheet("records", rows=2000, cols=6)
        ws.append_row(["학번", "문항", "유형", "정답여부", "학생답", "시각"])
    return ws


def save_result(student_id, problem, ok, user_answer):
    """채점 결과 한 줄을 구글 시트에 추가. 학번이 없거나 미설정이면 건너뜀."""
    if not (student_id and sheets_available()):
        return
    try:
        ws = _sheet()
        ts = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        type_name = TYPES[problem["t"]]["cat"] + " · " + TYPES[problem["t"]]["sub"]
        ws.append_row([student_id, problem["id"], type_name,
                       "O" if ok else "X", int(user_answer), ts])
    except Exception as e:
        st.warning(f"기록 저장 실패: {e}")


def load_progress(student_id):
    """해당 학번의 저장 기록을 {문항id: 최신 정답여부} 로 반환."""
    out = {}
    if not (student_id and sheets_available()):
        return out
    try:
        ws = _sheet()
        for r in ws.get_all_records():      # 과거→최신 순으로 덮어써 최신값 유지
            if str(r.get("학번")) == str(student_id):
                out[int(r.get("문항"))] = (r.get("정답여부") == "O")
    except Exception as e:
        st.warning(f"기록 불러오기 실패: {e}")
    return out


# ============================================================
# 확장 포인트 ①  해설
# ============================================================
def show_explanation(problem):
    sol = problem.get("sol", "").strip()
    if sol:
        st.info(sol)
    else:
        st.caption("· 해설 미등록 — PROBLEMS의 \"sol\" 값을 채우면 여기에 표시됩니다.")


# ============================================================
# 확장 포인트 ②  AI 풀이 피드백  (선택 기능)
#    .streamlit/secrets.toml 에 아래 한 줄을 넣어야 동작합니다.
#        ANTHROPIC_API_KEY = "sk-ant-..."
#    키가 없으면 버튼 자체가 숨겨집니다.
# ============================================================
def get_ai_feedback(problem, user_answer):
    import anthropic
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    prompt = f"""당신은 한국 고등학교 수학(확률과 통계) 선생님입니다.
학생이 아래 '경우의 수' 문제를 풀었는데 틀렸습니다.
어떤 개념이나 실수(예: 중복 제거 누락, 순서 고려 오류, 조건 빠뜨림)를
점검해야 하는지 3~4줄로 친절하게 짚어 주세요.
단, 정답 숫자는 절대 직접 알려주지 마세요. 스스로 다시 풀도록 힌트만 줍니다.

[문제] {problem['lead']}
[조건] {' / '.join(problem.get('conds', []))}
[정답(교사용, 노출 금지)] {problem['ans']}
[학생이 낸 답] {user_answer}"""
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",   # 빠르고 저렴. 더 깊은 풀이 분석은 상위 모델로 교체
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


# ============================================================
# 확장 포인트 ④  인증  (자리만 비워둠)
# ============================================================
def check_license(key):
    return True  # TODO: 라이선스키 검증(만료일 등). 예전 방식 재활용 가능.


def has_api_key():
    try:
        return "ANTHROPIC_API_KEY" in st.secrets
    except Exception:
        return False


# ============================================================
# 4) 화면
# ============================================================
st.set_page_config(page_title="경우의 수 · 채점 연습", page_icon="🎯", layout="centered")

if "results" not in st.session_state:
    st.session_state.results = {}   # {문항 인덱스: True/False}

st.caption("코드스튜디오 입시연구소")
st.title("경우의 수 · 채점 연습")

# ---- 사이드바: 학번(이어서 하기) ----
with st.sidebar:
    st.subheader("학생")
    student = st.text_input("학번 (이어서 풀려면 입력)", key="student_input").strip()
    if student and st.session_state.get("loaded_for") != student:
        prog = load_progress(student)                       # {문항id: 정답여부}
        id2idx = {p["id"]: i for i, p in enumerate(PROBLEMS)}
        st.session_state.results = {id2idx[pid]: ok
                                    for pid, ok in prog.items() if pid in id2idx}
        st.session_state.loaded_for = student
    if not sheets_available():
        st.caption("기록 저장 미설정 — 이번 세션만 유지됩니다.")
    elif student:
        st.caption(f"{student} · 저장된 풀이 {len(st.session_state.results)}문항 불러옴")
    st.divider()

# ---- 사이드바: 유형 선택 ----
cats = list(dict.fromkeys(t["cat"] for t in TYPES))
with st.sidebar:
    st.subheader("유형 선택")
    cat = st.selectbox("분류", cats)
    subs = [(i, t["sub"]) for i, t in enumerate(TYPES) if t["cat"] == cat]
    sub_labels = [s for _, s in subs]
    sub_choice = st.radio("소제목", sub_labels)
    type_idx = next(i for i, s in subs if s == sub_choice)

    pool = [i for i, p in enumerate(PROBLEMS) if p["t"] == type_idx]
    st.divider()
    solved = sum(1 for i in pool if i in st.session_state.results)
    correct = sum(1 for i in pool if st.session_state.results.get(i))
    st.caption(f"이 유형 {len(pool)}문항 · 푼 문항 {solved} · 정답 {correct}")

# ---- 문항 선택 ----
labels = [f"{k+1}번   ({PROBLEMS[i]['src']})" for k, i in enumerate(pool)]
pick = st.selectbox("문항", range(len(pool)), format_func=lambda k: labels[k])
idx = pool[pick]
p = PROBLEMS[idx]

# ---- 문제 표시 ----
st.markdown(f"### {TYPES[type_idx]['cat']} · {TYPES[type_idx]['sub']}")
meta = p["src"] + (f"  ·  {p['jum']}" if p.get("jum") else "")
st.caption(meta)
st.write(p["lead"])
for c in p.get("conds", []):
    st.markdown(f"- {c}")

# ---- 답 입력 & 채점 ----
c1, c2 = st.columns([3, 1])
with c1:
    user_answer = st.number_input("정답(자연수) 입력", min_value=0, step=1, value=0, key=f"ans_{idx}")
with c2:
    st.write("")
    graded = st.button("채점", use_container_width=True, type="primary")

if graded:
    ok = is_correct(p, user_answer)
    st.session_state.results[idx] = ok
    save_result(st.session_state.get("student_input", "").strip(), p, ok, user_answer)  # 확장 포인트 ③
    if ok:
        st.success("정답입니다!  ⭕")
    else:
        st.error("오답입니다. 다시 풀어보세요.  ❌")
elif idx in st.session_state.results:
    st.caption("○ 정답 처리됨" if st.session_state.results[idx] else "✕ 오답 처리됨")

# ---- 오답일 때: 해설 / AI 힌트 ----
if st.session_state.results.get(idx) is False:
    with st.expander("해설 보기"):
        show_explanation(p)                  # 확장 포인트 ①
    if has_api_key():
        if st.button("AI 힌트 받기"):
            with st.spinner("피드백 생성 중..."):
                st.write(get_ai_feedback(p, user_answer))   # 확장 포인트 ②

# ---- 전체 점수 ----
st.divider()
total = len(st.session_state.results)
total_ok = sum(1 for v in st.session_state.results.values() if v)
rate = round(total_ok / total * 100) if total else 0
st.metric("전체 정답률", f"{rate}%", f"{total_ok} / {total} 문항")
