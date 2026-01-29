"""
Problem 01) Titanic 생존 분석 (Pandas 기초)

목표
- Kaggle Titanic 데이터를 Pandas로 불러오고, 결측치/요약통계/그룹 분석을 수행한다.
- "생존율"을 다양한 기준으로 비교해 본다.
- (선택) 간단한 규칙 기반 예측을 만들어 submission 파일 형식을 흉내 내본다.

난이도
- Pandas 완전 기초 ~ 초급

데이터
# Kaggle 링크(데이터 받기): https://www.kaggle.com/competitions/titanic/data
# (대회 페이지)         : https://www.kaggle.com/competitions/titanic

준비
- train.csv, test.csv 를 이 파일과 같은 폴더(또는 원하는 경로)에 다운로드해 두세요.

제출물(권장)
- 문제를 푸는 코드 자체(이 파일)
- (선택) result/ 폴더에 분석 결과 csv 저장
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd  # type: ignore[import-not-found]


def main() -> None:
    """
    TODO 0) 경로 설정
    - 기본은 현재 파일 기준 폴더에서 train/test를 찾도록 해둠
    - 파일 위치가 다르면 data_dir 값을 바꾸세요.
    """
    here = Path(__file__).resolve().parent
    data_dir = here  # 필요 시 Path("...") 로 수정

    train_path = data_dir / "train.csv"
    test_path = data_dir / "test.csv"

    # TODO 1) 데이터 로드
    # - pd.read_csv()로 train/test를 읽어오세요.
    # - 읽어온 뒤 shape, head(처음 5행), info를 확인하세요.
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)

    print("train.shape:", train.shape)
    print("test.shape :", test.shape)
    print(train.head())
    print(train.info())

    # TODO 2) 결측치 확인
    # - train에서 결측치가 많은 컬럼 상위 5개를 찾아서 출력하세요.
    # 힌트: train.isna().sum().sort_values(ascending=False)
    # na_counts = ...
    # print(na_counts.head(5))

    # TODO 3) 타깃(생존) 분포 확인
    # - Survived 컬럼의 value_counts(), value_counts(normalize=True) 를 출력하세요.
    # print(train["Survived"].value_counts())
    # print(train["Survived"].value_counts(normalize=True))

    # TODO 4) 그룹별 생존율 비교 (핵심 연습)
    # - 성별(Sex)별 생존율
    # - 객실 등급(Pclass)별 생존율
    # - (조합) Sex & Pclass 별 생존율 (피벗테이블/그룹바이)
    # 힌트(선택):
    # - train.groupby("Sex")["Survived"].mean()
    # - train.pivot_table(index="Sex", columns="Pclass", values="Survived", aggfunc="mean")
    #
    # survival_by_sex = ...
    # survival_by_pclass = ...
    # survival_pivot = ...
    #
    # print(survival_by_sex)
    # print(survival_by_pclass)
    # print(survival_pivot)

    # TODO 5) 결측치 처리 연습
    # - Age 결측치를 중앙값으로 채우기(fillna)
    # - Embarked 결측치를 최빈값으로 채우기
    # - Cabin은 결측이 매우 많으니, "Cabin 여부" 파생변수(has_cabin) 만들기
    # 주의: 지금은 분석 연습이 목적이니, 완벽한 전처리는 아니어도 OK.
    # train2 = train.copy()
    # train2["Age"] = ...
    # train2["Embarked"] = ...
    # train2["has_cabin"] = ...

    # TODO 6) 파생변수로 다시 그룹 분석
    # - has_cabin 별 생존율 비교
    # print(train2.groupby("has_cabin")["Survived"].mean())

    # TODO 7) (선택) 아주 단순한 규칙 기반 예측 만들어보기
    # - 예: 여자면 1, 남자면 0 같은 규칙으로 test에 Survived 예측
    # - Kaggle 제출 형식(PassengerId, Survived)으로 CSV 저장
    #
    # pred = ...
    # submission = pd.DataFrame({"PassengerId": test["PassengerId"], "Survived": pred})
    # out_dir = here / "result"
    # os.makedirs(out_dir, exist_ok=True)
    # submission.to_csv(out_dir / "submission_rule_based.csv", index=False)
    # print("Saved:", out_dir / "submission_rule_based.csv")

    print("\nTODO들이 남아있습니다. 위 TODO 블록을 직접 채워서 실행해 보세요.")


if __name__ == "__main__":
    main()
