#!/bin/bash
# ============================================================
# run.sh — One-click Smart City Platform launcher
# Works on Mac and Linux. On Windows use run.bat instead.
# ============================================================

set -e
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

echo ""
echo -e "${GREEN}=== Helsinki Smart City Platform ===${NC}"
echo ""

# 1. Check Python
if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    echo "Python not found. Install from https://python.org"
    exit 1
fi
PY=$(command -v python3 || command -v python)
echo -e "${GREEN}[1/4]${NC} Python: $($PY --version)"

# 2. Install dependencies
echo -e "${GREEN}[2/4]${NC} Installing dependencies..."
$PY -m pip install -r requirements.txt -q

# 3. Generate data + train model if not present
if [ ! -f "ml_model/lstm_model.keras" ]; then
    echo -e "${GREEN}[3/4]${NC} Generating training data..."
    $PY ml_model/generate_training_data.py
    echo -e "${GREEN}[3/4]${NC} Training LSTM model (takes ~2 minutes)..."
    $PY ml_model/train_lstm.py
else
    echo -e "${GREEN}[3/4]${NC} Model already trained — skipping."
fi

# 4. Launch dashboard
echo -e "${GREEN}[4/4]${NC} Launching dashboard at http://localhost:8501"
echo ""
$PY -m streamlit run dashboard/dashboard.py
