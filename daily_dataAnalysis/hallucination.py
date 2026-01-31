# ============================================================
# 미션 4) 환각(Hallucination) 제로 논리 추론 봇 만들기
# ============================================================
#
# [문제 설명]
# LLM(대규모 언어 모델)은 그럴듯한 문장을 생성하는 데 강하지만,
# "모르는 것"도 마치 아는 것처럼 꾸며서 말하는 문제가 있습니다.
# 이 현상을 보통 환각(Hallucination)이라고 부릅니다.
#
# 이 미션의 목표는 "절대 환각을 하지 않는" 봇을 만드는 것입니다.
# 다만 현실적으로 LLM을 100% 무오류로 만들기는 어렵기 때문에,
# 여기서 말하는 "환각 제로"는 다음과 같은 행동 규칙을 의미합니다:
#
# - 근거가 없으면 단정하지 않는다.
# - 검증할 수 없으면 "모른다"라고 말하고, 필요한 정보를 되묻는다.
# - 계산/논리/문서 근거가 있는 것만 결론으로 제시한다.
# - 출처(근거)와 검증 과정이 없는 답변은 금지한다.
#
# 비유로 이해하기:
# - 일반 LLM: "말 잘하는 사람" (자신감 있게 말하지만 사실 확인은 안 할 수도 있음)
# - 환각 제로 봇: "감사(Auditor) + 연구원" (근거/증거 없으면 결론을 내리지 않음)
#
# [이 봇이 해결하려는 문제]
# - 사용자가 사실 질문(예: 최신 뉴스, 특정 통계)을 했을 때 모델이 추측으로 답하는 문제
# - 논리/수학 문제에서 중간 계산이 틀리거나 결론이 바뀌는 문제
# - 근거 없이 '확실하다'고 표현하는 문제
#
# ------------------------------------------------------------
# [해결해야 하는 단계별 과정(코드 작성 금지: 주석으로만)]
# ------------------------------------------------------------
#
# Step 0) 목표 정의 및 출력 규격 먼저 확정하기
# - "환각 제로"를 테스트 가능한 규칙으로 정의한다.
#   예) (a) 근거 없는 단정 금지, (b) 불확실하면 모름 처리, (c) 검증 로그 포함
# - 응답 출력 포맷을 고정한다.
#   예) {결론, 근거, 검증, 불확실성, 추가질문}
#
# -----------------------------
# Step 0) 코드: 출력 규격(Contract)
# -----------------------------
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, Tuple

import ast
import json
import os
import re
import time

from dotenv import load_dotenv
import google.generativeai as genai


AnswerType = Literal["reasoning", "fact", "opinion", "refusal"]


@dataclass
class AnswerContract:
    """
    Step 0의 '출력 규격'을 코드로 고정한 데이터 구조.
    """

    conclusion: str
    evidence: List[str]
    verification: List[str]
    uncertainty: str
    follow_up_questions: List[str]
    answer_type: AnswerType

    def to_dict(self) -> Dict[str, Any]:
        return {
            "answerType": self.answer_type,
            "conclusion": self.conclusion,
            "evidence": self.evidence,
            "verification": self.verification,
            "uncertainty": self.uncertainty,
            "followUpQuestions": self.follow_up_questions,
        }


# Step 1) 입력 타입 분류기 설계하기 (질문을 먼저 분류)
# - 사실 질의(lookup 필요): "2026년 xx는?" "어느 회사가?"
# - 추론/계산 질의(reasoning 가능): 수학, 로직 퍼즐, 코드 논리, 규칙 기반 추론
# - 의견/창작(정답 없음): "추천해줘", "에세이 써줘"
# - 분류 결과에 따라 "허용되는 답변 방식"을 바꾼다.
#
# -----------------------------
# Step 1) 코드: 입력 분류기
# -----------------------------
def classify_question(question: str) -> AnswerType:
    """
    환각을 줄이기 위한 '보수적인' 분류기.

    - fact: 외부 근거가 없으면 답을 확정하면 안 되는 질문
    - reasoning: 내부 계산/논리로 검증 가능한 질문
    - opinion: 정답이 고정되지 않아 조건/선호를 되물어야 안전한 질문
    """
    q = question.strip().lower()

    if re.search(r"(확률|경우의\s*수|주사위|수학|계산|미분|적분)", q):
        return "reasoning"

    # 간단 산술식 (2+2, 10/3 등)
    if re.search(r"[\d\)\]]\s*[\+\-\*/%]\s*[\d\(\[]", q):
        return "reasoning"

    # 최신/현실 세계 사실(연도/날짜/오늘/뉴스/금리 등)
    if re.search(r"(기준금리|주가|뉴스|현재|요즘|오늘|어제|이번\s*주|202\d|20\d{2})", q):
        return "fact"

    # 사실 확인 성격
    if re.search(r"(누구|어느\s*회사|어디|언제|몇\s*살|몇\s*년도)", q):
        return "fact"

    # 추천/의견/창작
    if re.search(r"(추천|의견|생각|에세이|소설|시|소개해줘|골라줘)", q):
        return "opinion"

    # 애매하면 fact로 두고(=근거 없으면 보류) 환각을 줄인다.
    return "fact"


# Step 2) 지식 정책(knowledge policy) 정하기
# - 내부 지식만으로 답해도 되는 범위 vs 반드시 근거(문서/데이터)가 필요한 범위
# - 외부 근거 없이 답하면 안 되는 질문의 예시 정의
# - "출처 요구 규칙" 정의
#   예) 사실 질의는 반드시 출처/근거가 제공되지 않으면 모름 처리
#
# -----------------------------
# Step 2) 코드: 지식 정책(Policy)
# -----------------------------
@dataclass
class KnowledgePolicy:
    """
    '언제 답할 수 있는가'를 규칙으로 고정하는 정책.
    환각 제로의 본질은 이 정책을 어기지 않는 것입니다.
    """

    require_sources_for_facts: bool = True
    allow_fact_answer_without_sources: bool = False
    allow_only_verifiable_reasoning: bool = True

    def can_answer_fact(self, sources: Optional[List[Dict[str, str]]]) -> bool:
        if self.allow_fact_answer_without_sources:
            return True
        if self.require_sources_for_facts and not sources:
            return False
        return True


# Step 3) 근거 확보 전략 선택하기 (중요: 두 갈래 중 선택/결합 가능)
# - 옵션 A: RAG/검색 도입 (외부 데이터/문서가 있을 때)
#   1) 사용자 질문 → 검색 쿼리 생성
#   2) 문서/데이터 검색 → Top-k 근거 수집
#   3) 근거 요약 + 근거 인용 형태로 답변 생성
#   4) 근거에 없는 내용은 "모름" 처리
#
# - 옵션 B: 외부 도구 없이 가능한 검증 중심 (계산/논리 문제에 강함)
#   1) 문제를 작은 단위로 분해(전제/규칙/목표)
#   2) 단계별로 추론/계산 수행
#   3) 자체 검증(역산, 경계조건 체크, 모순 검사)
#   4) 검증 실패 시 결론 보류 및 추가 정보 요청
#
# -----------------------------
# Step 3) 코드: 근거 확보(Option A) + 검증 가능한 추론(Option B)
# -----------------------------
def normalize_sources(sources: Optional[List[Dict[str, str]]]) -> List[Dict[str, str]]:
    """
    sources 입력을 정규화한다.
    기대 형식:
      [{"title": "...", "url": "...", "content": "..."}, ...]
    """
    if not sources:
        return []
    normalized: List[Dict[str, str]] = []
    for s in sources:
        title = str(s.get("title", "")).strip()
        url = str(s.get("url", "")).strip()
        content = str(s.get("content", "")).strip()
        if content:
            normalized.append({"title": title, "url": url, "content": content})
    return normalized


def build_source_pack(sources: List[Dict[str, str]], max_chars: int = 6000) -> str:
    """
    LLM에게 전달할 '근거 묶음' 문자열을 만든다(토큰 제한 대비).
    """
    chunks: List[str] = []
    used = 0
    for i, s in enumerate(sources, 1):
        block = f"[SOURCE {i}]\nTITLE: {s['title']}\nURL: {s['url']}\nCONTENT:\n{s['content']}\n"
        if used + len(block) > max_chars:
            break
        chunks.append(block)
        used += len(block)
    return "\n".join(chunks).strip()


class SafeMathSolver:
    """
    외부 데이터 없이도 '검증 가능한' 문제만 답하기 위한 솔버.
    - 산술식 계산
    - 주사위 2개 합 확률(예시)
    """

    @staticmethod
    def _safe_eval(expr: str) -> Optional[Tuple[float, List[str]]]:
        try:
            tree = ast.parse(expr, mode="eval")
        except Exception:
            return None

        allowed_nodes = (
            ast.Expression,
            ast.BinOp,
            ast.UnaryOp,
            ast.Add,
            ast.Sub,
            ast.Mult,
            ast.Div,
            ast.Pow,
            ast.Mod,
            ast.FloorDiv,
            ast.USub,
            ast.UAdd,
            ast.Constant,
            ast.Load,
        )
        for node in ast.walk(tree):
            if not isinstance(node, allowed_nodes):
                return None
            if isinstance(node, ast.Constant) and not isinstance(node.value, (int, float)):
                return None

        result = eval(compile(tree, filename="<safe_eval>", mode="eval"), {"__builtins__": {}}, {})
        steps = [f"산술식 해석: {expr}", f"계산 결과: {result}"]
        return float(result), steps

    @staticmethod
    def _dice_two_sum_probability(target_sum: int) -> Tuple[str, List[str]]:
        outcomes = [(a, b) for a in range(1, 7) for b in range(1, 7)]
        favorable = [(a, b) for (a, b) in outcomes if a + b == target_sum]
        num = len(favorable)
        den = len(outcomes)
        prob = num / den
        steps = [
            "모델 없이 계산 가능한 확률 문제로 분류",
            f"전체 경우의 수: 6*6 = {den}",
            f"유리한 경우의 수(합이 {target_sum}): {num} = {favorable}",
            f"확률 = {num}/{den} = {prob}",
        ]
        conclusion = f"두 주사위를 던져 합이 {target_sum}일 확률은 {num}/{den} = {prob} 입니다."
        return conclusion, steps

    def solve(self, question: str) -> Optional[Tuple[str, List[str]]]:
        q = question.strip()

        # 주사위 2개 합 확률 패턴
        m = re.search(r"주사위\s*2개.*합이\s*(\d+)", q)
        if m:
            target = int(m.group(1))
            return self._dice_two_sum_probability(target)

        # 산술식만 뽑아 계산 시도
        expr_match = re.search(r"([0-9\.\s\+\-\*/\(\)\*\*%]+)", q)
        if expr_match:
            expr = expr_match.group(1).strip()
            if re.search(r"[\+\-\*/%]", expr):
                solved = self._safe_eval(expr)
                if solved:
                    value, steps = solved
                    return f"{expr} = {value}", steps

        return None


# Step 4) 검증(Verification) 레이어 설계하기
# - "답변 생성"과 "검증"을 분리한다.
# - 검증 체크리스트 예:
#   - 수학: 단위/부호/범위/역산
#   - 논리: 전제 누락/모순/반례 존재 여부
#   - 사실: 출처에 존재하는 문장인지(근거 스팬 확인)
# - 검증 결과에 따라:
#   - 통과: 결론 + 근거 + 검증 로그 출력
#   - 실패: 결론 보류 + 실패 사유 + 필요한 정보 질문
#
# -----------------------------
# Step 4) 코드: 검증 레이어
# -----------------------------
class Verifier:
    """
    검증기는 '환각을 막는 마지막 문지기' 역할.
    여기서는 교육용으로 단순하지만, 원칙은 동일:
    - 검증 못하면 결론을 확정하지 않는다.
    """

    @staticmethod
    def verify_reasoning(steps: List[str]) -> Tuple[bool, List[str]]:
        checks: List[str] = ["검증: 계산/나열 로그 존재 여부 확인"]
        if not steps:
            checks.append("실패: 검증 로그가 비어있음")
            return False, checks
        checks.append("통과: 검증 로그가 존재함(내부 계산 기반)")
        return True, checks

    @staticmethod
    def verify_fact_has_quotes(answer_text: str, sources: List[Dict[str, str]]) -> Tuple[bool, List[str]]:
        """
        사실 답변은 '인용문이 sources에 실제로 존재'해야 통과시키는 매우 보수적 검증.
        """
        checks: List[str] = ["검증: sources 제공 여부 확인"]
        if not sources:
            checks.append("실패: sources가 없어 사실 답변 검증 불가")
            return False, checks

        # "..." 형태의 인용문 추출
        quotes = re.findall(r"\"([^\"]+)\"", answer_text)
        if not quotes:
            checks.append("실패: 인용문이 없어 sources 기반 검증 불가")
            return False, checks

        corpus = "\n".join([s["content"] for s in sources])
        missing = [q for q in quotes if q not in corpus]
        if missing:
            checks.append(f"실패: 인용문이 sources에 없음(상위 1개): {missing[:1]}")
            return False, checks

        checks.append("통과: 인용문이 sources에서 발견됨")
        return True, checks


# Step 5) 출력 포맷(Answer Contract) 고정하기
# - 사용자에게 "왜 이렇게 답했는지"를 항상 보여준다.
# - 예시 포맷(개념):
#   - 결론: (짧게)
#   - 근거: (문서/계산/규칙)
#   - 검증: (체크 항목 통과/실패)
#   - 불확실성: (모름/가정/추가 데이터 필요)
#   - 추가 질문: (정보가 부족하면 딱 1~3개)
#
# -----------------------------
# Step 5) 코드: 포맷터/응답 빌더
# -----------------------------
def build_refusal(why: str, follow_ups: Optional[List[str]] = None) -> AnswerContract:
    follow_ups = [q for q in (follow_ups or []) if q.strip()][:3]
    return AnswerContract(
        conclusion=f"현재 정보만으로는 답변을 확정할 수 없습니다. ({why})",
        evidence=[],
        verification=[f"거절/보류: {why}"],
        uncertainty="검증 가능한 근거가 부족합니다.",
        follow_up_questions=follow_ups,
        answer_type="refusal",
    )


def build_opinion_response() -> AnswerContract:
    follow_ups = [
        "어떤 목적(학습/업무/프로젝트)인지 알려주실 수 있나요?",
        "현재 수준(초급/중급/고급)과 선호(실습 위주/이론 위주)는 어떤가요?",
    ]
    return AnswerContract(
        conclusion="이 질문은 정답이 하나로 고정되지 않는 성격이라, 조건을 확인한 뒤 맞춤 제안을 드리는 게 안전합니다.",
        evidence=["의견/추천 유형은 사용자의 선호/제약조건에 따라 답이 달라짐"],
        verification=["검증: 사실 단정 대신 조건 질문으로 전환"],
        uncertainty="선호/제약조건이 없어 일반론으로 단정하면 환각 위험이 큽니다.",
        follow_up_questions=follow_ups[:3],
        answer_type="opinion",
    )


# Step 6) 안전장치(Guardrail) 규칙 만들기
# - 금지 표현/행동 예:
#   - "확실합니다" 같은 단정어 남발 금지
#   - 출처 없이 수치/연도/고유명사 생성 금지
# - 허용 행동 예:
#   - "제가 가진 정보만으로는 확인할 수 없습니다."
#   - "다음 정보를 주시면 정확히 답할 수 있습니다: ..."
#
# -----------------------------
# Step 6) 코드: 가드레일(금지/허용) 구현
# -----------------------------
FORBIDDEN_ASSERTIVE_PHRASES = ["확실합니다", "100%입니다", "틀림없습니다", "무조건"]


def apply_guardrails(text: str) -> str:
    out = text
    for phrase in FORBIDDEN_ASSERTIVE_PHRASES:
        out = out.replace(phrase, "단정할 수 없습니다(근거가 필요합니다)")
    return out


# Step 7) 테스트/평가 방법 만들기 (Pass/Fail 기준)
# - 환각 유발 질문 세트 준비:
#   - 최신성 필요한 질문(모델이 추측하기 쉬움)
#   - 애매한 질문(전제가 누락됨)
#   - 함정 수학 문제(부호/단위)
# - Pass 기준 예:
#   - 근거 없는 단정 0회
#   - 불확실 시 모름 처리 + 추가 질문 제시
#   - 계산 문제는 검증 로그 포함
#
# -----------------------------
# Step 7) 코드: 테스트/평가(간단 러너)
# -----------------------------
def run_smoke_tests(bot: "HallucinationZeroBot") -> None:
    tests = [
        {"q": "2026년 1월 1일 대한민국 기준금리는?", "sources": None},
        {"q": "2개의 주사위를 던질 때 합이 7일 확률은?", "sources": None},
        {"q": "2+2*3은?", "sources": None},
        {"q": "파이썬 입문 책 추천해줘", "sources": None},
    ]
    for i, t in enumerate(tests, 1):
        print("=" * 60)
        print(f"[TEST {i}] Q: {t['q']}")
        ans = bot.answer(t["q"], sources=t["sources"])
        print(json.dumps(ans.to_dict(), ensure_ascii=False, indent=2))


# Step 8) 운영 관점(실전 적용) 고려사항 메모
# - 토큰 제한: 히스토리/근거가 길면 요약/슬라이싱 필요
# - 비용: 검색/검증 단계가 늘어날수록 비용 증가 → 캐시/샘플링 전략 필요
# - 장애/빈 응답: LLM 응답이 비어있는 경우(예: finish_reason) 처리 필요
#
# -----------------------------
# Step 8) 코드: 운영 유틸(빈 응답 대비)
# -----------------------------
def gemini_setup() -> None:
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def safe_get_text(response: Any) -> Optional[str]:
    try:
        if not response.candidates or not response.candidates[0].content.parts:
            return None
        return str(response.text).strip()
    except Exception:
        return None


# ------------------------------------------------------------
# (통합) Step들을 조합한 파이프라인
# ------------------------------------------------------------
class HallucinationZeroBot:
    """
    - fact: sources 없으면 보류
    - reasoning: 내부에서 검증 가능한 것만 답변
    - opinion: 조건을 되물어 환각을 줄임
    """

    def __init__(self, policy: Optional[KnowledgePolicy] = None, model_name: str = "gemini-3-flash-preview"):
        gemini_setup()
        self.policy = policy if policy else KnowledgePolicy()
        self.model = genai.GenerativeModel(model_name)
        self.solver = SafeMathSolver()
        self.verifier = Verifier()

    def answer(self, question: str, sources: Optional[List[Dict[str, str]]] = None) -> AnswerContract:
        qtype = classify_question(question)
        sources_norm = normalize_sources(sources)

        if qtype == "opinion":
            return build_opinion_response()

        if qtype == "fact" and not self.policy.can_answer_fact(sources_norm):
            return build_refusal(
                why="사실 질의는 외부 근거(sources)가 없으면 환각 위험이 큽니다",
                follow_ups=[
                    "답변에 사용할 공식 출처(링크/문서 내용)를 제공해주실 수 있나요?",
                    "원하시는 기준 시점(날짜/시간대)과 범위를 알려주실 수 있나요?",
                ],
            )

        if qtype == "reasoning":
            solved = self.solver.solve(question)
            if not solved and self.policy.allow_only_verifiable_reasoning:
                return build_refusal(
                    why="현재 구현은 '자동 검증 가능한' 계산/추론만 답하도록 제한되어 있습니다",
                    follow_ups=[
                        "문제를 수학식(산술식) 형태로 줄여서 보내주실 수 있나요?",
                        "조건(전제/정의)을 더 명확히 적어주실 수 있나요?",
                    ],
                )

            if solved:
                conclusion, steps = solved
                ok, verify_log = self.verifier.verify_reasoning(steps)
                if not ok:
                    return build_refusal(why="검증 실패", follow_ups=["문제 조건을 다시 확인해 주세요."])
                return AnswerContract(
                    conclusion=apply_guardrails(conclusion),
                    evidence=steps,
                    verification=verify_log,
                    uncertainty="없음(내부 계산으로 검증됨)",
                    follow_up_questions=[],
                    answer_type="reasoning",
                )

        # fact + sources가 있으면: sources 범위 내에서만 답하도록 LLM에 요청
        if qtype == "fact":
            source_pack = build_source_pack(sources_norm)
            prompt = f"""
[ROLE]
You are an auditor building a zero-hallucination answer.

[RULES]
1) Use ONLY the content inside SOURCES.
2) If the answer is not in SOURCES, say you cannot verify it.
3) Include 1~3 direct quotes wrapped in double quotes (\"...\").
4) Do NOT paraphrase quotes. They must appear verbatim in SOURCES.
5) Output Korean.

[QUESTION]
{question}

[SOURCES]
{source_pack}
"""
            time.sleep(1)
            resp = self.model.generate_content(prompt)
            text = safe_get_text(resp)
            if not text:
                return build_refusal(why="LLM 응답이 비어있어 검증 불가", follow_ups=["sources를 더 짧게/명확하게 제공해 주세요."])

            ok, verify_log = self.verifier.verify_fact_has_quotes(text, sources_norm)
            if not ok:
                return build_refusal(
                    why="근거(인용) 검증 실패: sources에 없는 내용을 포함했을 가능성",
                    follow_ups=[
                        "sources 내용을 더 직접적으로(원문 그대로) 제공해주실 수 있나요?",
                        "질문 범위를 sources가 커버하는지 확인해 주세요.",
                    ],
                )

            return AnswerContract(
                conclusion=apply_guardrails(text),
                evidence=["sources 기반 인용 포함 답변(검증 통과)"],
                verification=verify_log,
                uncertainty="sources 범위 밖은 답변하지 않음",
                follow_up_questions=[],
                answer_type="fact",
            )

        return build_refusal(why="질문을 안전하게 검증할 수 없음", follow_ups=["질문 의도를 더 구체적으로 알려주세요."])


# ------------------------------------------------------------
# [예시(주석)] 기대되는 동작 예
# ------------------------------------------------------------
# Q) "2026년 1월 1일 대한민국 기준금리는?"
# - 분류: 사실 질의(lookup 필요)
# - 근거 없음(외부 데이터 연결 없음) → 결론 보류
# - A) "확인할 수 없습니다. 기준금리 정보(출처 링크/데이터)를 주시면 근거 기반으로 답하겠습니다."
#
# Q) "2개의 주사위를 던질 때 합이 7일 확률은?"
# - 분류: 계산/추론 가능
# - 계산: 유효한 경우의 수 6 / 전체 36 → 1/6
# - 검증: 합이 7인 조합 나열로 재검증
# - A) 결론 1/6 + 근거(조합) + 검증 로그
#
# ------------------------------------------------------------
# 다음 단계(나중에 코드 작성할 때) 힌트
# - (1) 질문 분류기 함수
# - (2) 답변 생성기 함수
# - (3) 검증기 함수
# - (4) 최종 포맷터 함수
# - (5) 테스트 케이스 러너
#

if __name__ == "__main__":
    bot = HallucinationZeroBot()
    run_smoke_tests(bot)
