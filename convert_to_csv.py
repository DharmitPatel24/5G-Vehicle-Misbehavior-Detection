import xml.etree.ElementTree as ET
import pandas as pd
import random

# Total vehicles in simulation
TOTAL_VEHICLES = 500

# Number of autonomous vehicles (CAV)
CAV_VEHICLES = 300

# Fix random seed for reproducibility
random.seed(42)

# Generate vehicle ID list
all_vehicle_ids = list(range(TOTAL_VEHICLES))

# Randomly select 300 CAV vehicles
cav_vehicle_ids = set(random.sample(all_vehicle_ids, CAV_VEHICLES))

# Load SUMO XML output
tree = ET.parse("cav_data.xml")
root = tree.getroot()

rows = []

# Iterate through simulation timesteps
for timestep in root.findall("timestep"):
    time = float(timestep.attrib["time"])

    for vehicle in timestep.findall("vehicle"):
        veh_id = int(vehicle.attrib["id"])

        # Only keep autonomous vehicles
        if veh_id in cav_vehicle_ids:
            rows.append([
                time,
                veh_id,
                float(vehicle.attrib["speed"]),
                float(vehicle.attrib["x"]),
                float(vehicle.attrib["y"])
            ])

# Convert to DataFrame
df = pd.DataFrame(rows, columns=["time", "veh_id", "speed", "x", "y"])

# Save CSV
df.to_csv("cav_data.csv", index=False)

print("CSV file created successfully!")
print("Total vehicles in simulation:", TOTAL_VEHICLES)
print("Autonomous vehicles (CAV):", CAV_VEHICLES)
print("Normal vehicles:", TOTAL_VEHICLES - CAV_VEHICLES)
print("Only CAV vehicles exported to dataset.")