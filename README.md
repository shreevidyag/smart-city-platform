# 🌆 Helsinki Smart City Mini-Platform

**Portfolio project — Shree Vidya Gurudath**  
Master of Business Informatics · Metropolia UAS · Helsinki · 2025

A complete end-to-end Smart City monitoring system: IoT sensor simulation →
MongoDB storage → LSTM air quality forecasting → live Streamlit dashboard →
business case PDF.

🔗 **[Live Demo](https://smart-city-platformgit-unzrefnbzhw8rnxcn7fpoh.streamlit.app/)**  
📄 **[Business Case PDF](business_case/smart_city_business_case.pdf)**

---

## Quickstart (3 options)

### Option A — Double-click (easiest)
- **Mac / Linux:** run `run.sh`
- **Windows:** double-click `run.bat`

Both scripts install everything, train the model, and open the dashboard automatically.

---

### Option B — Terminal (step by step)

**Step 1: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 2: Generate training data**
```bash
python ml_model/generate_training_data.py
```
Creates `ml_model/training_data.csv` (8,640 rows, 60 days of simulated sensor readings).

**Step 3: Train the LSTM model**
```bash
python ml_model/train_lstm.py
```
Takes ~2 minutes. Creates `ml_model/lstm_model.keras` and `ml_model/scaler.pkl`.  
Expected output: `RMSE=6.94  MAE=5.32  R2=0.790`

**Step 4: Run the dashboard**
```bash
streamlit run dashboard/dashboard.py
```
Opens at **http://localhost:8501** — fully interactive with real LSTM forecasts.

---

### Option C — Dashboard only (no ML, instant)
Skip steps 2 & 3. The dashboard falls back to a trend-following forecast if the
model files are not present. Still looks great for a demo.

```bash
pip install streamlit plotly pandas numpy
streamlit run dashboard/dashboard.py
```

---

## 📁 Project Structure

```
smart-city-platform/
│
├── run.sh                          ← one-click launcher (Mac/Linux)
├── run.bat                         ← one-click launcher (Windows)
├── requirements.txt                ← all Python dependencies
│
├── ml_model/
│   ├── generate_training_data.py   ← creates 60-day synthetic CSV
│   ├── train_lstm.py               ← trains LSTM, saves model + scaler
│   ├── training_data.csv           ← auto-generated (8,640 rows)
│   ├── lstm_model.keras            ← auto-generated after training
│   └── scaler.pkl                  ← auto-generated after training
│
├── dashboard/
│   └── dashboard.py                ← Streamlit app (loads real LSTM model)
│
├── simulator/
│   └── sensor_simulator.py         ← live IoT streaming to MongoDB
│
└── business_case/
    ├── build_pdf.py                ← generates the business case PDF
    └── smart_city_business_case.pdf← pre-generated 5-page business case
```

---

## LSTM Model Performance

| Metric | Value | Context |
|--------|-------|---------|
| RMSE   | **6.94 AQI** | Below WHO 10-unit significance threshold |
| MAE    | **5.32 AQI** | Average error < 1 AQI category |
| R²     | **0.790** | Strong predictive power |
| Horizon | **24 steps (12 hours)** | 30-min resolution |
| Architecture | 2-layer LSTM → Dense | Batch norm + dropout |

---

## Simulated Sensor Network

| ID | District | Location |
|----|----------|----------|
| sensor_kallio | Kallio | 60.1836°N, 24.9508°E |
| sensor_kamppi | Kamppi | 60.1690°N, 24.9320°E |
| sensor_pasila | Pasila | 60.1987°N, 24.9336°E |

---

##  Deploy Live (Free — Streamlit Cloud)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account → New app
4. Select repo → main file: `dashboard/dashboard.py`
5. Click **Deploy** — live URL in ~2 minutes

> **Note:** Streamlit Cloud runs the dashboard in simulated-data mode since there is
> no persistent filesystem for the model files. To use the real LSTM forecast on the
> cloud, commit `lstm_model.keras` and `scaler.pkl` to the repo after training locally,
> then redeploy.

---

## Connecting Real Helsinki Data (Optional Upgrade)

Replace the `get_sensor_data()` function in `dashboard/dashboard.py` with:

```python
from pymongo import MongoClient
import streamlit as st

def get_sensor_data(hours):
    client = MongoClient(st.secrets["MONGO_URI"])
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    df = pd.DataFrame(list(
        client.smartcity.sensor_readings
              .find({"timestamp": {"$gte": cutoff}}, {"_id": 0})
    ))
    return df
```

Then run the sensor simulator to stream real data:
```bash
# Edit MONGO_URI in simulator/sensor_simulator.py first
python simulator/sensor_simulator.py --backfill 30   # seed 30 days
python simulator/sensor_simulator.py                  # live stream
```

Free MongoDB Atlas cluster: [mongodb.com/atlas](https://www.mongodb.com/atlas)  
Helsinki open air quality API: [hsy.fi/en/air-quality](https://www.hsy.fi/en/air-quality/)

---

## Business Case

See `business_case/smart_city_business_case.pdf` for:
- Problem statement (Helsinki AQI monitoring gap)
- System architecture
- Business Model Canvas + SWOT
- ROI analysis (95% cost saving vs traditional networks)
- Implementation roadmap

Regenerate it anytime:
```bash
python business_case/build_pdf.py
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Data simulation | Python · NumPy · Pandas |
| IoT streaming | MQTT-ready · MongoDB Atlas |
| Machine learning | TensorFlow 2.x · LSTM · scikit-learn |
| Dashboard | Streamlit · Plotly |
| Business case | ReportLab PDF |
| Deployment | Streamlit Cloud (free) |

---

##  About

This project extends published research on IoT-based air quality monitoring using
LSTM and spatial-temporal models (Information Science & Engineering, RIT Bangalore,
2017–2022) into a production-ready, cloud-native deployment — demonstrating both
technical depth and business informatics strategy.

**Shree Vidya Gurudath**  
📧 shreevidyag@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/shreevidya-gurudath-6437b9200/)  
🎓 MBI · Metropolia UAS · Helsinki, Finland
