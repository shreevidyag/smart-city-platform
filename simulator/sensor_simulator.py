"""
sensor_simulator.py  —  Smart City IoT Sensor Simulator
========================================================
Simulates 3 sensor nodes streaming to MongoDB.

Usage:
    python sensor_simulator.py                  # live mode (30-sec intervals)
    python sensor_simulator.py --backfill 30    # generate 30 days historical data
    python sensor_simulator.py --export out.csv # export last 7 days to CSV

Requires: pip install pymongo pandas
MongoDB: free cloud instance at mongodb.com/atlas (no credit card needed)
"""

import argparse, math, random, time
from datetime import datetime, timedelta
import pandas as pd

MONGO_URI  = "mongodb://localhost:27017/"   # ← replace with Atlas URI
DB_NAME    = "smartcity"
COLLECTION = "sensor_readings"

SENSORS = {
    "sensor_kallio": {"lat": 60.1836, "lon": 24.9508, "district": "Kallio"},
    "sensor_kamppi": {"lat": 60.1690, "lon": 24.9320, "district": "Kamppi"},
    "sensor_pasila": {"lat": 60.1987, "lon": 24.9336, "district": "Pasila"},
}

def _aqi(h, wd):
    rush = 1 if (7<=h<=9 or 16<=h<=18) and wd else 0
    return max(10, round(42+12*math.sin((h-5)*math.pi/12)+rush*25+random.gauss(0,4),1))

def _traffic(h, wd):
    if not wd: base = 0.15+0.25*math.sin((h-11)*math.pi/10)
    else: base = 0.10+0.65*max(math.exp(-0.5*((h-8)/1.2)**2), math.exp(-0.5*((h-17)/1.5)**2))
    return max(0.02, min(0.99, round(base+random.gauss(0,.03),3)))

def _energy(h):
    return max(80, round(180+260*(0.3+0.7*math.sin((h-2)*math.pi/11)**2)+random.gauss(0,20),1))

def _noise(h):
    return max(25, round(38+22*math.sin((h-5)*math.pi/12)+random.gauss(0,3),1))

def reading(sid, meta, ts):
    h, wd = ts.hour, ts.weekday()<5
    return {"sensor_id":sid,"district":meta["district"],"lat":meta["lat"],"lon":meta["lon"],
            "timestamp":ts,"aqi":_aqi(h,wd),"traffic_density":_traffic(h,wd),
            "energy_kwh":_energy(h),"noise_db":_noise(h)}

def live_mode(col, interval=30):
    print(f"[LIVE] Streaming every {interval}s. Ctrl+C to stop.")
    while True:
        ts = datetime.utcnow()
        batch = [reading(sid,meta,ts) for sid,meta in SENSORS.items()]
        col.insert_many(batch)
        for r in batch:
            print(f"  {r['timestamp'].strftime('%H:%M:%S')}  {r['district']:<10}  AQI={r['aqi']:>5.1f}  Traffic={r['traffic_density']:.2f}")
        time.sleep(interval)

def backfill_mode(col, days=30):
    print(f"[BACKFILL] Generating {days} days …")
    ts = datetime.utcnow()-timedelta(days=days); docs=[]
    while ts <= datetime.utcnow():
        for sid,meta in SENSORS.items(): docs.append(reading(sid,meta,ts))
        ts += timedelta(minutes=30)
        if len(docs)>=500: col.insert_many(docs); docs=[]
    if docs: col.insert_many(docs)
    print(f"  Done: ~{days*48*len(SENSORS):,} documents inserted")

def export_mode(col, path, days=7):
    cutoff = datetime.utcnow()-timedelta(days=days)
    df = pd.DataFrame(list(col.find({"timestamp":{"$gte":cutoff}},{"_id":0})))
    df.sort_values(["sensor_id","timestamp"],inplace=True)
    df.to_csv(path, index=False)
    print(f"  Exported {len(df):,} rows → {path}")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--backfill", type=int, metavar="DAYS")
    p.add_argument("--export",   type=str, metavar="FILE")
    p.add_argument("--interval", type=int, default=30)
    args = p.parse_args()
    try:
        from pymongo import MongoClient
        col = MongoClient(MONGO_URI)[DB_NAME][COLLECTION]
        col.create_index([("timestamp",1)])
        col.create_index([("sensor_id",1),("timestamp",1)])
    except ImportError:
        print("[ERROR] pymongo not installed. Run: pip install pymongo")
        return
    if args.backfill: backfill_mode(col, args.backfill)
    elif args.export:  export_mode(col, args.export)
    else:              live_mode(col, args.interval)

if __name__ == "__main__": main()
