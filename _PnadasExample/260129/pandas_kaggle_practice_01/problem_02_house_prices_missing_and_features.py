"""
Problem 02) House Prices - 결측치/피처 살펴보기 (Pandas 초급)

목표
- Kaggle House Prices 데이터를 Pandas로 불러온다.
- 결측치(NA)가 많은 컬럼을 파악하고, "결측치 전략"을 연습한다.
- 숫자형/범주형 컬럼을 분리하고, 간단한 피처 엔지니어링을 경험한다.

난이도
- Pandas 초급 (하지만 한 번 해두면 실전에서 정말 많이 씀)

데이터
# Kaggle 링크(데이터 받기): https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/data
# (대회 페이지)         : https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques

준비
- train.csv, test.csv 를 이 파일과 같은 폴더(또는 원하는 경로)에 다운로드해 두세요.

핵심 포인트
- 회귀 문제에서는 보통 train에만 정답(타깃: SalePrice)이 있고 test에는 없음
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd  # type: ignore[import-not-found]


def main() -> None:
    here = Path(__file__).resolve().parent
    data_dir = here  # 필요 시 수정

    train_path = data_dir / "train.csv"
    test_path = data_dir / "test.csv"

    # TODO 1) 데이터 로드 후 기본 확인
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)

    print("train.shape:", train.shape)
    print("test.shape :", test.shape)
    print(train[["Id", "SalePrice"]].head())

    # TODO 2) 타깃(SalePrice) 요약 통계
    # - describe() 출력
    # - (선택) SalePrice가 큰 상위 10개 집의 일부 컬럼만 출력해 보기
    # print(train["SalePrice"].describe())

    # TODO 3) 결측치(NA) 분석
    # - 결측치 개수/비율을 계산해서 상위 15개 컬럼 출력
    # 힌트:
    #   na_cnt = train.isna().sum()
    #   na_ratio = (na_cnt / len(train)).sort_values(ascending=False)
    #   na_table = pd.DataFrame({"na_count": na_cnt, "na_ratio": na_ratio}).sort_values("na_ratio", ascending=False).head(15)
    #   print(na_table)

    # TODO 4) 수치형/범주형 컬럼 나누기
    # - train에서 SalePrice 제외하고, numeric / categorical 컬럼 리스트 만들기
    # 힌트: select_dtypes(include="number")
    # features = train.drop(columns=["SalePrice"])
    # numeric_cols = ...
    # categorical_cols = ...
    # print(len(numeric_cols), len(categorical_cols))

    # TODO 5) 결측치 채우기(가장 단순한 전략)
    # - numeric은 중앙값(median)으로 채우기
    # - categorical은 최빈값(mode) 또는 "Unknown"으로 채우기
    # 힌트(선택):
    # - train_filled = train.copy()
    # - test_filled = test.copy()
    # - for col in numeric_cols: ...
    # - for col in categorical_cols: ...

    # TODO 6) One-hot encoding(범주형 → 숫자) 연습
    # - get_dummies로 train/test를 같은 컬럼 공간으로 맞추기
    # 힌트(선택):
    #   all_data = pd.concat([train_filled.drop(columns=["SalePrice"]), test_filled], axis=0, ignore_index=True)
    #   all_encoded = pd.get_dummies(all_data, drop_first=False)
    #   X_train = all_encoded.iloc[:len(train_filled)]
    #   X_test  = all_encoded.iloc[len(train_filled):]
    #   y_train = train_filled["SalePrice"]
    #   print(X_train.shape, X_test.shape, y_train.shape)

    # TODO 7) (선택) 가장 단순한 베이스라인 예측 만들기
    # - 규칙: train의 SalePrice 평균을 모든 test에 예측(완전 베이스라인)
    # - 제출 형식(Id, SalePrice)으로 저장해보기
    # 힌트(선택):
    #   baseline_pred = pd.Series(y_train.mean(), index=test["Id"])
    #   submission = pd.DataFrame({"Id": test["Id"], "SalePrice": baseline_pred.values})
    #   out_dir = here / "result"
    #   os.makedirs(out_dir, exist_ok=True)
    #   submission.to_csv(out_dir / "submission_baseline_mean.csv", index=False)

    print("\nTODO들이 남아있습니다. 위 TODO 블록을 직접 채워서 실행해 보세요.")


if __name__ == "__main__":
    main()
