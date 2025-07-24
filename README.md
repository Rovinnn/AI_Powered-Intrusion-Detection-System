# 🚀 AI-Powered Intrusion Detection System (IDS)

Detect cyber attacks *in real time* with cutting-edge AI! This project harnesses **XGBoost** and the massive **CICIDS2017** dataset to build a super-accurate network intrusion detection system — ready for deployment.

---

## ✨ Highlights

- 💥 Processed **2.2 million+** network flows from CICIDS2017 — massive scale!
- 🎯 Balanced tricky class imbalances with **SMOTE** to catch rare attacks.
- 🔥 Combined rare attacks into a unified **RareAttack** category for cleaner predictions.
- ⚡ Integrated **NFStreamer-compatible** features for lightning-fast, live packet classification.
- 📈 Achieved a **99.8% weighted F1-score** across 9 attack types — DDoS, PortScan, Botnet & more.
- 💾 Exported trained model & preprocessing pipeline as `.joblib` files for seamless deployment.
- 🔍 Rigorous **cross-validation** and sanity checks to ensure rock-solid accuracy.

---

## 🚀 Getting Started

### What You Need

- Python 3.8+ installed
- Dependencies — just run:

  ```bash
  pip install pandas numpy scikit-learn imbalanced-learn xgboost joblib

    Combined CICIDS2017 dataset (combine.csv) with NFStreamer features

How to Use

    Preprocess the data and balance classes with SMOTE.

    Train the XGBoost model on the cleaned dataset.

    Evaluate using precision, recall, F1, and confusion matrix.

    Save your model & scaler for real-time predictions!

Check out the ids_training.py script for the full workflow.
📊 Results at a Glance
Metric	Score
Weighted F1	99.2%
Top Features	Bwd Packet Length Std, Average Packet Size, PSH Flag Count, and more

Cross-validation confirms this model is ready for the real world.
📁 Project Files

.
├── combine.csv           # Raw combined CICIDS2017 dataset
├── ids_training.py       # Training + evaluation script
├── ids_model.joblib      # Trained XGBoost model
├── scaler.joblib         # Feature scaler (MinMaxScaler)
├── label_encoder.joblib  # Attack label encoder
└── README.md             # This overview

⚠️ Safety First

    Only simulate attacks on your own network, local VM, or test lab.

    Never target devices or networks you don’t own.

    Use a firewall or air-gapped VM to isolate test traffic.

🧪 Attack Simulation Options
1. 🧨 DoS: Slowloris

    Tool: slowloris

    Targets: HTTP servers (can use Python's built-in HTTP server)

# Start a test web server
python -m http.server 80

# Launch slowloris (needs Python 3)
git clone https://github.com/gkbrk/slowloris
cd slowloris
python3 slowloris.py 127.0.0.1

2. 💣 DoS/DDoS & PortScan: hping3

# SYN Flood (DoS)
sudo hping3 -S -p 80 --flood 127.0.0.1

# UDP Flood
sudo hping3 --udp -p 53 --flood 127.0.0.1

# Port Scan
sudo hping3 -S -p ++20 -c 100 127.0.0.1

    📦 Install: sudo apt install hping3 (Linux)

3. 🦠 Botnet Emulation: LOIC or HOIC (Use with caution)

    Tools like LOIC are not safe to use on real networks.

    You can run them inside a VM with isolated networking to test how your IDS responds.

4. 🧪 Metasploit Framework (Advanced)

    Exploit known vulnerabilities (e.g. Heartbleed, SMB)

    Use auxiliary/scanner modules for PortScan/DDoS sim

    Requires setup of vulnerable targets (e.g., Metasploitable2)

✅ Easy Local Safe Setup (Recommended for Now)

    Spin up a Python HTTP server:

python -m http.server 80

    Run slowloris from a separate terminal/VM:

python3 slowloris.py 127.0.0.1

    Your realtime_ids.py should start detecting high-volume flows (e.g., DoS Hulk or Slowl

📝 License

MIT License — feel free to use and adapt!

## 🔍 Demo Output

![Live Prediction Screenshot](images/output.png)
![Model Training Results](images/performance.png)
![Sanity check](images/SANITYCHEACK.png)




