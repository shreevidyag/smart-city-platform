"""
generate_training_data.py
Generates 60 days of synthetic sensor data as training_data.csv
Run this first before train_lstm.py
"""
import math, random, os
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)

SENSORS = ["sensor_kallio", "sensor_kamppi", "sensor_pasila"]
rows = []
ts = datetime(2024, 1, 1)
end = ts + timedelta(days=60)

while ts < end:
    h = ts.hour
    weekday = ts.weekday() < 5
    rush = 1 if (7 <= h <= 9 or 16 <= h <= 18) and weekday else 0
    for sid in SENSORS:
        noise = {"sensor_kallio": 3, "sensor_kamppi": 6, "sensor_pasila": 1}[sid]
        rows.append({
            "sensor_id": sid,
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "aqi": max(10, round(42 + 12*math.sin((h-5)*math.pi/12) + rush*25 + random.gauss(0, 4+noise), 1)),
            "traffic_density": max(0.02, min(0.99, round(0.10 + 0.65*math.exp(-0.5*((h-8)/1.3)**2) + random.gauss(0, 0.03), 3))),
            "energy_kwh": max(80, round(180 + 260*(0.3 + 0.7*math.sin((h-2)*math.pi/11)**2) + random.gauss(0, 20), 1)),
        })
    ts += timedelta(minutes=30)

out = os.path.join(os.path.dirname(__file__), "training_data.csv")
df = pd.DataFrame(rows)
df.to_csv(out, index=False)
print(f"[OK] Saved {len(df):,} rows -> {out}")
