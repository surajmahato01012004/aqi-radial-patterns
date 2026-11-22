import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set page title and layout
st.set_page_config(
    page_title="AQI Radial Patterns & Trends",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f8fafc;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    file_path = "city_day.csv"
    if not os.path.exists(file_path):
        return None
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    return df

df = load_data()

if df is None:
    st.error("Error: `city_day.csv` not found in current directory!")
    st.stop()

# Header
st.markdown('<div class="main-title">Air Quality Index (AQI): Radial Patterns & Annual Trends</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Python Lab Project • Data Source: Kaggle (Air Quality Data in India 2015-2020)</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("⚙️ Controls & Filters")
available_cities = sorted(df['City'].unique())
default_index = available_cities.index("Delhi") if "Delhi" in available_cities else 0
selected_city = st.sidebar.selectbox("Select City", available_cities, index=default_index)

pollutant = st.sidebar.selectbox("Pollutant Metric", ["PM2.5", "PM10", "AQI"], index=0)

# Filter data
city_df = df[df['City'] == selected_city].dropna(subset=[pollutant]).copy()

if city_df.empty:
    st.warning(f"No valid data available for {selected_city} with metric {pollutant}.")
    st.stop()

# Calculations
yearly_avg = city_df.groupby('Year')[pollutant].mean().round(2)
overall_mean = city_df[pollutant].mean()
highest_year = yearly_avg.idxmax()
lowest_year = yearly_avg.idxmin()

# 2019 vs 2020 COVID change
change_covid = None
if 2019 in yearly_avg.index and 2020 in yearly_avg.index:
    val_19 = yearly_avg[2019]
    val_20 = yearly_avg[2020]
    pct = ((val_20 - val_19) / val_19) * 100
    change_covid = f"{pct:.1f}%"

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)
col1.metric(f"City", selected_city, f"{len(city_df)} days recorded")
col2.metric(f"Overall Avg {pollutant}", f"{overall_mean:.1f} µg/m³" if pollutant != "AQI" else f"{overall_mean:.1f}")
col3.metric("Peak Year", f"{highest_year} ({yearly_avg[highest_year]:.1f})", delta_color="inverse")
col4.metric("2020 Lockdown Effect", f"{yearly_avg.get(2020, 'N/A')}", delta=change_covid, delta_color="inverse" if change_covid else "off")

st.markdown("---")

# Tabs for Views
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 1. Annual Trend (Lab Requirement)", 
    "🎯 2. Radial Seasonal Clock (The Showstopper)",
    "🏙️ 3. Multi-City Comparison", 
    "📋 4. Groupby Data Table"
])

# ----------------- TAB 1: LINE CHART -----------------
with tab1:
    st.subheader(f"Average Annual {pollutant} in {selected_city} (Matplotlib Line Chart)")
    
    fig, ax = plt.subplots(figsize=(10, 5), dpi=200)
    years = yearly_avg.index
    values = yearly_avg.values

    ax.plot(years, values, marker='o', markersize=8, linewidth=2.5, color='#d9381e', label=f'{selected_city} Annual Avg')

    for x, y in zip(years, values):
        ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points", xytext=(0, 8),
                    ha='center', fontweight='bold', fontsize=9.5, color='#2b2b2b')

    if pollutant == "PM2.5":
        ax.axhline(60, color='#e67e22', linestyle='--', linewidth=1.5, label='CPCB Safe Standard (60 µg/m³)')
        ax.axhline(15, color='#27ae60', linestyle=':', linewidth=1.5, label='WHO Safe Limit (15 µg/m³)')
        ax.fill_between(years, values, 60, where=(values >= 60), color='#e74c3c', alpha=0.12, label='Exceeds CPCB Safe Standard')

    ax.set_title(f"{selected_city}: Yearly Average {pollutant} (Pandas groupby)", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Year", fontsize=11, fontweight='bold')
    ax.set_ylabel(f"{pollutant} Concentration", fontsize=11, fontweight='bold')
    ax.set_xticks(years)
    ax.legend(loc='best', frameon=True)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    
    st.pyplot(fig)
    plt.close()
    
    st.info(f"💡 **Key Observation for {selected_city}:** In 2020, nationwide lockdowns caused a sharp dip in emissions compared to 2016-2019.")

# ----------------- TAB 2: RADIAL SEASONAL CLOCK -----------------
with tab2:
    st.subheader(f"🎯 Radial Seasonal Pattern (Polar Clock) for {selected_city}")
    st.markdown("This visualization maps the **12 months of the year onto a 360° circle**, revealing cyclical seasonal pollution spikes.")

    monthly_pivot = city_df.groupby(['Year', 'Month'])[pollutant].mean().unstack(level=0)
    months = np.arange(1, 13)
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    angles = np.linspace(0, 2 * np.pi, len(months), endpoint=False)
    angles_closed = np.concatenate((angles, [angles[0]]))

    fig_polar = plt.figure(figsize=(8, 8), dpi=200)
    ax_polar = fig_polar.add_subplot(111, projection='polar')

    palette = ['#3498db', '#9b59b6', '#1abc9c', '#f39c12', '#e74c3c', '#2c3e50', '#8e44ad']

    for i, yr in enumerate(monthly_pivot.columns):
        vals = monthly_pivot[yr].values
        vals_closed = np.concatenate((vals, [vals[0]]))
        if not np.all(np.isnan(vals_closed)):
            ax_polar.plot(angles_closed, vals_closed, label=f'{yr}', 
                          color=palette[i % len(palette)], linewidth=1.6, marker='o', markersize=3.5, alpha=0.75)

    # Overall seasonal average
    overall_seasonal = city_df.groupby('Month')[pollutant].mean().values
    overall_closed = np.concatenate((overall_seasonal, [overall_seasonal[0]]))
    ax_polar.plot(angles_closed, overall_closed, label='Overall Average Cycle', 
                  color='#c0392b', linewidth=3.2, marker='s', markersize=5)

    if pollutant == "PM2.5":
        ax_polar.fill_between(angles_closed, 0, 60, color='#2ecc71', alpha=0.18, label='CPCB Safe Zone (≤60)')

    ax_polar.set_theta_offset(np.pi / 2)
    ax_polar.set_theta_direction(-1)
    ax_polar.set_thetagrids(np.degrees(angles), month_names, fontsize=11, fontweight='bold')
    ax_polar.grid(True, linestyle=':', alpha=0.6)
    
    ax_polar.legend(loc='upper right', bbox_to_anchor=(1.25, 1.05), frameon=True)
    plt.tight_layout()

    st.pyplot(fig_polar)
    plt.close()

# ----------------- TAB 3: CITY COMPARISON -----------------
with tab3:
    st.subheader("🏙️ City Comparison: Delhi vs. Major Metros")
    compare_cities = st.multiselect("Select Cities to Compare", available_cities, default=["Delhi", "Bengaluru", "Mumbai", "Kolkata"])
    
    if compare_cities:
        comp_df = df[df['City'].isin(compare_cities)].dropna(subset=[pollutant])
        comp_summary = comp_df.groupby(['Year', 'City'])[pollutant].mean().unstack(level=1)

        st.line_chart(comp_summary)
        
        st.write("Average Annual Levels Summary:")
        st.dataframe(comp_summary.style.highlight_max(axis=1, color='#ffcdd2').highlight_min(axis=1, color='#c8e6c9'))

# ----------------- TAB 4: GROUPBY TABLE -----------------
with tab4:
    st.subheader(f"📋 Pandas Groupby Data Table for {selected_city}")
    summary_table = city_df.groupby('Year').agg(
        Days_Recorded=('Date', 'count'),
        Average_Level=(pollutant, 'mean'),
        Min_Level=(pollutant, 'min'),
        Max_Level=(pollutant, 'max')
    ).round(2)
    
    st.dataframe(summary_table, width='stretch')
    
    csv_data = summary_table.to_csv().encode('utf-8')
    st.download_button(
        label=f"📥 Download {selected_city} {pollutant} Summary CSV",
        data=csv_data,
        file_name=f"{selected_city.lower()}_{pollutant.lower()}_yearly_summary.csv",
        mime="text/csv"
    )
