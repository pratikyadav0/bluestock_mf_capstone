import pandas as pd
import os

print("DATA INGESTION STARTED")

data_path = "data/raw"

files = os.listdir(data_path)

dfs = {}

for file in files:
    path = os.path.join(data_path, file)
    dfs[file] = pd.read_csv(path)
    print(f"Loaded: {file} -> shape {dfs[file].shape}")

print("\nTOTAL FILES LOADED:", len(dfs))