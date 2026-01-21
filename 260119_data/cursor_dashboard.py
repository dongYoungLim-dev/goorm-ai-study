from pathlib import Path
from typing import Dict, Tuple

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="사내 인사 및 마케팅 현황 통합 모니터링",
    page_icon="📊",
    layout="wide",
)


def _data_dir() -> Path:
    return Path(__file__).resolve().parent / "data"


@st.cache_data(show_spinner=False)
def load_hr_data() -> pd.DataFrame:
    path = _data_dir() / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
    df = pd.read_csv(path)
    df["AttritionFlag"] = df["Attrition"].str.strip().str.lower() == "yes"
    return df


@st.cache_data(show_spinner=False)
def load_marketing_data() -> pd.DataFrame:
    path = _data_dir() / "marketing_campaign_dataset.csv"
    df = pd.read_csv(path, parse_dates=["Date"])
    # 정규화: 통화/숫자 문자열을 수치로 변환
    df["Acquisition_Cost"] = (
        df["Acquisition_Cost"]
        .astype(str)
        .str.replace(r"[^\d\.]", "", regex=True)
        .astype(float)
    )
    df["ROI"] = df["ROI"].astype(float)
    df["Conversion_Rate"] = df["Conversion_Rate"].astype(float)
    # ROL: ROI 대비 획득비용 효율 지표 (단순 비율)
    df["ROL"] = df["ROI"] / df["Acquisition_Cost"].replace(0, pd.NA)
    return df


def render_sidebar_filters(
    hr_df: pd.DataFrame, mkt_df: pd.DataFrame
) -> Tuple[Dict, Dict]:
    st.sidebar.title("사내 인사 및 마케팅 현황 통합 모니터링")
    st.sidebar.markdown("---")

    st.sidebar.subheader("HR 필터")
    dept_options = sorted(hr_df["Department"].dropna().unique())
    sel_dept = st.sidebar.multiselect("부서 선택", dept_options, default=dept_options)
    attrition_filter = st.sidebar.multiselect(
        "재직 상태",
        options=["재직", "퇴사"],
        default=["재직", "퇴사"],
    )

    st.sidebar.subheader("마케팅 필터")
    channel_options = sorted(mkt_df["Channel_Used"].dropna().unique())
    sel_channel = st.sidebar.multiselect(
        "채널 선택", channel_options, default=channel_options
    )
    min_date, max_date = mkt_df["Date"].min(), mkt_df["Date"].max()
    sel_date = st.sidebar.date_input(
        "기간 선택", value=(min_date, max_date), min_value=min_date, max_value=max_date
    )

    hr_filters = {
        "departments": sel_dept,
        "attrition": attrition_filter,
    }
    mkt_filters = {
        "channels": sel_channel,
        "date_range": sel_date,
    }
    return hr_filters, mkt_filters


def filter_hr_data(df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
    filtered = df[df["Department"].isin(filters["departments"])]
    if "재직" not in filters["attrition"]:
        filtered = filtered[filtered["AttritionFlag"]]
    elif "퇴사" not in filters["attrition"]:
        filtered = filtered[~filtered["AttritionFlag"]]
    return filtered


def filter_marketing_data(df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
    filtered = df[df["Channel_Used"].isin(filters["channels"])]
    if isinstance(filters["date_range"], tuple) and len(filters["date_range"]) == 2:
        start, end = filters["date_range"]
        filtered = filtered[(filtered["Date"] >= pd.to_datetime(start)) & (filtered["Date"] <= pd.to_datetime(end))]
    return filtered


def render_hr_tab(hr_df: pd.DataFrame):
    st.header("HR 대시보드")
    col1, col2 = st.columns(2)

    attrition_rate = (hr_df["AttritionFlag"].mean() * 100) if not hr_df.empty else 0
    total_employees = len(hr_df)
    col1.metric("퇴사율(%)", f"{attrition_rate:.1f}%")
    col2.metric("인원 수", f"{total_employees:,}")

    st.markdown("#### 부서별 현황")
    dept_group = (
        hr_df.groupby("Department")
        .agg(
            인원수=("AttritionFlag", "size"),
            퇴사율=("AttritionFlag", "mean"),
        )
        .reset_index()
    )
    bar_fig = px.bar(
        dept_group,
        x="Department",
        y="인원수",
        color="퇴사율",
        color_continuous_scale="Reds",
        title="부서별 인원 수 및 퇴사율",
    )
    st.plotly_chart(bar_fig, use_container_width=True)

    st.markdown("#### 부서별 소득 분포 (퇴사 여부)")
    if not hr_df.empty:
        box_fig = px.box(
            hr_df,
            x="Department",
            y="MonthlyIncome",
            color=hr_df["AttritionFlag"].map({True: "퇴사", False: "재직"}),
            points="outliers",
            title="부서별 월소득 vs 퇴사 여부",
        )
        st.plotly_chart(box_fig, use_container_width=True)
    else:
        st.info("선택된 조건에 맞는 HR 데이터가 없습니다.")


def render_marketing_tab(mkt_df: pd.DataFrame):
    st.header("마케팅 대시보드")
    col1, col2 = st.columns(2)

    avg_roi = mkt_df["ROI"].mean() if not mkt_df.empty else 0
    avg_rol = mkt_df["ROL"].mean() if not mkt_df.empty else 0
    col1.metric("평균 ROI", f"{avg_roi:.2f}")
    col2.metric("평균 ROL(ROI/Cost)", f"{avg_rol:.4f}")

    st.markdown("#### 채널별 전환율")
    conv_group = (
        mkt_df.groupby("Channel_Used")
        .agg(전환율=("Conversion_Rate", "mean"))
        .reset_index()
    )
    conv_fig = px.bar(
        conv_group,
        x="Channel_Used",
        y="전환율",
        color="전환율",
        color_continuous_scale="Blues",
        title="채널별 평균 전환율",
    )
    st.plotly_chart(conv_fig, use_container_width=True)

    st.markdown("#### 예산 효율성 (비용 vs ROI)")
    if not mkt_df.empty:
        scatter_fig = px.scatter(
            mkt_df,
            x="Acquisition_Cost",
            y="ROI",
            color="Channel_Used",
            size="Impressions",
            hover_data=["Campaign_ID", "Company", "Conversion_Rate"],
            title="캠페인 비용 대비 ROI",
        )
        st.plotly_chart(scatter_fig, use_container_width=True)
    else:
        st.info("선택된 조건에 맞는 마케팅 데이터가 없습니다.")


def main():
    hr_df = load_hr_data()
    mkt_df = load_marketing_data()

    hr_filters, mkt_filters = render_sidebar_filters(hr_df, mkt_df)
    filtered_hr = filter_hr_data(hr_df, hr_filters)
    filtered_mkt = filter_marketing_data(mkt_df, mkt_filters)

    hr_tab, marketing_tab = st.tabs(["HR 대시보드", "마케팅 대시보드"])
    with hr_tab:
        render_hr_tab(filtered_hr)
    with marketing_tab:
        render_marketing_tab(filtered_mkt)


if __name__ == "__main__":
    main()
