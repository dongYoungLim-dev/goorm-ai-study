# 팀 미션: 대한민국 코로나19 대시보드 (데이터 정제)

이 폴더는 `data/`에 있는 원천 엑셀을 읽어, 팀원들이 바로 Plotly/Streamlit에서 사용할 수 있는 CSV를 생성합니다.

## 설치 (가상환경)

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/pip install -r requirements.txt
```

> 만약 macOS에서 `SSLError(SSLCertVerificationError('OSStatus -26276'))`로 설치가 막히면 아래처럼 설치하세요.

```bash
.venv/bin/pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org -r requirements.txt
```

## 실행

```bash
.venv/bin/python make_csv.py
```

실행하면 `output/` 폴더에 아래 CSV들이 생성됩니다.

## 생성 CSV (팀별)

### A팀: 국내 확진자/사망자 추이 (라인 차트)

- `output/a_national_trend_daily.csv`
  - 컬럼: `date`, `new_cases`, `new_deaths`, `cum_cases`, `cum_deaths`

### B팀: 지역별 확진 현황 (지도 그래프 또는 막대 그래프)

- `output/b_region_latest.csv`
  - “시도별 누적” 스냅샷(검역 포함)을 제공합니다.
  - 컬럼: `as_of_date`, `region`, `cum_cases`, `cum_deaths`

추가로(원하면 활용):

- `output/b_region_daily_timeseries.csv`
  - 컬럼: `date`, `region`, `new_cases`, `new_deaths`
- `output/b_sigungu_monthly_cases.csv`
- `output/b_sigungu_monthly_deaths.csv`
  - “시군구별 월별” 원천에서 월 단위 long-format으로 변환한 데이터입니다.

### C팀: 백신 접종률 vs 중증화율 상관관계 (산점도)

- `output/c_vax_vs_fatality_proxy.csv`
  - **주의**: 현재 제공된 원천 엑셀에는 ‘위중증(중환자)’ 지표가 없어, 대체 지표로 **사망률(치명률) 기반 proxy**를 생성합니다.
  - 컬럼: `date`, `vax2_rate`, `vax3_rate`, `fatality_rate_7d`

