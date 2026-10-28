from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from modules.farmer_assistant import render_farmer_assistant
from modules.reports_explorer import render_reports_explorer


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="FarmWise Insights Haryana",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "data" / "haryana_crop_demo_data.csv"


# =====================================================
# PROFESSIONAL CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* Main application */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #0b1220 !important;
    color: #f1f5f9 !important;
}

/* Main content */
[data-testid="stMain"] > div {
    background-color: #0b1220 !important;
}

/* Sidebar */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background-color: #101a2b !important;
    color: #f1f5f9 !important;
}

/* All headings and normal text */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp p,
.stApp label,
.stApp li {
    color: #e2e8f0 !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #151f30 !important;
    border: 1px solid #334155 !important;
    border-radius: 14px !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #cbd5e1 !important;
}

[data-testid="stMetricValue"] {
    color: #4ade80 !important;
}

/* Containers and expanders */
[data-testid="stExpander"],
[data-testid="stExpander"] details {
    background-color: #151f30 !important;
    color: #f1f5f9 !important;
    border-color: #334155 !important;
}

/* Text inputs */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background-color: #151f30 !important;
    color: #f1f5f9 !important;
    border-color: #475569 !important;
}

/* Select boxes */
[data-baseweb="select"] > div {
    background-color: #151f30 !important;
    color: #f1f5f9 !important;
    border-color: #475569 !important;
}

/* Tables */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background-color: #151f30 !important;
    color: #f1f5f9 !important;
}

/* Tabs */
[data-testid="stTabs"] [role="tablist"] {
    background-color: #101a2b !important;
}

[data-testid="stTabs"] [role="tab"] {
    color: #e2e8f0 !important;
}

/* Buttons */
.stButton button,
.stDownloadButton button {
    background-color: #15803d !important;
    color: white !important;
    border-color: #22c55e !important;
}

/* Separators */
hr {
    border-color: #334155 !important;
}

</style>

""", unsafe_allow_html=True)


# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data(file_path):

    data = pd.read_csv(file_path)

    required_columns = [
        "Year",
        "District",
        "Crop",
        "Area_Hectares",
        "Yield_Tonnes_Per_Hectare",
        "Production_Tonnes",
        "Rainfall_mm",
        "Average_Temperature_C",
        "Indicative_Price_Rs_Per_Quintal"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns in dataset: {missing_columns}"
        )

    return data


if not DATA_FILE.exists():

    st.error(
        f"Dataset not found: {DATA_FILE}"
    )

    st.stop()


try:
    df = load_data(DATA_FILE)

except Exception as error:

    st.error(f"Unable to load dataset: {error}")

    st.stop()


if df.empty:

    st.warning("The dataset contains no records.")

    st.stop()


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

st.sidebar.markdown(
    """
    <h2 style="color:#14532d;">🌾 FarmWise</h2>
    <p style="color:#64748b;">
        Agricultural Intelligence Platform
    </p>
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Farmer Assistant",
        "Reports & Data Explorer"
    ],
    key="main_navigation"
)


# =====================================================
# OTHER MODULES
# =====================================================

if page == "Farmer Assistant":

    render_farmer_assistant(df)

    st.stop()


if page == "Reports & Data Explorer":

    render_reports_explorer(df)

    st.stop()


# =====================================================
# EXECUTIVE DASHBOARD
# =====================================================

st.markdown(
    """
    <div class="hero-banner">
        <h1>🌾 FarmWise Insights Haryana</h1>
        <p>
            Smart Agricultural Analytics Dashboard
        </p>
        <p>
            Explore crop production, district performance,
            agricultural yield, weather indicators and market trends.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.warning(
    "DEMO DATA ONLY — Figures are illustrative and "
    "must not be reported as official Haryana statistics."
)


# =====================================================
# FILTERS
# =====================================================

st.sidebar.markdown("---")

st.sidebar.markdown(
    "### 🌱 Dashboard Filters"
)

years = sorted(
    df["Year"].dropna().unique().tolist()
)

districts = sorted(
    df["District"].dropna().unique().tolist()
)

crops = sorted(
    df["Crop"].dropna().unique().tolist()
)


selected_years = st.sidebar.multiselect(
    "Select Year",
    options=years,
    default=years,
    key="dashboard_years"
)

selected_districts = st.sidebar.multiselect(
    "Select District",
    options=districts,
    default=districts,
    key="dashboard_districts"
)

selected_crops = st.sidebar.multiselect(
    "Select Crop",
    options=crops,
    default=crops,
    key="dashboard_crops"
)


filtered_df = df[
    df["Year"].isin(selected_years)
    & df["District"].isin(selected_districts)
    & df["Crop"].isin(selected_crops)
].copy()


if filtered_df.empty:

    st.info(
        "No records match your filters. "
        "Please select another year, district or crop."
    )

    st.stop()


# =====================================================
# CALCULATE METRICS
# =====================================================

total_production = filtered_df[
    "Production_Tonnes"
].sum()

total_area = filtered_df[
    "Area_Hectares"
].sum()

average_yield = filtered_df[
    "Yield_Tonnes_Per_Hectare"
].mean()

average_rainfall = filtered_df[
    "Rainfall_mm"
].mean()


crop_production = (
    filtered_df.groupby("Crop")["Production_Tonnes"]
    .sum()
    .sort_values(ascending=False)
)

district_production = (
    filtered_df.groupby("District")["Production_Tonnes"]
    .sum()
    .sort_values(ascending=False)
)


highest_crop = crop_production.index[0]

best_district = district_production.index[0]


# =====================================================
# KPI CARDS
# =====================================================

st.markdown("## 📊 Executive Overview")

st.caption(
    "Key performance indicators based on your selected filters."
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🌾 Total Production",
    f"{total_production:,.0f} tonnes"
)

col2.metric(
    "🌱 Cultivated Area",
    f"{total_area:,.0f} hectares"
)

col3.metric(
    "📈 Average Yield",
    f"{average_yield:.2f} tonnes/ha"
)

col4.metric(
    "🌧️ Average Rainfall",
    f"{average_rainfall:.1f} mm"
)


st.markdown("")


# =====================================================
# HIGHLIGHT CARDS
# =====================================================

st.markdown("## 🏆 Performance Highlights")

highlight1, highlight2 = st.columns(2)

with highlight1:

    st.markdown(
        f"""
        <div style="
          background:linear-gradient(120deg,#15803d,#166534); padding:24px; border-radius:16px; border-left:6px solid #22c55e; min-height:145px; "> 
        <h3 style="color:#0a0a0a; margin-top:0; font-weight:700;">🌾 Leading Crop</h3> 
        <h2 style="color:#0a0a0a; margin:8px 0; font-weight:800;">{highest_crop}</h2> 
        <p style="color:#0a0a0a; margin-bottom:0; font-weight:500;">Highest total production in the selected data.</p> 
        </div>

        """,
        unsafe_allow_html=True
    )

with highlight2:

    st.markdown(
        f"""
        <div style="
                      background:linear-gradient(120deg,#15803d,#166534); 
                      padding:24px; border-radius:16px; 
                      border-left:6px solid #22c55e; 
                      min-height:145px; ">
            <h3 style="color:#0a0a0a;">📍 Leading District</h3>
            <h2 style="color:#0a0a0a;">{best_district}</h2>
            <p>Highest total production in the selected data.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("")


# =====================================================
# COMMON PLOTLY SETTINGS
# =====================================================

def style_chart(fig, height=390):

    fig.update_layout(
        template="plotly_dark",
    paper_bgcolor="#0b1220",
    plot_bgcolor="#151f30",
    font=dict(
        family="Arial",
        size=13,
        color="#f8fafc"
    ),
    title_font=dict(
        color="#ffffff",
        size=20
    ),
    xaxis=dict(
        title_font=dict(color="#f8fafc", size=14),
        tickfont=dict(color="#e2e8f0", size=11),
        gridcolor="#334155"
    ),
    yaxis=dict(
        title_font=dict(color="#f8fafc", size=14),
        tickfont=dict(color="#e2e8f0", size=12),
        gridcolor="#334155"
    ),
    legend=dict(
        font=dict(color="#f8fafc")
        )
    )

    fig.update_xaxes(
        showgrid=False,
        automargin=True
    )

    fig.update_yaxes(
        gridcolor="#e5e7eb",
        zerolinecolor="#d1d5db",
        automargin=True
    )

    return fig


# =====================================================
# CROP ANALYSIS
# =====================================================

st.markdown("---")

st.markdown("## 🌾 Crop Production Analysis")

chart1, chart2 = st.columns(2)


with chart1:

    st.markdown("### Production by Crop")

    crop_chart = (
        filtered_df.groupby("Crop", as_index=False)
        ["Production_Tonnes"]
        .sum()
        .sort_values(
            "Production_Tonnes",
            ascending=True
        )
    )

    fig_crop = px.bar(
        crop_chart,
        x="Production_Tonnes",
        y="Crop",
        orientation="h",
        color="Production_Tonnes",
        color_continuous_scale=[
            "#bbf7d0",
            "#4ade80",
            "#15803d"
        ],
        labels={
            "Production_Tonnes": "Production (tonnes)",
            "Crop": "Crop"
        },
        title="Total Production by Crop",
        hover_data={
            "Production_Tonnes": ":,.2f"
        }
    )

    fig_crop.update_coloraxes(showscale=False)

    style_chart(fig_crop)

    st.plotly_chart(
        fig_crop,
        use_container_width=True
    )


with chart2:

    st.markdown("### Average Yield by Crop")

    yield_chart = (
        filtered_df.groupby("Crop", as_index=False)
        ["Yield_Tonnes_Per_Hectare"]
        .mean()
        .sort_values(
            "Yield_Tonnes_Per_Hectare",
            ascending=True
        )
    )

    fig_yield = px.bar(
        yield_chart,
        x="Yield_Tonnes_Per_Hectare",
        y="Crop",
        orientation="h",
        color="Yield_Tonnes_Per_Hectare",
        color_continuous_scale=[
            "#bfdbfe",
            "#60a5fa",
            "#1d4ed8"
        ],
        labels={
            "Yield_Tonnes_Per_Hectare": "Yield (tonnes/ha)",
            "Crop": "Crop"
        },
        title="Average Yield by Crop"
    )

    fig_yield.update_coloraxes(showscale=False)

    style_chart(fig_yield)

    st.plotly_chart(
        fig_yield,
        use_container_width=True
    )


# =====================================================
# DISTRICT PERFORMANCE
# =====================================================

st.markdown("---")

st.markdown("## 📍 District Performance")

district_chart = (
    filtered_df.groupby("District", as_index=False)
    ["Production_Tonnes"]
    .sum()
    .sort_values("Production_Tonnes", ascending=False)
)

fig_district = px.bar(
    district_chart,
    x="District",
    y="Production_Tonnes",
    color="Production_Tonnes",
    color_continuous_scale="Greens",
    title="Compare Total Production Across Districts",
    labels={
        "Production_Tonnes": "Production (tonnes)",
        "District": "District"
    },
    hover_data={
        "Production_Tonnes": ":,.2f"
    }
)

fig_district.update_xaxes(tickangle=-35)

style_chart(fig_district, height=440)

st.plotly_chart(
    fig_district,
    use_container_width=True
)


# =====================================================
# YEAR-WISE PRODUCTION TREND
# =====================================================

st.markdown("---")

st.markdown("## 📈 Agricultural Trends")

trend_col1, trend_col2 = st.columns(2)


with trend_col1:

    yearly_production = (
        filtered_df.groupby("Year", as_index=False)
        ["Production_Tonnes"]
        .sum()
        .sort_values("Year")
    )

    fig_trend = px.line(
        yearly_production,
        x="Year",
        y="Production_Tonnes",
        markers=True,
        title="Year-wise Production Trend",
        labels={
            "Year": "Year",
            "Production_Tonnes": "Production (tonnes)"
        }
    )

    fig_trend.update_traces(
        line=dict(color="#15803d", width=4),
        marker=dict(size=9)
    )

    style_chart(fig_trend)

    st.plotly_chart(
        fig_trend,
        use_container_width=True
    )


with trend_col2:

    area_chart = (
        filtered_df.groupby("Crop", as_index=False)
        ["Area_Hectares"]
        .sum()
        .sort_values("Area_Hectares", ascending=False)
    )

    fig_area = px.pie(
        area_chart,
        names="Crop",
        values="Area_Hectares",
        hole=0.55,
        title="Cultivated Area Distribution",
        color_discrete_sequence=px.colors.sequential.Greens
    )

    fig_area.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Area: %{value:,.0f} hectares<br>"
            "Share: %{percent}<extra></extra>"
        )
    )

    style_chart(fig_area)

    st.plotly_chart(
        fig_area,
        use_container_width=True
    )


# =====================================================
# WEATHER INSIGHTS
# =====================================================

st.markdown("---")

st.markdown("## 🌦️ Weather Insights")

weather_col1, weather_col2 = st.columns(2)


with weather_col1:

    rainfall_data = (
        filtered_df.groupby("Year", as_index=False)
        ["Rainfall_mm"]
        .mean()
        .sort_values("Year")
    )

    fig_rainfall = px.area(
        rainfall_data,
        x="Year",
        y="Rainfall_mm",
        title="Average Recorded Rainfall",
        labels={
            "Year": "Year",
            "Rainfall_mm": "Rainfall (mm)"
        }
    )

    fig_rainfall.update_traces(
        line_color="#0284c7",
        fillcolor="rgba(14,165,233,0.18)"
    )

    style_chart(fig_rainfall)

    st.plotly_chart(
        fig_rainfall,
        use_container_width=True
    )


with weather_col2:

    temperature_data = (
        filtered_df.groupby("Year", as_index=False)
        ["Average_Temperature_C"]
        .mean()
        .sort_values("Year")
    )

    fig_temperature = px.line(
        temperature_data,
        x="Year",
        y="Average_Temperature_C",
        markers=True,
        title="Average Recorded Temperature",
        labels={
            "Year": "Year",
            "Average_Temperature_C": "Temperature (°C)"
        }
    )

    fig_temperature.update_traces(
        line=dict(color="#ea580c", width=3),
        marker=dict(size=8)
    )

    style_chart(fig_temperature)

    st.plotly_chart(
        fig_temperature,
        use_container_width=True
    )


# =====================================================
# DATA-DRIVEN INSIGHTS
# =====================================================

st.markdown("---")

st.markdown("## 💡 Key Insights")

insight1, insight2, insight3 = st.columns(3)


with insight1:

    st.markdown("### 🌾 Crop Insight")

    st.write(
        f"**{highest_crop}** has the highest total "
        f"production in the currently selected records."
    )

    st.caption(
        "Based on the filtered dataset."
    )


with insight2:

    st.markdown("### 📍 District Insight")

    st.write(
        f"**{best_district}** leads in total recorded "
        f"production among the selected districts."
    )

    st.caption(
        "This does not necessarily mean it has the highest yield."
    )


with insight3:

    st.markdown("### 🌱 Yield Insight")

    best_yield_crop = (
        filtered_df.groupby("Crop")
        ["Yield_Tonnes_Per_Hectare"]
        .mean()
        .idxmax()
    )

    best_yield = (
        filtered_df.groupby("Crop")
        ["Yield_Tonnes_Per_Hectare"]
        .mean()
        .max()
    )

    st.write(
        f"**{best_yield_crop}** has the highest average "
        f"recorded yield at {best_yield:.2f} tonnes per hectare."
    )

    st.caption(
        "Yield and total production measure different things."
    )


# =====================================================
# DATA EXPLORER
# =====================================================

st.markdown("---")

with st.expander("🔎 Explore Agricultural Dataset"):

    st.write(
        f"Showing **{len(filtered_df):,} records** "
        "based on your selected filters."
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="⬇️ Download Filtered Dataset",
        data=csv_data,
        file_name="farmwise_filtered_data.csv",
        mime="text/csv"
    )


# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    """
    <div style="
    text-align:center;
    padding:18px;
    background:#2e7d32;
    border-radius:12px;
">
    <h4 style="color:#0a0a0a; margin-top:0; font-weight:700;">
        🌾 FarmWise Insights Haryana
    </h4>
    <p style="color:#0a0a0a; margin:8px 0; font-weight:500;">
        Agricultural Analytics | Data Visualization | Farmer Support
    </p>
    <p style="color:#0a0a0a; font-size:12px; margin-bottom:0; opacity:0.9; font-weight:500;">
        Educational demonstration project. Figures are not official agricultural statistics.
    </p>
</div>

    """,
    unsafe_allow_html=True
)