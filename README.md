# Project 14: Air Quality Index (AQI) Radial Patterns & Annual Trends

**Course:** Python Programming Lab  
**Dataset:** Kaggle - [Air Quality Data in India (2015 - 2020)](https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india)  

---

## 📌 Project Overview & Question

### Lab Question:
> *Filter the data for a single city (e.g., "Delhi"). Extract the year from the Date column. Use Pandas groupby to find the average PM2.5 level per year in that city, and plot it as a Matplotlib line chart.*

### Why This Project Stands Out:
1. **Title Alignment ("Radial Patterns")**: The topic title is *"AQI Radial Patterns"*. Rather than just producing a standard line chart, this project transforms multi-year seasonal air quality into a **12-Month Radial Polar Clock Chart**.
2. **Benchmark Comparisons**: Overlays official **CPCB Safe Limit (60 µg/m³)** and **WHO Safe Guidelines (15 µg/m³)**.
3. **Event Impact Analysis**: Annotates and quantifies the **2020 COVID-19 lockdown emissions drop**.
4. **Interactive Viva Demo**: Includes an interactive **Streamlit web dashboard** (`app.py`) allowing examiners to explore all 26 cities in real time.

---

## 📂 Project Structure

| File | Purpose |
| :--- | :--- |
| `city_day.csv` | Kaggle dataset containing daily AQI and pollutant records (2015–2020). |
| `analysis.py` | Complete Python script that performs the filtering, groupby, and saves the publication-quality charts. |
| `figure1_yearly_pm25_line_chart.png` | Required Matplotlib line chart with CPCB/WHO lines and 2020 lockdown callout. |
| `figure2_aqi_radial_seasonal_pattern.png` | Showstopper 12-month radial polar clock demonstrating winter flaring vs. monsoon washout. |
| `aqi_project_notebook.ipynb` | Ready-to-submit Jupyter Notebook with formatted narrative markdown and code. |
| `app.py` | Interactive Streamlit web app with city selector, live tabs, and comparison tools. |

---

## 🚀 How to Run

### Option 1: Run the Core Python Analysis Script
Generates both figures and outputs the groupby summary in your terminal:
```bash
cd "c:\suraj mahato\aqi_radial_patterns"
python analysis.py
```

### Option 2: Run the Interactive Web Dashboard (Streamlit)
Launches the live interactive app in your browser:
```bash
cd "c:\suraj mahato\aqi_radial_patterns"
streamlit run app.py
```

### Option 3: Open in Jupyter Notebook or VS Code
Open `aqi_project_notebook.ipynb` directly in VS Code or Jupyter:
```bash
jupyter notebook aqi_project_notebook.ipynb
```

---

## 📊 Key Results (Delhi PM2.5)

| Year | Average PM2.5 (µg/m³) | CPCB Status (Limit: 60 µg/m³) | Observation |
| :---: | :---: | :---: | :--- |
| **2015** | 117.34 | Exceeded (1.95x) | Severe baseline |
| **2016** | 138.50 | Exceeded (2.31x) | **Peak historic high** |
| **2017** | 125.09 | Exceeded (2.08x) | High winter pollution |
| **2018** | 115.02 | Exceeded (1.92x) | Gradual reduction starts |
| **2019** | 108.50 | Exceeded (1.81x) | Cleaner pre-lockdown year |
| **2020** | **80.32** | Exceeded (1.34x) | **~26% sharp drop due to COVID-19 lockdown** |

---

## 🎓 Lab Viva Questions & Model Answers

**Q1: How did you extract the year from the date column in Pandas?**  
> *"First, I converted the Date string into Pandas datetime using `pd.to_datetime(df['Date'])`. Then I extracted the year using the datetime accessor: `df['Date'].dt.year`."*

**Q2: What does `delhi_df.groupby('Year')['PM2.5'].mean()` do?**  
> *"It partitions all the rows for Delhi by their Year value, extracts the 'PM2.5' column for each group, and calculates the arithmetic mean for each year."*

**Q3: Why did you plot a Radial / Polar chart for AQI?**  
> *"Because air pollution follows a strong annual cyclical pattern. A linear plot spreads time on a flat axis, whereas a polar chart places the 12 months in a full 360° circle. It visually highlights that pollution expands outward in winter (Oct–Jan) and contracts inward during monsoon (Jul–Aug)."*

**Q4: Why does PM2.5 drop sharply in July and August?**  
> *"Monsoon rains cause 'wet deposition' or rain washout, where raindrops scrub particulate matter from the atmosphere."*

**Q5: Why is 2020 so much lower than 2016?**  
> *"Two reasons: (1) The nationwide COVID-19 lockdowns in early 2020 drastically reduced vehicular and industrial emissions. (2) The dataset ends in July 2020, excluding the heavily polluted winter months of late 2020."*
