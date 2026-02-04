# TODO: 아래 모르는 Library 내용 찾아서 정리.
from __future__ import annotations 

import pandas as pd 

import re
from dataclasses import dataclass
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"

@dataclass(frozen=True)
class OverallSidoDaily:
    daily: pd.DataFrame  # columns: date + regions (daily counts)
    cumulative_row: pd.Series  # cumulative snapshot row (single row)

def _pick_file_by_sheets(xlsx_files: list[Path], must_have_sheets: str[str]) -> Path:
  for f in xlsx_files:
    sheets = set(pd.ExcelFile(f).sheet_names)
    if must_have_sheets.issubset(sheets):
      return f
  raise FileNotFoundError(f"Cannot find xlsx having sheets: {sorted(must_have_sheets)}")


# xlsx_files = sorted(DATA_DIR.glob("*.xlsx"))
# if not xlsx_files:
#     raise FileNotFoundError(f"No xlsx files found under {DATA_DIR}")


def _make_b_region_daily_timeseries(cases: OverallSidoDaily, deaths: OverallSidoDaily) -> pd.DataFrame:
    cases_long = cases.daily.melt(id_vars=["date"], var_name="region", value_name="new_cases")
    deaths_long = deaths.daily.melt(id_vars=["date"], var_name="region", value_name="new_deaths")
    out = cases_long.merge(deaths_long, on=["date", "region"], how="inner")
    return out.sort_values(["date", "region"]).reset_index(drop=True)

def _load_overall_sido_daily(file: Path, sheet_name: str) -> OverallSidoDaily:
    """
    From: '코로나19 확진자 발생현황(전수감시)' xlsx
    Sheet format (header=None):
      row 4: header (일자, 계(명), 서울, ... , 검역)
      row 5: cumulative row labeled '누적(명)'
      row 6+: daily rows (datetime + numbers / '-')
    """
    raw = pd.read_excel(file, sheet_name=sheet_name, header=None)

    header_row_idx = 4
    cumulative_row_idx = 5
    data_start_idx = 6

    header = raw.iloc[header_row_idx].tolist()
    df = raw.iloc[data_start_idx:].copy()
    df.columns = header

    date_col = header[0]
    df = df[df[date_col].notna()].copy()

    # Convert date
    df[date_col] = pd.to_datetime(df[date_col])

    # Convert numbers ('-' -> 0)
    for c in df.columns[1:]:
        df[c] = (
            df[c]
            .replace("-", 0)
            .replace("－", 0)
            .pipe(pd.to_numeric, errors="coerce")
            .fillna(0)
            .astype(int)
        )

    cum = raw.iloc[cumulative_row_idx].copy()
    cum.index = header
    # First column is label ('누적(명)'); remaining columns are cumulative counts
    for c in header[1:]:
        v = cum[c]
        if pd.isna(v) or v in ("-", "－"):
            cum[c] = 0
        else:
            cum[c] = int(v)

    df = df.rename(columns={date_col: "date"})
    cum = cum.rename(index={date_col: "date_label"})

    return OverallSidoDaily(daily=df, cumulative_row=cum)


# overall_file = _pick_file_by_sheets(xlsx_files, {"시도별 발생(17개시도+검역)"})
# raw = pd.read_excel(overall_file, sheet_name="시도별 발생(17개시도+검역)", header=None)

# overall_cases = _load_overall_sido_daily(overall_file, "시도별 발생(17개시도+검역)")
# overall_deaths = _load_overall_sido_daily(overall_file, "시도별 사망(17개시도+검역) ")


# b_ts = _make_b_region_daily_timeseries(overall_cases, overall_deaths)
# print(b_ts.head(10))


def _extract_year(v) -> int | None:
  if pd.isna(v):
      return None
  s = str(v).strip()
  # 정규표현식 수정: 연도(예: 2020년, 2021년 등)에 매칭되도록 함.
  # 기존 정규식은 이중 백슬래시(\\)라 실제 백슬래시와 일치하게 되어 있었음.
  # 파이썬 raw string에서 정규식은 단일 백슬래시(r"(20\d{2})\s*년")를 사용해야 정상 동작.
  m = re.search(r"(20\d{2})\s*년", s)
  if not m:
      return None
  return int(m.group(1))


def _extract_month(v) -> int | None:
  if pd.isna(v):
      return None
  s = str(v).strip()
  m = re.search(r"(\d{1,2})\s*월", s)
  if not m:
      return None
  month = int(m.group(1))
  if 1 <= month <= 12:
      return month
  return None




def _load_sigungu_monthly_long(file: Path, sheet_name: str, value_name: str) -> pd.DataFrame:
  """
  From: '시군구별 월별 확진자 및 사망 발생 현황' xlsx (확진자/사망자 sheets)

  Layout (header=None):
    row 6: year group labels (2020년/2021년/2022년/2023년) across columns
    row 7: month labels (전체, 1월..., 2월..., ...)
    row 8+: data rows: [시도명, 시군구, ... month values ...]
  """
  raw = pd.read_excel(file, sheet_name=sheet_name, header=None)
  # 시트 내에서 '년'이 포함된 첫 번째 row를 year_row로 동적으로 찾는다.
  year_row_idx = next(
      (i for i, row in enumerate(raw.values) if any(isinstance(cell, str) and "년" in str(cell) for cell in row)), 
      None
  )
  if year_row_idx is None:
      raise ValueError("시트에서 연도(년)가 포함된 행을 찾을 수 없습니다.")
  print(f"year_row_idx: {year_row_idx}")
  year_row = raw.iloc[year_row_idx].tolist()
  month_row = raw.iloc[7].tolist()
  # Forward fill year labels across columns
  years: list[int | None] = [None] * len(year_row)
  current_year: int | None = None
  for i, y in enumerate(year_row):
      yi = _extract_year(y)
      if yi is not None:
          current_year = yi
      years[i] = current_year
  col_to_date: dict[int, pd.Timestamp] = {}
  for i, (y, mlabel) in enumerate(zip(years, month_row)):
      if y is None:
          continue
      month = _extract_month(mlabel)
      if month is None:
          continue
      col_to_date[i] = pd.Timestamp(year=y, month=month, day=1)
  data = raw.iloc[8:].copy()
  data = data[data[0].notna()].copy()
  data = data.rename(columns={0: "sido", 1: "sigungu"})

  keep_cols = ["sido", "sigungu"] + sorted(col_to_date.keys())
  data = data[keep_cols]
  data = data.replace("-", 0).replace("－", 0)
  for c in sorted(col_to_date.keys()):
      data[c] = pd.to_numeric(data[c], errors="coerce").fillna(0).astype(int)

  long = data.melt(id_vars=["sido", "sigungu"], var_name="col_idx", value_name=value_name)
  long["date"] = long["col_idx"].map(col_to_date)
  long = long.drop(columns=["col_idx"]).dropna(subset=["date"])
  return long.sort_values(["date", "sido", "sigungu"]).reset_index(drop=True)



# monthly_file = _pick_file_by_sheets(xlsx_files, {"확진자", "사망자"})
# b_sigungu_cases = _load_sigungu_monthly_long(monthly_file, "확진자", "monthly_cases")
# b_sigungu_deaths = _load_sigungu_monthly_long(monthly_file, "사망자", "monthly_deaths")

