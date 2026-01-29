"""
Problem 03) Netflix Titles - 문자열/날짜/리스트 컬럼 다루기 (Pandas 실전 감각)

목표
- 문자열 컬럼에서 전처리(strip, replace, contains)를 해본다.
- 날짜 컬럼을 to_datetime으로 변환하고 year/month 파생변수를 만든다.
- 쉼표로 묶인 리스트 형태 컬럼을 split + explode로 펼쳐서 집계를 해본다.

난이도
- Pandas 초급~중급 입문(실전에서 많이 쓰는 패턴)

데이터
# Kaggle 링크(데이터 받기): https://www.kaggle.com/datasets/shivamb/netflix-shows

준비
- 보통 파일명이 `netflix_titles.csv` 입니다. 이 파일과 같은 폴더에 두세요.
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd  # type: ignore[import-not-found]


def _split_list_cell(value: object) -> list[str]:
    """
    쉼표로 구분된 문자열을 리스트로 변환.
    - 결측/비문자 값은 빈 리스트 반환
    - 각 토큰은 strip 처리
    """
    if not isinstance(value, str):
        return []
    items = [x.strip() for x in value.split(",")]
    return [x for x in items if x]


def main() -> None:
    here = Path(__file__).resolve().parent
    data_dir = here  # 필요 시 수정

    csv_path = data_dir / "netflix_titles.csv"

    # TODO 1) 데이터 로드 & 기본 확인
    df = pd.read_csv(csv_path)
    print("shape:", df.shape)
    print(df.head(3))
    print(df.info())

    # TODO 2) 결측치 확인(상위 10개 컬럼)
    # - 결측치 개수를 구하고, 많은 순서대로 상위 10개를 출력하세요.
    # 힌트: df.isna().sum().sort_values(ascending=False)
    # na = ...
    # print(na.head(10))

    # TODO 3) 날짜 처리: date_added -> datetime
    # - df를 복사해서 df2를 만들고,
    # - date_added를 datetime으로 변환(errors='coerce')
    # - year_added, month_added 파생변수 만들기
    # - year_added 별 컨텐츠 추가 수(count) 상위 10개 출력
    #
    # df2 = df.copy()
    # df2["date_added_dt"] = ...
    # df2["year_added"] = ...
    # df2["month_added"] = ...
    # print(df2["year_added"].value_counts(dropna=True).head(10))

    # TODO 4) 문자열 필터링/비율 계산 연습
    # - type 컬럼이 "Movie" / "TV Show" 로 구성되어 있음
    # - 각 비율을 구해서 출력하세요.
    # 힌트: value_counts(normalize=True)
    # type_ratio = ...
    # print(type_ratio)

    # TODO 5) country 컬럼 정리 후 상위 국가 분석 (explode)
    # - country는 "United States, India, ..." 형태일 수 있음
    # - split + explode로 국가를 펼친 뒤 상위 15개 국가를 출력하세요.
    # 힌트(선택):
    #   country_exploded = df2.assign(country_list=df2["country"].map(_split_list_cell)).explode("country_list", ignore_index=True)
    #   country_exploded = country_exploded[country_exploded["country_list"].notna()]
    #   country_exploded = country_exploded[country_exploded["country_list"] != ""]
    #   print(country_exploded["country_list"].value_counts().head(15))

    # TODO 6) 장르(listed_in) 분석 (explode 패턴 핵심)
    # - listed_in도 "Dramas, International Movies, ..." 형태
    # - 장르를 펼친 뒤 상위 20개 장르를 출력하세요.
    # 힌트(선택):
    #   genre_exploded = df2.assign(genre=df2["listed_in"].map(_split_list_cell)).explode("genre", ignore_index=True)
    #   genre_exploded = genre_exploded[genre_exploded["genre"].notna()]
    #   genre_exploded = genre_exploded[genre_exploded["genre"] != ""]
    #   print(genre_exploded["genre"].value_counts().head(20))

    # TODO 7) (선택) 감독(director) 결측치 처리/집계
    # - director 결측을 "Unknown"으로 채운 뒤, 작품 수 상위 10명을 출력하세요.
    # 힌트(선택):
    #   df2["director_filled"] = df2["director"].fillna("Unknown").astype(str).str.strip()
    #   print(df2["director_filled"].value_counts().head(10))

    # TODO 8) (선택) 분석 결과를 csv로 저장해보기
    # - country_exploded / genre_exploded가 준비되면 result 폴더에 저장해보세요.
    # 힌트(선택):
    #   out_dir = here / "result"
    #   os.makedirs(out_dir, exist_ok=True)
    #   country_exploded[["show_id", "title", "country_list"]].to_csv(out_dir / "netflix_country_exploded.csv", index=False)
    #   genre_exploded[["show_id", "title", "genre"]].to_csv(out_dir / "netflix_genre_exploded.csv", index=False)

    print("\nTODO들이 남아있습니다. 위 TODO 블록을 직접 채워서 실행해 보세요.")


if __name__ == "__main__":
    main()
