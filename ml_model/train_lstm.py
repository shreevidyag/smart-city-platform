"""
train_lstm.py
Trains a 2-layer LSTM to forecast AQI 12 hours ahead.
Saves: lstm_model.keras  scaler.pkl

Usage:
    python train_lstm.py
"""
import os, warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

HERE = os.path.dirname(__file__)
CSV  = os.path.join(HERE, "training_data.csv")
MODEL_OUT  = os.path.join(HERE, "lstm_model.keras")
SCALER_OUT = os.path.join(HERE, "scaler.pkl")

FEATURES  = ["aqi", "traffic_density", "energy_kwh"]
LOOKBACK  = 48   # 24 hrs at 30-min resolution
HORIZON   = 24   # predict next 12 hrs
EPOCHS    = 60
BATCH     = 32

def make_sequences(data, lb, hz):
    X, y = [], []
    tc = FEATURES.index("aqi")
    for i in range(len(data) - lb - hz + 1):
        X.append(data[i:i+lb])
        y.append(data[i+lb:i+lb+hz, tc])
    return np.array(X), np.array(y)

def main():
    print("\n=== Smart City LSTM Training ===")

    # 1. load & aggregate across sensors
    df = pd.read_csv(CSV, parse_dates=["timestamp"])
    df = df.groupby("timestamp")[FEATURES].mean().reset_index().sort_values("timestamp")
    print(f"  Rows: {len(df):,}")

    # 2. scale
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df[FEATURES])
    joblib.dump(scaler, SCALER_OUT)

    # 3. sequences
    X, y = make_sequences(scaled, LOOKBACK, HORIZON)
    split = int(len(X) * 0.85)
    X_tr, X_te = X[:split], X[split:]
    y_tr, y_te = y[:split], y[split:]
    print(f"  Train {X_tr.shape}  Test {X_te.shape}")

    # 4. model
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
    from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=(LOOKBACK, len(FEATURES))),
        BatchNormalization(), Dropout(0.2),
        LSTM(32),
        BatchNormalization(), Dropout(0.2),
        Dense(64, activation="relu"),
        Dense(HORIZON),
    ])
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    model.summary()

    cbs = [
        EarlyStopping(patience=8, restore_best_weights=True),
        ReduceLROnPlateau(factor=0.5, patience=4, min_lr=1e-5),
    ]
    model.fit(X_tr, y_tr, validation_split=0.1,
              epochs=EPOCHS, batch_size=BATCH, callbacks=cbs, verbose=1)

    # 5. evaluate (inverse transform)
    tc = FEATURES.index("aqi")
    def inv(arr):
        d = np.zeros((arr.shape[0]*arr.shape[1], len(FEATURES)))
        d[:, tc] = arr.flatten()
        return scaler.inverse_transform(d)[:, tc].reshape(arr.shape)

    yp = inv(model.predict(X_te, verbose=0))
    yt = inv(y_te)
    rmse = np.sqrt(mean_squared_error(yt.flatten(), yp.flatten()))
    mae  = mean_absolute_error(yt.flatten(), yp.flatten())
    r2   = r2_score(yt.flatten(), yp.flatten())
    print(f"\n  RMSE={rmse:.2f}  MAE={mae:.2f}  R2={r2:.3f}")

    # 6. save
    model.save(MODEL_OUT)
    print(f"  Model -> {MODEL_OUT}")
    print(f"  Scaler -> {SCALER_OUT}\n")

if __name__ == "__main__":
    main()
