# trial_codespaces.py

import subprocess
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

# --- Step 0: Install packages if missing ---
required_packages = ["pandas", "matplotlib"]
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# --- Step 1: Load CSV ---
filename = "yourfile.csv"  # Replace with your actual CSV
if not os.path.exists(filename):
    raise FileNotFoundError(f"CSV file not found: {filename}")

df = pd.read_csv(filename)

# --- Step 2: Clean and process columns ---
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

possible_name_cols = [c for c in df.columns if "account" in c and "name" in c]
possible_count_cols = [c for c in df.columns if "member" in c and "count" in c]

if not possible_name_cols or not possible_count_cols:
    raise ValueError("❌ CSV must contain 'Account Name' and 'Member Count' columns.")

account_col = possible_name_cols[0]
count_col = possible_count_cols[0]

df[count_col] = pd.to_numeric(df[count_col], errors="coerce")
df = df.sort_values(by=count_col, ascending=False)

# --- Step 3: Plot chart ---
plt.figure(figsize=(10, 6))
bars = plt.bar(df[account_col], df[count_col], color="#1f77b4")

for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=10)

plt.title("Active Member Count by Account", fontsize=14, fontweight="bold")
plt.xlabel("Account Name", fontsize=12)
plt.ylabel("Member Count", fontsize=12)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# --- Step 4: Save plot ---
output_file = "active_members_plot.png"
plt.savefig(output_file)
print(f"✅ Plot saved as {output_file}")

# --- Done ---
print("✅ Open the PNG file in VS Code explorer to preview the chart.")
