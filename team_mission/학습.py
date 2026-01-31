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


xlsx_files = sorted(DATA_DIR.glob("*.xlsx"))
if not xlsx_files:
    raise FileNotFoundError(f"No xlsx files found under {DATA_DIR}")


def _make_b_region_daily_timeseries(cases: OverallSidoDaily, deaths: OverallSidoDaily) -> pd.DataFrame:
    cases_long = cases.daily.melt(id_vars=["date"], var_name="region", value_name="new_cases")
    deaths_long = deaths.daily.melt(id_vars=["date"], var_name="region", value_name="new_deaths")
    print(cases_long.head(200))
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


overall_file = _pick_file_by_sheets(xlsx_files, {"시도별 발생(17개시도+검역)"})
raw = pd.read_excel(overall_file, sheet_name="시도별 발생(17개시도+검역)", header=None)

overall_cases = _load_overall_sido_daily(overall_file, "시도별 발생(17개시도+검역)")
overall_deaths = _load_overall_sido_daily(overall_file, "시도별 사망(17개시도+검역) ")


b_ts = _make_b_region_daily_timeseries(overall_cases, overall_deaths)
# print(b_ts.head(10))