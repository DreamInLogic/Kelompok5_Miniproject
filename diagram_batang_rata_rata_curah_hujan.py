import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

# Load the average rainfall data
try:
    df_avg = pd.read_excel('rata_rata_curah_hujan.xlsx')
except Exception as e:
    print(f"Error reading average rainfall file: {e}")
    exit()

# Create figure and axis
plt.figure(figsize=(10, 8))

# Generate random colors for each bar
colors = []
for _ in range(len(df_avg)):
    r = random.random()
    g = random.random()
    b = random.random()
    colors.append((r, g, b))

# Create vertical bar chart
bars = plt.bar(df_avg['Nama Stasiun Hujan'], df_avg['Rata-rata Curah Hujan Tahunan (mm)'], color=colors)

# Customize the chart
plt.title('Rata-rata Curah Hujan Tahunan per Stasiun (2020-2024)', fontsize=16, fontweight='bold')
plt.xlabel('Nama Stasiun Hujan', fontsize=12)
plt.ylabel('Rata-rata Curah Hujan Tahunan (mm)', fontsize=12)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Add value labels on top of each bar
for i, bar in enumerate(bars):
    height = bar.get_height()
    rainfall_value = df_avg.iloc[i]['Rata-rata Curah Hujan Tahunan (mm)']
    
    # Add rainfall value text on top of each bar
    plt.text(bar.get_x() + bar.get_width()/2., height + 10,
             f'{rainfall_value:.2f} mm',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

# Add grid for better readability
plt.grid(axis='y', alpha=0.3)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save the chart
plt.savefig('diagram_batang_rata_rata_curah_hujan.png', dpi=300, bbox_inches='tight')
plt.show()

print("Bar chart for average rainfall saved as 'diagram_batang_rata_rata_curah_hujan.png'")