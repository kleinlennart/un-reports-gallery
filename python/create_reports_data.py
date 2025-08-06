from pathlib import Path

import pandas as pd

data_folder = Path("data")
input_path = data_folder / "input" / "entities.csv"
df = pd.read_csv(input_path)

df = df[["entity", "entity_long", "annual_report_link"]]


all_paths = list(Path("docs").glob("**/*.pdf"))

# Create a dictionary to map entity names to their matched paths
entity_to_path = {}

for path in all_paths:
    entity_name = path.stem.split("_")[0]  # Extract the part before the first '_'
    if entity_name in df["entity"].values:  # Match with the 'entity' column in the DataFrame
        entity_to_path[entity_name] = str(path)  # Store the path as a string

# Add a new column to the DataFrame with the matched paths
df["pdf_path"] = df["entity"].map(entity_to_path)

