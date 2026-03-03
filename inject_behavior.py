import pandas as pd
import numpy as np

df = pd.read_csv("cav_data.csv")

df["label"] = "normal"

# Get all unique vehicle IDs
unique_ids = df["veh_id"].unique()

total_vehicles = len(unique_ids)

# Define percentage (15% faulty, 15% attacker)
num_faulty = int(0.15 * total_vehicles)
num_attacker = int(0.15 * total_vehicles)

# Select vehicles
faulty_ids = unique_ids[:num_faulty]
attacker_ids = unique_ids[num_faulty:num_faulty + num_attacker]

# Inject faulty behavior (small speed noise)
df.loc[df["veh_id"].isin(faulty_ids), "speed"] += np.random.normal(
    0, 5, size=len(df.loc[df["veh_id"].isin(faulty_ids)])
)

df.loc[df["veh_id"].isin(faulty_ids), "label"] = "faulty"

# Inject attacker behavior (high speed + GPS jump)
df.loc[df["veh_id"].isin(attacker_ids), "speed"] = 180
df.loc[df["veh_id"].isin(attacker_ids), ["x", "y"]] += 300
df.loc[df["veh_id"].isin(attacker_ids), "label"] = "attacker"


df.to_csv("cav_data_labeled.csv", index=False)
