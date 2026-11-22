"""
=============================================================================
Project Title: Air Quality Index (AQI) Radial Patterns
Python Lab Project - Data Analysis & Visualization
Dataset: Kaggle Air Quality Data in India (city_day.csv)
=============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set modern aesthetic style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

def run_aqi_analysis():
    print("=" * 65)
    print("       AIR QUALITY INDEX (AQI) - DELHI PM2.5 & RADIAL PATTERNS")
    print("=" * 65)
    
    # ---------------------------------------------------------
    # STEP 1: Load the Dataset
    # ---------------------------------------------------------
    csv_file = "city_day.csv"
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"'{csv_file}' not found. Please ensure it is in the same directory.")
        
    print(f"\n[1/5] Loading '{csv_file}'...")
    df = pd.read_csv(csv_file)
    print(f"      Total records loaded: {len(df):,} rows across {df['City'].nunique()} cities.")

    # ---------------------------------------------------------
    # STEP 2: Filter for Single City ("Delhi") & Extract Year
    # ---------------------------------------------------------
    print("\n[2/5] Filtering data for single city: 'Delhi'...")
    delhi_df = df[df['City'] == 'Delhi'].copy()
    
    # Convert 'Date' column to datetime format
    delhi_df['Date'] = pd.to_datetime(delhi_df['Date'])
    
    # Extract Year and Month from the Date column
    delhi_df['Year'] = delhi_df['Date'].dt.year
    delhi_df['Month'] = delhi_df['Date'].dt.month
    
    # Handle missing PM2.5 values using forward fill or dropping for clean averages
    null_count = delhi_df['PM2.5'].isna().sum()
    print(f"      Delhi records: {len(delhi_df)} days (2015 to 2020). Missing PM2.5 values: {null_count}")

    # ---------------------------------------------------------
    # STEP 3: Pandas groupby to find Average PM2.5 per Year
    # ---------------------------------------------------------
    print("\n[3/5] Calculating average PM2.5 per year using Pandas groupby()...")
    yearly_pm25 = delhi_df.groupby('Year')['PM2.5'].mean().round(2)
    
    print("\n      ---------------------------------------")
    print("      Year    Average PM2.5 (µg/m³)   Status")
    print("      ---------------------------------------")
    for yr, val in yearly_pm25.items():
        note = " (COVID Lockdown Drop)" if yr == 2020 else ""
        print(f"      {yr}     {val:6.2f} µg/m³         {note}")
    print("      ---------------------------------------")

    # ---------------------------------------------------------
    # STEP 4: Matplotlib Line Chart (Elevated Lab Requirement)
    # ---------------------------------------------------------
    print("\n[4/5] Generating Figure 1: Annual PM2.5 Trend Line Chart...")
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    years = yearly_pm25.index
    values = yearly_pm25.values

    # Plot line and points
    ax.plot(years, values, marker='o', markersize=9, linewidth=2.8, color='#d9381e', label='Delhi Annual Average PM2.5')

    # Add data labels on points
    for x, y in zip(years, values):
        ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points", xytext=(0, 10),
                    ha='center', fontweight='bold', fontsize=10, color='#2b2b2b')

    # Reference standard lines (CPCB Standard = 60 µg/m³, WHO Limit = 15 µg/m³)
    ax.axhline(60, color='#e67e22', linestyle='--', linewidth=1.8, label='CPCB Safe Limit (60 µg/m³)')
    ax.axhline(15, color='#27ae60', linestyle=':', linewidth=1.8, label='WHO Safe Limit (15 µg/m³)')

    # Add fill under the curve
    ax.fill_between(years, values, 60, where=(values >= 60), color='#e74c3c', alpha=0.15, label='Exceeds CPCB Safe Level')

    # Highlight 2020 COVID lockdown drop
    ax.annotate("2020 Drop:\nCOVID-19 Lockdown\n& partial year data", 
                xy=(2020, values[-1]), xytext=(2018.5, 65),
                arrowprops=dict(facecolor='#2980b9', shrink=0.08, width=1.5, headwidth=7),
                bbox=dict(boxstyle="round,pad=0.4", facecolor='#ebf5fb', edgecolor='#2980b9', alpha=0.9),
                fontsize=9.5, fontweight='bold', color='#1b4f72')

    ax.set_title("Delhi Air Quality: Average Annual PM2.5 Level (2015 - 2020)", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Year", fontsize=12, fontweight='bold', labelpad=10)
    ax.set_ylabel("PM2.5 Concentration (µg/m³)", fontsize=12, fontweight='bold', labelpad=10)
    ax.set_xticks(years)
    ax.set_ylim(0, 160)
    ax.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9)
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    line_chart_path = "figure1_yearly_pm25_line_chart.png"
    plt.savefig(line_chart_path)
    plt.close()
    print(f"      Saved: {line_chart_path}")

    # ---------------------------------------------------------
    # STEP 5: The Showstopper - "AQI Radial Patterns" (Polar Plot)
    # ---------------------------------------------------------
    print("\n[5/5] Generating Figure 2: The 'Radial Seasonal Pattern' (Polar Clock)...")
    
    # Calculate monthly average across months (1 to 12) for each year
    monthly_pivot = delhi_df.groupby(['Year', 'Month'])['PM2.5'].mean().unstack(level=0)
    
    # Polar angles for 12 months (0 to 2*pi)
    months = np.arange(1, 13)
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    angles = np.linspace(0, 2 * np.pi, len(months), endpoint=False)
    
    # To close the circular loop, append first element to end
    angles_closed = np.concatenate((angles, [angles[0]]))
    
    fig = plt.figure(figsize=(10, 10), dpi=300)
    ax_polar = fig.add_subplot(111, projection='polar')

    # Color palette for years
    year_colors = {
        2015: '#3498db',
        2016: '#9b59b6',
        2017: '#1abc9c',
        2018: '#f39c12',
        2019: '#e74c3c',
        2020: '#2c3e50'
    }

    # Plot each year's radial loop
    for yr in monthly_pivot.columns:
        vals = monthly_pivot[yr].values
        # Close loop
        vals_closed = np.concatenate((vals, [vals[0]]))
        
        # Plot if there are valid values
        valid_mask = ~np.isnan(vals_closed)
        if valid_mask.sum() > 2:
            ax_polar.plot(angles_closed, vals_closed, label=f'{yr}', color=year_colors.get(yr, 'grey'),
                          linewidth=1.8, marker='o', markersize=4, alpha=0.85)

    # Calculate overall multi-year monthly average to show the distinct seasonal "winter bulge"
    overall_monthly_avg = delhi_df.groupby('Month')['PM2.5'].mean().values
    overall_closed = np.concatenate((overall_monthly_avg, [overall_monthly_avg[0]]))
    
    ax_polar.plot(angles_closed, overall_closed, label='Overall Average Cycle', 
                  color='#c0392b', linewidth=3.5, linestyle='-', marker='s', markersize=6)
    
    # Shading the safe zone in green center
    ax_polar.fill_between(angles_closed, 0, 60, color='#2ecc71', alpha=0.18, label='CPCB Safe Zone (≤60 µg/m³)')

    # Polar formatting: 12 radial slices for months
    ax_polar.set_theta_offset(np.pi / 2)  # Start at top (12 o'clock = Jan)
    ax_polar.set_theta_direction(-1)       # Clockwise direction
    ax_polar.set_thetagrids(np.degrees(angles), month_names, fontsize=12, fontweight='bold', color='#1a252f')
    
    # Radial ring limit & labels
    ax_polar.set_ylim(0, 320)
    ax_polar.set_rlabel_position(75)
    ax_polar.set_rticks([50, 100, 150, 200, 250, 300])
    ax_polar.grid(True, linestyle=':', alpha=0.6, color='#7f8c8d')
    
    # Title with generous padding to prevent overlap
    fig.suptitle("Delhi PM2.5 Radial Seasonal Clock (2015 - 2020)", 
                 fontsize=15, fontweight='bold', color='#2c3e50', y=0.98)
    ax_polar.set_title("Exposing the severe cyclical winter flare (Oct–Jan) vs. monsoon dip (Jul–Aug)",
                       fontsize=11, fontstyle='italic', color='#555555', pad=35)
    
    ax_polar.legend(loc='upper right', bbox_to_anchor=(1.30, 1.05), frameon=True, 
                    facecolor='#ffffff', edgecolor='#bdc3c7', fontsize=10)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    radial_chart_path = "figure2_aqi_radial_seasonal_pattern.png"
    plt.savefig(radial_chart_path)
    plt.close()
    print(f"      Saved: {radial_chart_path}")

    print("\n" + "=" * 65)
    print("SUCCESS! Both figures have been generated and saved:")
    print(f"1. {os.path.abspath(line_chart_path)}")
    print(f"2. {os.path.abspath(radial_chart_path)}")
    print("=" * 65)

if __name__ == '__main__':
    run_aqi_analysis()
