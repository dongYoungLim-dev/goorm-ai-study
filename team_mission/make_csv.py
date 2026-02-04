from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"


@dataclass(frozen=True)
class OverallSidoDaily:
    daily: pd.DataFrame  # columns: date + regions (daily counts)
    cumulative_row: pd.Series  # cumulative snapshot row (single row)


def _pick_file_by_sheets(xlsx_files: list[Path], must_have_sheets: set[str]) -> Path:
    for f in xlsx_files:
        sheets = set(pd.ExcelFile(f).sheet_names)
        if must_have_sheets.issubset(sheets):
            return f
    raise FileNotFoundError(f"Cannot find xlsx having sheets: {sorted(must_have_sheets)}")


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


def _make_a_national_trend(cases: OverallSidoDaily, deaths: OverallSidoDaily) -> pd.DataFrame:
    df = cases.daily[["date", "계(명)"]].merge(
        deaths.daily[["date", "계(명)"]], on="date", how="inner", suffixes=("_cases", "_deaths")
    )
    df = df.rename(columns={"계(명)_cases": "new_cases", "계(명)_deaths": "new_deaths"})
    df = df.sort_values("date").reset_index(drop=True)
    df["cum_cases"] = df["new_cases"].cumsum()
    df["cum_deaths"] = df["new_deaths"].cumsum()
    return df


def _make_b_region_latest(cases: OverallSidoDaily, deaths: OverallSidoDaily) -> pd.DataFrame:
    as_of_date = cases.daily["date"].max().date().isoformat()

    regions = [c for c in cases.daily.columns if c not in ("date",)]
    # Drop the national total column name from regions list (we still can include it as a row)
    # '계(명)' exists in this dataset, but for map/bar teams may want '전국' too, so keep.
    rows = []
    for r in regions:
        if r == "date":
            continue
        rows.append(
            {
                "as_of_date": as_of_date,
                "region": r,
                "cum_cases": int(cases.cumulative_row.get(r, 0)),
                "cum_deaths": int(deaths.cumulative_row.get(r, 0)),
            }
        )
    return pd.DataFrame(rows).sort_values(["cum_cases"], ascending=False).reset_index(drop=True)


def _make_b_region_daily_timeseries(cases: OverallSidoDaily, deaths: OverallSidoDaily) -> pd.DataFrame:
    # long format: date, region, new_cases/new_deaths
    cases_long = cases.daily.melt(id_vars=["date"], var_name="region", value_name="new_cases")
    deaths_long = deaths.daily.melt(id_vars=["date"], var_name="region", value_name="new_deaths")
    out = cases_long.merge(deaths_long, on=["date", "region"], how="inner")
    return out.sort_values(["date", "region"]).reset_index(drop=True)


def _extract_year(v) -> int | None:
    if pd.isna(v):
        return None
    s = str(v).strip()
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
    year_row = raw.iloc[year_row_idx].tolist()
    month_row = raw.iloc[year_row_idx + 1].tolist()

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

    data = raw.iloc[year_row_idx + 2:].copy()
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


def _parse_vax_region_sheet(file: Path, region_sheet: str) -> pd.DataFrame:
    """
    From: 예방접종 통계 현황 (지역별 시트)

    Layout (header=None):
      row 1: population per age group (repeated across dose blocks)
      row 2: dose labels (1차/2차/3차) across columns
      row 3: metric labels (건수/접종률) across columns
      row 4: age group labels (65세이상/12-64세/...)
      row 5+: data rows (date yyyymmdd, daily counts, rates)
    """
    raw = pd.read_excel(file, sheet_name=region_sheet, header=None)

    pop_row = raw.iloc[1]
    dose_row = raw.iloc[2]
    metric_row = raw.iloc[3]
    age_row = raw.iloc[4]

    # Forward fill dose/metric across columns
    doses = [] # 차수 데이터
    metrics = [] # 건수/접종률 데이터
    cur_dose = None
    cur_metric = None
    for d, m in zip(dose_row.tolist(), metric_row.tolist()):
        if not pd.isna(d):
            cur_dose = str(d).strip()
        if not pd.isna(m):
            cur_metric = str(m).strip()
        doses.append(cur_dose)
        metrics.append(cur_metric)

    # Identify date column: in sample it's column 1
    date_col_idx = 1

    # Build column keys for count columns
    count_cols: dict[str, list[int]] = {"1차": [], "2차": [], "3차": []}
    age_cols_for_pop: list[int] = []
    for i in range(len(doses)):
        if i == date_col_idx: 
            continue
        dose = doses[i] # 차수 데이터
        metric = metrics[i] # 건수/접종률 데이터
        age = age_row.iloc[i] # 연령 데이터
        if pd.isna(age): # 연령 데이터가 nan이면 무시
            continue
        age_s = str(age).strip() # 연령 데이터를 문자열로 변환하고 양쪽 공백 제거
        if dose in count_cols and metric == "건수":
            count_cols[dose].append(i) #
            # Use the first dose block's count columns as population reference
            if dose == "1차":
                age_cols_for_pop.append(i)


    # population total (sum of age groups) from row 1
    pop_total = pd.to_numeric(pop_row.iloc[age_cols_for_pop], errors="coerce").fillna(0).sum()
    pop_total = int(pop_total)
    
    data = raw.iloc[5:].copy()
    data = data[data[date_col_idx].notna()].copy()
    data = data.rename(columns={date_col_idx: "date_raw"})

    # date parsing: yyyymmdd as float/int
    data["date"] = (
        data["date_raw"]
        .astype(str)
        .str.replace(r"\.0$", "", regex=True)
        .pipe(pd.to_datetime, format="%Y%m%d", errors="coerce")
    )
    data = data.dropna(subset=["date"]).copy()

    out = pd.DataFrame({"date": data["date"]})
    out["region"] = region_sheet
    out["pop_total"] = pop_total

    for dose, idxs in count_cols.items():
        if not idxs:
            continue
        daily = data[idxs].replace("-", 0).replace("－", 0)
        daily = daily.apply(pd.to_numeric, errors="coerce").fillna(0).astype(int)
        out[f"{dose}_daily"] = daily.sum(axis=1)

    return out.sort_values("date").reset_index(drop=True)


def _make_c_vax_vs_fatality_proxy(
    vax_file: Path,
    cases: OverallSidoDaily,
    deaths: OverallSidoDaily,
) -> pd.DataFrame:
    # Vaccination: sum across all region sheets (exclude '기준')
    sheets = pd.ExcelFile(vax_file).sheet_names
    region_sheets = [s for s in sheets if s != "기준"]

    vax_parts = []
    for s in region_sheets:
        vax_parts.append(_parse_vax_region_sheet(vax_file, s))
    vax = pd.concat(vax_parts, ignore_index=True)

    # National aggregation by date
    agg = vax.groupby("date", as_index=False).agg(
        pop_total=("pop_total", "sum"),
        dose1=("1차_daily", "sum"),
        dose2=("2차_daily", "sum"),
        dose3=("3차_daily", "sum"),
    )
    agg = agg.sort_values("date").reset_index(drop=True)
    agg["dose1_cum"] = agg["dose1"].cumsum()
    agg["dose2_cum"] = agg["dose2"].cumsum()
    agg["dose3_cum"] = agg["dose3"].cumsum()
    agg["vax1_rate"] = (agg["dose1_cum"] / agg["pop_total"]) * 100
    agg["vax2_rate"] = (agg["dose2_cum"] / agg["pop_total"]) * 100
    agg["vax3_rate"] = (agg["dose3_cum"] / agg["pop_total"]) * 100

    # Cases/deaths (national)
    cd = cases.daily[["date", "계(명)"]].merge(
        deaths.daily[["date", "계(명)"]], on="date", how="inner", suffixes=("_cases", "_deaths")
    )
    cd = cd.rename(columns={"계(명)_cases": "new_cases", "계(명)_deaths": "new_deaths"}).sort_values("date")
    cd["cases_7d"] = cd["new_cases"].rolling(7).sum()
    cd["deaths_7d"] = cd["new_deaths"].rolling(7).sum()
    cd["fatality_rate_7d"] = (cd["deaths_7d"] / cd["cases_7d"]) * 100
    # 1차 누적 값을 계산해서 agg에 추가합니다.

    out = agg[["date","vax1_rate", "vax2_rate", "vax3_rate"]].merge(
        cd[["date", "fatality_rate_7d"]], on="date", how="inner"
    )

    out = out.dropna().reset_index(drop=True)
    return out


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    xlsx_files = sorted(DATA_DIR.glob("*.xlsx"))
    if not xlsx_files:
        raise FileNotFoundError(f"No xlsx files found under {DATA_DIR}")

    monthly_file = _pick_file_by_sheets(xlsx_files, {"확진자", "사망자"})
    vax_file = _pick_file_by_sheets(xlsx_files, {"기준", "서울"})
    overall_file = _pick_file_by_sheets(xlsx_files, {"시도별 발생(17개시도+검역)"})

    overall_cases = _load_overall_sido_daily(overall_file, "시도별 발생(17개시도+검역)")
    overall_deaths = _load_overall_sido_daily(overall_file, "시도별 사망(17개시도+검역) ")

    # A : 날짜병 발생/사망자 count 리스트
    a = _make_a_national_trend(overall_cases, overall_deaths)
    a.to_csv(OUTPUT_DIR / "a_national_trend_daily.csv", index=False, encoding="utf-8-sig")

    # B
    # 
    b_latest = _make_b_region_latest(overall_cases, overall_deaths)
    b_latest.to_csv(OUTPUT_DIR / "b_region_latest.csv", index=False, encoding="utf-8-sig")
    # b_ts : 날짜별 지역 발생/사망자 count( 날짜별 계(명) 포함)
    b_ts = _make_b_region_daily_timeseries(overall_cases, overall_deaths)
    b_ts.to_csv(OUTPUT_DIR / "b_region_daily_timeseries.csv", index=False, encoding="utf-8-sig")
    
    # 아래 두개는 확인 필요
    b_sigungu_cases = _load_sigungu_monthly_long(monthly_file, "확진자", "monthly_cases")
    b_sigungu_cases.to_csv(OUTPUT_DIR / "b_sigungu_monthly_cases.csv", index=False, encoding="utf-8-sig")

    b_sigungu_deaths = _load_sigungu_monthly_long(monthly_file, "사망자", "monthly_deaths")
    b_sigungu_deaths.to_csv(OUTPUT_DIR / "b_sigungu_monthly_deaths.csv", index=False, encoding="utf-8-sig")

    # C (proxy: fatality rate)
    c = _make_c_vax_vs_fatality_proxy(vax_file, overall_cases, overall_deaths)
    c.to_csv(OUTPUT_DIR / "c_vax_vs_fatality_proxy.csv", index=False, encoding="utf-8-sig")

    print("Done. CSVs written to:", OUTPUT_DIR)


if __name__ == "__main__":
    main()

