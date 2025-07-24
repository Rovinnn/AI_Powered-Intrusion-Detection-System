

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
import joblib
from collections import Counter
import copy

# === Load Dataset ===
print("Loading dataset...")
df = pd.read_csv("combine.csv", low_memory=False)
print("Original shape:", df.shape)

# === Identify label column ===
label_candidates = ['Label', 'label', 'LABEL', 'class', 'Class', 'CLASS', 'target', 'Target', 'TARGET']
label_col = next((c for c in label_candidates if c in df.columns), df.columns[-1])
print(f"Label column detected: {label_col}")

# === Drop potential leak columns ===
leak_cols = ['src_ip', 'dst_ip', 'src_mac', 'dst_mac', 'flow_id', 'id', 'timestamp', 'start_time', 'end_time']
df.drop(columns=[c for c in leak_cols if c in df.columns], inplace=True, errors='ignore')

# === Keep only final supported features ===
supported_features = [
    'Destination Port',
    'Flow Duration',
    'Total Fwd Packets',
    'Total Backward Packets',
    'Total Length of Fwd Packets',
    'Total Length of Bwd Packets',
    'Fwd Packet Length Max',
    'Bwd Packet Length Max',
    'Flow Bytes/s',
    'Flow Packets/s'
]

# Drop any extra features
X = df.drop(columns=[label_col])
X = X[supported_features]  # Ensure only supported features used
y = df[label_col]

# === Clean data ===
X.replace([np.inf, -np.inf], np.nan, inplace=True)
X.dropna(inplace=True)
y = y.loc[X.index]

# === Label encoding ===
y = y.replace({'Heartbleed': 'RareAttack', 'Infiltration': 'RareAttack'})
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# === Split before SMOTE ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# === Scale ===
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# === Apply SMOTE ===
target_count = 10000
smote_strategy = {cls: target_count for cls, count in Counter(y_train).items() if count < target_count}
smote = SMOTE(random_state=42, sampling_strategy=smote_strategy)
X_train_res, y_train_res = smote.fit_resample(X_train_scaled, y_train)

# === Train Model ===
clf = XGBClassifier(eval_metric='mlogloss', verbosity=1, random_state=42)
clf.fit(X_train_res, y_train_res)

# === Evaluate ===
y_pred = clf.predict(X_test_scaled)
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# === Cross-validation ===
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(clf, scaler.transform(X), y_encoded, cv=skf, scoring='f1_weighted')
print(f"\nCross-validated F1 scores: {cv_scores}")
print(f"Mean CV F1: {cv_scores.mean():.4f}")

# === Sanity Check ===
y_shuffled = copy.deepcopy(y_encoded)
np.random.shuffle(y_shuffled)
X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(
    X, y_shuffled, test_size=0.2, random_state=42, stratify=y_shuffled
)
X_train_s_scaled = scaler.fit_transform(X_train_s)
X_test_s_scaled = scaler.transform(X_test_s)
clf_sanity = XGBClassifier(eval_metric='mlogloss', verbosity=0, random_state=42)
clf_sanity.fit(X_train_s_scaled, y_train_s)
y_pred_s = clf_sanity.predict(X_test_s_scaled)
print("\nSanity check classification report (should be poor):")
print(classification_report(y_test_s, y_pred_s))

# === Save Artifacts ===
joblib.dump(clf, "ids_model_realtime.joblib")
joblib.dump(scaler, "scaler_realtime.joblib")
joblib.dump(le, "label_encoder_realtime.joblib")
print("\n✅ Model and preprocessing saved.")
