# ==============================
# Vehicle Misbehavior Detection
# Data Preprocessing & Feature Engineering
# ==============================

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

print("Loading dataset...")

# 1️⃣ Load dataset
df = pd.read_csv("cav_data_labeled.csv")

print("Initial Dataset Shape:", df.shape)
print("\nFirst 5 Rows:")
print(df.head())


# =====================================
# 2️⃣ Encode Labels (string → numeric)
# =====================================

df['label'] = df['label'].map({
    'normal': 0,
    'faulty': 1,
    'attacker': 2
})

print("\nLabel Distribution:")
print(df['label'].value_counts())


# =====================================
# 3️⃣ Sort Data (VERY IMPORTANT)
# =====================================

df = df.sort_values(by=['veh_id', 'time'])


# =====================================
# 4️⃣ Feature Engineering
# =====================================

print("\nPerforming Feature Engineering...")

# 🔹 Speed change
df['delta_speed'] = df.groupby('veh_id')['speed'].diff()

# 🔹 Position change
df['delta_x'] = df.groupby('veh_id')['x'].diff()
df['delta_y'] = df.groupby('veh_id')['y'].diff()

# 🔹 Distance moved
df['distance_moved'] = np.sqrt(df['delta_x']**2 + df['delta_y']**2)

# 🔹 Time difference
df['time_diff'] = df.groupby('veh_id')['time'].diff()

# 🔹 Physics consistency check
df['expected_distance'] = df['speed'] * df['time_diff']
df['distance_error'] = abs(df['distance_moved'] - df['expected_distance'])


# =====================================
# 5️⃣ Remove NaN (from diff())
# =====================================

df = df.dropna()

print("Dataset Shape After Feature Engineering:", df.shape)


# =====================================
# 6️⃣ Select Features for ML
# =====================================

features = [
    'speed',
    'delta_speed',
    'distance_moved',
    'time_diff',
    'distance_error'
]


# =====================================
# 7️⃣ Normalize Features
# =====================================

scaler = StandardScaler()
df[features] = scaler.fit_transform(df[features])


# =====================================
# 8️⃣ Save Processed Dataset
# =====================================

df.to_csv("processed_dataset.csv", index=False)

print("\nPreprocessing Complete ✅")
print("Processed dataset saved as: processed_dataset.csv")
print("\nNumber of Unique Vehicles:")
print(df['veh_id'].nunique())

print("\nMaximum Simulation Time:")
print(df['time'].max())