import xml.etree.ElementTree as ET
import pandas as pd

tree = ET.parse("cav_data.xml")
root = tree.getroot()

rows = []

for timestep in root.findall("timestep"):
    time = float(timestep.attrib["time"])
    for vehicle in timestep.findall("vehicle"):
        rows.append([
            time,
            vehicle.attrib["id"],
            float(vehicle.attrib["speed"]),
            float(vehicle.attrib["x"]),
            float(vehicle.attrib["y"])
        ])

df = pd.DataFrame(rows, columns=["time","veh_id","speed","x","y"])

df.to_csv("cav_data.csv", index=False)

print("CSV file created successfully!")
