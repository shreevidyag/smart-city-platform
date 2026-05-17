@echo off
REM ============================================================
REM run.bat — One-click Smart City Platform launcher (Windows)
REM Double-click this file to start everything.
REM ============================================================

echo.
echo === Helsinki Smart City Platform ===
echo.

REM Check Python
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python not found. Install from https://python.org
    pause
    exit /b 1
)

echo [1/4] Python found.

REM Install dependencies
echo [2/4] Installing dependencies...
python -m pip install -r requirements.txt -q

REM Train model if not present
IF NOT EXIST "ml_model\lstm_model.keras" (
    echo [3/4] Generating training data...
    python ml_model\generate_training_data.py
    echo [3/4] Training LSTM model - takes about 2 minutes...
    python ml_model\train_lstm.py
) ELSE (
    echo [3/4] Model already trained - skipping.
)

REM Launch dashboard
echo [4/4] Launching dashboard at http://localhost:8501
echo.
python -m streamlit run dashboard\dashboard.py

pause
