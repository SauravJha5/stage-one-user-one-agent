import os
import json
import csv

print("=== 1. CHECKING DIRECTORIES ===")
required_folders = ["data", "config", "replay", "simulator", "pilot"]
for folder in required_folders:
    if os.path.exists(folder):
        print(f" Folder '{folder}': {os.listdir(folder)}")
    else:
        print(f"❌ Missing: {folder}")

print("\n=== 2. CHECKING GOALS (config/goals.json) ===")
if os.path.exists("config/goals.json"):
    with open("config/goals.json", "r", encoding="utf-8") as f:
        goals = json.load(f)
        print(f"Total Goals: {len(goals)}")
        for g in goals[:3]:
            print(f" - ID: {g.get('id')}, Window: {g.get('window_days')}d, Success: {g.get('success_event') or g.get('success_condition')}")

print("\n=== 3. CHECKING ARMS (replay/arms.csv) ===")
if os.path.exists("replay/arms.csv"):
    with open("replay/arms.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        print(f"Total Viewers: {len(rows)}")
        sample_arms = {r['viewer_id']: r.get('arm') for r in rows[:3]}
        print(f"Sample arms: {sample_arms}")

print("\n=== 4. CHECKING CATALOGUE HEADERS (data/catalogue.csv) ===")
if os.path.exists("data/catalogue.csv"):
    with open("data/catalogue.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        print(f"Catalogue Columns: {header}")
