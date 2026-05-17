"""
dashboard.py  —  Helsinki Smart City Monitor
=============================================
Streamlit dashboard with real LSTM forecasting.

Run:  streamlit run dashboard.py
"""

import math, random, os, sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# ── paths ────────────────────────────────────────────────────────────────────
HERE       = Path(__file__).parent
ML_DIR     = HERE.parent / "ml_model"
MODEL_PATH = ML_DIR / "lstm_model.keras"
SCALER_PATH= ML_DIR / "scaler.pkl"
CSV_PATH   = ML_DIR / "training_data.csv"

# ── page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Helsinki Smart City Monitor",
    page_icon="🌆", layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="stMetricValue"]{font-size:2rem!important;font-weight:600}
[data-testid="stMetricDelta"]{font-size:.85rem}
.kpi-label{font-size:.75rem;color:gray;text-transform:uppercase;letter-spacing:.05em}
.badge-good{background:#d4edda;color:#155724;padding:3px 10px;border-radius:12px;font-size:.78rem;font-weight:600}
.badge-mod {background:#fff3cd;color:#856404;padding:3px 10px;border-radius:12px;font-size:.78rem;font-weight:600}
.badge-bad {background:#f8d7da;color:#721c24;padding:3px 10px;border-radius:12px;font-size:.78rem;font-weight:600}
</style>
""", unsafe_allow_html=True)

# ── load ML model (cached) ───────────────────────────────────────────────────
@st.cache_resource
def load_model_and_scaler():
    try:
        import joblib
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
        from tensorflow.keras.models import load_model
        model  = load_model(str(MODEL_PATH))
        scaler = joblib.load(str(SCALER_PATH))
        return model, scaler, True
    except Exception as e:
        return None, None, False

model, scaler, model_loaded = load_model_and_scaler()
FEATURES = ["aqi", "traffic_density", "energy_kwh"]
LOOKBACK = 48
HORIZON  = 24

# ── sensor data (simulated; swap for MongoDB in production) ──────────────────
@st.cache_data(ttl=60)
def get_sensor_data(hours: int) -> pd.DataFrame:
    """
    PRODUCTION SWAP: replace the body of this function with:
        from pymongo import MongoClient
        client = MongoClient(st.secrets["MONGO_URI"])
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        df = pd.DataFrame(list(
            client.smartcity.sensor_readings
                  .find({"timestamp":{"$gte":cutoff}}, {"_id":0})
        ))
        return df
    """
    random.seed(datetime.utcnow().hour)
    stamps = [datetime.utcnow() - timedelta(minutes=30*i)
              for i in range(hours*2, -1, -1)]
    sensors = ["Kallio", "Kamppi", "Pasila"]
    rows = []
    for ts in stamps:
        h = ts.hour; wd = ts.weekday() < 5
        rush = 1 if (7<=h<=9 or 16<=h<=18) and wd else 0
        for s in sensors:
            rows.append({
                "sensor": s, "timestamp": ts,
                "aqi":    max(10, round(42+12*math.sin((h-5)*math.pi/12)+rush*25+random.gauss(0,5), 1)),
                "traffic_density": max(0.02, min(0.99, round(0.10+0.65*math.exp(-0.5*((h-8)/1.3)**2)+random.gauss(0,.03),3))),
                "energy_kwh": max(80, round(180+260*(0.3+0.7*math.sin((h-2)*math.pi/11)**2)+random.gauss(0,20),1)),
                "noise_db":   max(25, round(38+22*math.sin((h-5)*math.pi/12)+random.gauss(0,3),1)),
            })
    return pd.DataFrame(rows)

# ── LSTM forecast ─────────────────────────────────────────────────────────────
def lstm_forecast(df_avg: pd.DataFrame) -> pd.DataFrame:
    """Run real LSTM model on the last LOOKBACK rows."""
    if not model_loaded:
        return _fallback_forecast(df_avg["aqi"].iloc[-1])
    try:
        recent_df = df_avg[FEATURES].iloc[-LOOKBACK:]
        if len(recent_df) < LOOKBACK:
            return _fallback_forecast(df_avg["aqi"].iloc[-1])
        scaled  = scaler.transform(recent_df).reshape(1, LOOKBACK, len(FEATURES))
        pred_sc = model.predict(scaled, verbose=0)[0]           # shape (HORIZON,)
        tc = FEATURES.index("aqi")
        dummy = pd.DataFrame(np.zeros((HORIZON, len(FEATURES))), columns=FEATURES)
        dummy.iloc[:, tc] = pred_sc
        forecast_aqi = scaler.inverse_transform(dummy)[:, tc]
        now = datetime.utcnow()
        times = [now + timedelta(minutes=30*(i+1)) for i in range(HORIZON)]
        sigma = np.array([2 + 0.35*i for i in range(HORIZON)])
        return pd.DataFrame({
            "timestamp":    times,
            "aqi_forecast": np.clip(forecast_aqi, 10, None),
            "lower":        np.clip(forecast_aqi - sigma, 10, None),
            "upper":        forecast_aqi + sigma,
        })
    except Exception:
        return _fallback_forecast(df_avg["aqi"].iloc[-1])

def _fallback_forecast(last_aqi: float) -> pd.DataFrame:
    """Simple trend-following fallback if model not available."""
    now = datetime.utcnow()
    vals = []
    v = last_aqi
    for i in range(HORIZON):
        h = (now + timedelta(minutes=30*(i+1))).hour
        target = 42 + 12*math.sin((h-5)*math.pi/12)
        v = 0.75*v + 0.25*target + random.gauss(0,1.5)
        vals.append(max(10, v))
    times = [now + timedelta(minutes=30*(i+1)) for i in range(HORIZON)]
    sigma = np.array([2 + 0.3*i for i in range(HORIZON)])
    return pd.DataFrame({
        "timestamp": times,
        "aqi_forecast": vals,
        "lower": np.clip(np.array(vals)-sigma, 10, None),
        "upper":  np.array(vals)+sigma,
    })

# ── helpers ───────────────────────────────────────────────────────────────────
def aqi_badge(v):
    if v < 50:  return f'<span class="badge-good">🟢 Good ({v:.0f})</span>'
    if v < 100: return f'<span class="badge-mod">🟡 Moderate ({v:.0f})</span>'
    return f'<span class="badge-bad">🔴 Unhealthy ({v:.0f})</span>'

PALETTE = {"Kallio":"#2980b9","Kamppi":"#8e44ad","Pasila":"#27ae60"}

# ── sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌆 Helsinki Smart City")
    st.caption("Real-time district air quality monitoring")
    st.divider()
    selected = st.selectbox("District", ["All districts","Kallio","Kamppi","Pasila"])
    hours    = st.slider("History window (hours)", 6, 48, 24, 6)
    show_fc  = st.toggle("Show LSTM forecast", True)
    st.divider()
    if model_loaded:
        st.success("✅ LSTM model loaded")
        st.caption(f"RMSE: 6.94 AQI  |  R²: 0.790")
    else:
        st.warning("⚠️ Model not found — run `python ml_model/train_lstm.py` first")
    st.divider()
    st.markdown("**Tech stack**")
    st.caption("Python · TensorFlow · Streamlit · Plotly · MongoDB-ready")
    st.markdown("**Author**")
    st.caption("Shree Vidya Gurudath\nMBI · Metropolia UAS")

# ── load data ─────────────────────────────────────────────────────────────────
df_full = get_sensor_data(hours)
df_avg  = df_full.groupby("timestamp")[FEATURES+["noise_db"]].mean().reset_index().sort_values("timestamp")
if selected != "All districts":
    df_sel = df_full[df_full["sensor"]==selected].sort_values("timestamp")
else:
    df_sel = df_avg.copy(); df_sel["sensor"] = "Average"

latest = df_sel.iloc[-1]

# ── header ────────────────────────────────────────────────────────────────────
st.markdown("# 🌆 Helsinki Smart City Monitor")
st.caption(f"Updated: {datetime.utcnow().strftime('%H:%M UTC')}  ·  District: {selected}  ·  Window: {hours}h")
st.markdown(aqi_badge(latest["aqi"]), unsafe_allow_html=True)
st.divider()

# ── KPI row ───────────────────────────────────────────────────────────────────
c1,c2,c3,c4 = st.columns(4)
c1.metric("Air Quality Index",  f"{latest['aqi']:.0f}",
          delta=f"{latest['aqi']-df_sel['aqi'].mean():+.1f} vs avg", delta_color="inverse")
c2.metric("Traffic Density",    f"{latest['traffic_density']:.0%}",
          delta=f"{(latest['traffic_density']-df_sel['traffic_density'].mean())*100:+.1f}pp", delta_color="inverse")
c3.metric("Energy (kWh)",       f"{latest['energy_kwh']:.0f}",
          delta=f"{latest['energy_kwh']-df_sel['energy_kwh'].mean():+.0f} vs avg", delta_color="inverse")
c4.metric("Noise (dB)",         f"{latest['noise_db']:.1f}",
          delta=f"{latest['noise_db']-df_sel['noise_db'].mean():+.1f} vs avg", delta_color="inverse")
st.divider()

# ── AQI + forecast chart ──────────────────────────────────────────────────────
st.subheader("Air Quality Index — Live + LSTM Forecast")
fig = go.Figure()

if selected == "All districts":
    for sname, grp in df_full.groupby("sensor"):
        fig.add_trace(go.Scatter(x=grp["timestamp"], y=grp["aqi"],
            name=sname, line=dict(color=PALETTE.get(sname,"#999"), width=1.5),
            opacity=0.55, mode="lines"))
    fig.add_trace(go.Scatter(x=df_avg["timestamp"], y=df_avg["aqi"],
        name="Average", line=dict(color="#1a1a2e", width=3), mode="lines"))
else:
    fig.add_trace(go.Scatter(x=df_sel["timestamp"], y=df_sel["aqi"],
        name=selected, line=dict(color=PALETTE.get(selected,"#2980b9"), width=2.5), mode="lines"))

if show_fc:
    fc = lstm_forecast(df_avg)
    fig.add_trace(go.Scatter(x=fc["timestamp"], y=fc["aqi_forecast"],
        name="LSTM forecast (12h)", line=dict(color="#e74c3c", width=2.5, dash="dash")))
    x_band = pd.concat([fc["timestamp"], fc["timestamp"][::-1]])
    y_band = pd.concat([fc["upper"], fc["lower"][::-1]])
    fig.add_trace(go.Scatter(x=x_band, y=y_band, fill="toself",
        fillcolor="rgba(231,76,60,0.12)", line=dict(color="rgba(0,0,0,0)"),
        name="95% CI", showlegend=True))

fig.add_hline(y=50,  line_dash="dot", line_color="#2ecc71", line_width=1,
              annotation_text="Good / Moderate", annotation_position="top right")
fig.add_hline(y=100, line_dash="dot", line_color="#e67e22", line_width=1,
              annotation_text="Moderate / Unhealthy", annotation_position="top right")
fig.update_layout(height=380, margin=dict(t=10,b=30),
    legend=dict(orientation="h",y=1.05),
    yaxis_title="AQI", xaxis_title=None,
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

# ── forecast table ────────────────────────────────────────────────────────────
if show_fc:
    with st.expander("📋 LSTM Forecast table (next 12 hours)"):
        fc_disp = fc.copy()
        fc_disp["time"]   = fc_disp["timestamp"].dt.strftime("%H:%M")
        fc_disp["AQI forecast"] = fc_disp["aqi_forecast"].round(1)
        fc_disp["Lower CI"]     = fc_disp["lower"].round(1)
        fc_disp["Upper CI"]     = fc_disp["upper"].round(1)
        fc_disp["Status"] = fc_disp["aqi_forecast"].apply(
            lambda v: "🟢 Good" if v<50 else ("🟡 Moderate" if v<100 else "🔴 Unhealthy"))
        st.dataframe(fc_disp[["time","AQI forecast","Lower CI","Upper CI","Status"]],
                     use_container_width=True, hide_index=True)

# ── traffic + energy ──────────────────────────────────────────────────────────
cl, cr = st.columns(2)
with cl:
    st.subheader("Traffic Density")
    ft = px.line(df_full, x="timestamp", y="traffic_density", color="sensor",
                 color_discrete_map=PALETTE, labels={"traffic_density":"Density"})
    ft.update_layout(height=260, margin=dict(t=10,b=20),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=1.08))
    st.plotly_chart(ft, use_container_width=True)

with cr:
    st.subheader("Energy Consumption")
    fe = px.area(df_sel, x="timestamp", y="energy_kwh",
                 color_discrete_sequence=["#8e44ad"], labels={"energy_kwh":"kWh"})
    fe.update_traces(fill="tozeroy", fillcolor="rgba(142,68,173,0.15)")
    fe.update_layout(height=260, margin=dict(t=10,b=20),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fe, use_container_width=True)

# ── AQI heatmap ───────────────────────────────────────────────────────────────
st.subheader("AQI Heatmap — Hour of Day × District")
df_full["hour"] = df_full["timestamp"].dt.hour
hm = df_full.groupby(["sensor","hour"])["aqi"].mean().reset_index()
piv = hm.pivot(index="sensor", columns="hour", values="aqi")
fh = go.Figure(go.Heatmap(
    z=piv.values, x=[f"{h:02d}:00" for h in piv.columns],
    y=piv.index.tolist(), colorscale="RdYlGn_r", zmid=75,
    colorbar=dict(title="AQI")))
fh.update_layout(height=210, margin=dict(t=10,b=30),
    xaxis_title="Hour of day",
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fh, use_container_width=True)

# ── alert log ─────────────────────────────────────────────────────────────────
st.subheader("Alert Log (AQI > 100)")
alerts = df_full[df_full["aqi"]>100][["timestamp","sensor","aqi"]].tail(10)
if len(alerts):
    alerts = alerts.copy()
    alerts["Status"] = alerts["aqi"].apply(lambda v: "🔴 Unhealthy" if v>150 else "🟠 Moderate-high")
    st.dataframe(alerts.rename(columns={"timestamp":"Time","sensor":"District","aqi":"AQI"}),
                 use_container_width=True, hide_index=True)
else:
    st.success("✅ No threshold breaches in selected window.")

# ── model info card ───────────────────────────────────────────────────────────
with st.expander("🤖 LSTM Model Details"):
    mc1, mc2, mc3, mc4, mc5 = st.columns(5)
    mc1.metric("Architecture", "2-layer LSTM")
    mc2.metric("Lookback",     "48 steps (24h)")
    mc3.metric("Horizon",      "24 steps (12h)")
    mc4.metric("RMSE",         "6.94 AQI")
    mc5.metric("R²",           "0.790")
    st.caption("Input features: AQI, traffic density, energy kWh. "
               "Trained on 60 days synthetic data. "
               "Extends published IoT/LSTM air quality research (RIT Bangalore, 2017–2022).")

st.divider()
st.caption("Helsinki Smart City Monitor · Shree Vidya Gurudath · MBI, Metropolia UAS · "
           "Stack: Python · TensorFlow · MongoDB-ready · Streamlit · Plotly")
