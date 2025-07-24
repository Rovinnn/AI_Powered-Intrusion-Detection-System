import joblib
from nfstream import NFStreamer
import time
import pandas as pd
import numpy as np
import multiprocessing

def main():
    print("\n🔍 Real-time IDS started. Monitoring flows...")

    # === Load model and artifacts ===
    model = joblib.load("ids_model_realtime.joblib")
    scaler = joblib.load("scaler_realtime.joblib")
    le = joblib.load("label_encoder_realtime.joblib")

    # === Safe division helper ===
    def safe_div(a, b):
        return a / b if b else 0

    # === Streamer ===
    streamer = NFStreamer(source=r"\\Device\\NPF_{YOUR_DEVICE_GUID}", statistical_analysis=True)

    for flow in streamer:
        try:
            row = {
                'Destination Port': flow.dst_port,
                'Flow Duration': flow.bidirectional_duration_ms,
                'Total Fwd Packets': flow.src2dst_packets,
                'Total Backward Packets': flow.dst2src_packets,
                'Total Length of Fwd Packets': flow.src2dst_bytes,
                'Total Length of Bwd Packets': flow.dst2src_bytes,
                'Fwd Packet Length Max': flow.src2dst_max_ps,
                'Bwd Packet Length Max': flow.dst2src_max_ps,
                'Flow Bytes/s': safe_div(flow.bidirectional_bytes, flow.bidirectional_duration_ms / 1000),
                'Flow Packets/s': safe_div(flow.bidirectional_packets, flow.bidirectional_duration_ms / 1000),
            }

            df = pd.DataFrame([row])
            df_scaled = scaler.transform(df)
            pred = model.predict(df_scaled)[0]
            label = le.inverse_transform([pred])[0]

            print(f"[+] Flow detected ➜ Predicted label: {label}")

        except Exception as e:
            print(f"[!] Error: {e}")

        time.sleep(0.1)  # slight delay to avoid spamming predictions

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
