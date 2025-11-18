
import pandas as pd
import numpy as np

# Define the path to the uploaded Excel file
file_path = 'data jumlah curah hujan maksimum per bulan berdasarkan stasiun v1.xlsx'

# --- 1. Load and Prepare Data ---
try:
    # Read the Excel file. Assuming the data is in the first sheet.
    df = pd.read_excel(file_path)
except Exception as e:
    print(f"Error reading Excel file: {e}")
    exit()

# Rename columns for easier access
df.columns = ['No', 'Kode Provinsi', 'Nama Provinsi', 'Nama Pos Hujan', 'Nama Stasiun Hujan', 'Bulan', 'Jumlah Curah Hujan', 'Satuan', 'Tahun']

# Convert 'Jumlah Curah Hujan' to numeric, coercing errors to NaN
df['Jumlah Curah Hujan'] = pd.to_numeric(df['Jumlah Curah Hujan'], errors='coerce')

# Filter data for the required years (2020-2024)
df_filtered = df[(df['Tahun'] >= 2020) & (df['Tahun'] <= 2024)].copy()

# Drop rows with missing rainfall data
df_filtered.dropna(subset=['Jumlah Curah Hujan'], inplace=True)

# --- 2. Calculate Annual Total Rainfall and Max Month per Station per Year ---

# Group by Station and Year to get the annual total and the month with max rainfall
annual_summary = df_filtered.groupby(['Nama Stasiun Hujan', 'Tahun']).agg(
    Total_Curah_Hujan=('Jumlah Curah Hujan', 'sum'),
    Max_Curah_Hujan=('Jumlah Curah Hujan', 'max')
).reset_index()

# Merge back to find the month corresponding to the Max_Curah_Hujan
# This is a bit tricky, so we'll use a function to find the month
def get_max_month(group):
    max_rainfall = group['Jumlah Curah Hujan'].max()
    # Get the month(s) with the maximum rainfall. If multiple, take the first one.
    max_month = group[group['Jumlah Curah Hujan'] == max_rainfall]['Bulan'].iloc[0]
    return max_month

# Apply the function to get the month of maximum rainfall
max_month_df = df_filtered.groupby(['Nama Stasiun Hujan', 'Tahun']).apply(get_max_month).reset_index(name='Bulan_Max_Curah_Hujan')

# Merge the max month back into the annual summary
annual_summary = pd.merge(annual_summary, max_month_df, on=['Nama Stasiun Hujan', 'Tahun'])
def classify_rainfall(total_rainfall):
    if total_rainfall > 2500:
        return 'Tinggi'
    elif total_rainfall >= 1500:
        return 'Sedang'
    else:
        return 'Rendah'

annual_summary['Klasifikasi_Curah_Hujan'] = annual_summary['Total_Curah_Hujan'].apply(classify_rainfall)

# Select and reorder columns for the first request
classification_result = annual_summary[['Nama Stasiun Hujan', 'Tahun', 'Klasifikasi_Curah_Hujan', 'Bulan_Max_Curah_Hujan', 'Total_Curah_Hujan']]
classification_result.rename(columns={'Total_Curah_Hujan': 'Total Curah Hujan Tahunan (mm)'}, inplace=True)


# --- 4. Calculate Average Annual Rainfall per Station (2020-2024) ---

# Group the annual summary by station to calculate the average annual total
average_annual_rainfall = classification_result.groupby('Nama Stasiun Hujan')['Total Curah Hujan Tahunan (mm)'].mean().reset_index(name='Rata-rata Curah Hujan Tahunan (mm)')

# Round the average to 2 decimal places
average_annual_rainfall['Rata-rata Curah Hujan Tahunan (mm)'] = average_annual_rainfall['Rata-rata Curah Hujan Tahunan (mm)'].round(2)
# --- 5. Save Results to Excel Files ---

# Save the classification result to Excel
classification_result.to_excel('klasifikasi_curah_hujan.xlsx', index=False)

# Save the average annual rainfall result to Excel
average_annual_rainfall.to_excel('rata_rata_curah_hujan.xlsx', index=False)

print("Analysis complete. Results saved to klasifikasi_curah_hujan.xlsx and rata_rata_curah_hujan.xlsx")

# --- 6. Create Bar Chart with Random Colors for Rainfall Classification ---
import matplotlib.pyplot as plt
import numpy as np
import random

# Load the classification data
try:
    df_chart = pd.read_excel('klasifikasi_curah_hujan.xlsx')
except Exception as e:
    print(f"Error reading classification file: {e}")
    exit()

# Create a combined label for station and year
df_chart['Station_Year'] = df_chart['Nama Stasiun Hujan'] + ' (' + df_chart['Tahun'].astype(str) + ')'

# Create figure and axis
plt.figure(figsize=(12, 10))

# Generate random colors for each bar
colors = []
for _ in range(len(df_chart)):
    r = random.random()
    g = random.random()
    b = random.random()
    colors.append((r, g, b))

# Create horizontal bar chart
bars = plt.barh(range(len(df_chart)), df_chart['Total Curah Hujan Tahunan (mm)'], color=colors)

# Customize the chart
plt.title('Klasifikasi Curah Hujan per Stasiun per Tahun', fontsize=16, fontweight='bold')
plt.xlabel('Total Curah Hujan Tahunan (mm)', fontsize=12)
plt.ylabel('Stasiun dan Tahun', fontsize=12)

# Set y-axis labels with station names and years
plt.yticks(range(len(df_chart)), df_chart['Station_Year'])

# Add classification labels and month information at the end of each bar
for i, bar in enumerate(bars):
    width = bar.get_width()
    classification = df_chart.iloc[i]['Klasifikasi_Curah_Hujan']
    month = df_chart.iloc[i]['Bulan_Max_Curah_Hujan']
    rainfall_value = df_chart.iloc[i]['Total Curah Hujan Tahunan (mm)']
    
    # Add classification text with more specific rainfall information
    plt.text(width + 20, bar.get_y() + bar.get_height()/2.,
             f'{classification}\n{rainfall_value:.1f} mm\n({month})',
             ha='left', va='center', fontsize=8, fontweight='bold')

# Add grid for better readability
plt.grid(axis='x', alpha=0.3)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save the chart
plt.savefig('diagram_batang_klasifikasi_curah_hujan.png', dpi=300, bbox_inches='tight')
plt.show()

print("Bar chart saved as 'diagram_batang_klasifikasi_curah_hujan.png'")

import pandas as pd
import numpy as np

# Define the path to the uploaded Excel file
file_path = 'data jumlah curah hujan maksimum per bulan berdasarkan stasiun v1.xlsx'

# --- 1. Load and Prepare Data ---
try:
    # Read the Excel file. Assuming the data is in the first sheet.
    df = pd.read_excel(file_path)
except Exception as e:
    print(f"Error reading Excel file: {e}")
    exit()

# Rename columns for easier access
df.columns = ['No', 'Kode Provinsi', 'Nama Provinsi', 'Nama Pos Hujan', 'Nama Stasiun Hujan', 'Bulan', 'Jumlah Curah Hujan', 'Satuan', 'Tahun']

# Convert 'Jumlah Curah Hujan' to numeric, coercing errors to NaN
df['Jumlah Curah Hujan'] = pd.to_numeric(df['Jumlah Curah Hujan'], errors='coerce')

# Filter data for the required years (2020-2024)
df_filtered = df[(df['Tahun'] >= 2020) & (df['Tahun'] <= 2024)].copy()

# Drop rows with missing rainfall data
df_filtered.dropna(subset=['Jumlah Curah Hujan'], inplace=True)

# --- 2. Calculate Annual Total Rainfall and Max Month per Station per Year ---

# Group by Station and Year to get the annual total and the month with max rainfall
annual_summary = df_filtered.groupby(['Nama Stasiun Hujan', 'Tahun']).agg(
    Total_Curah_Hujan=('Jumlah Curah Hujan', 'sum'),
    Max_Curah_Hujan=('Jumlah Curah Hujan', 'max')
).reset_index()

# Merge back to find the month corresponding to the Max_Curah_Hujan
# This is a bit tricky, so we'll use a function to find the month
def get_max_month(group):
    max_rainfall = group['Jumlah Curah Hujan'].max()
    # Get the month(s) with the maximum rainfall. If multiple, take the first one.
    max_month = group[group['Jumlah Curah Hujan'] == max_rainfall]['Bulan'].iloc[0]
    return max_month

# Apply the function to get the month of maximum rainfall
max_month_df = df_filtered.groupby(['Nama Stasiun Hujan', 'Tahun']).apply(get_max_month).reset_index(name='Bulan_Max_Curah_Hujan')

# Merge the max month back into the annual summary
annual_summary = pd.merge(annual_summary, max_month_df, on=['Nama Stasiun Hujan', 'Tahun'])
def classify_rainfall(total_rainfall):
    if total_rainfall > 2500:
        return 'Tinggi'
    elif total_rainfall >= 1500:
        return 'Sedang'
    else:
        return 'Rendah'

annual_summary['Klasifikasi_Curah_Hujan'] = annual_summary['Total_Curah_Hujan'].apply(classify_rainfall)

# Select and reorder columns for the first request
classification_result = annual_summary[['Nama Stasiun Hujan', 'Tahun', 'Klasifikasi_Curah_Hujan', 'Bulan_Max_Curah_Hujan', 'Total_Curah_Hujan']]
classification_result.rename(columns={'Total_Curah_Hujan': 'Total Curah Hujan Tahunan (mm)'}, inplace=True)


# --- 4. Calculate Average Annual Rainfall per Station (2020-2024) ---

# Group the annual summary by station to calculate the average annual total
average_annual_rainfall = classification_result.groupby('Nama Stasiun Hujan')['Total Curah Hujan Tahunan (mm)'].mean().reset_index(name='Rata-rata Curah Hujan Tahunan (mm)')

# Round the average to 2 decimal places
average_annual_rainfall['Rata-rata Curah Hujan Tahunan (mm)'] = average_annual_rainfall['Rata-rata Curah Hujan Tahunan (mm)'].round(2)
# --- 5. Save Results to Excel Files ---

# Save the classification result to Excel
classification_result.to_excel('klasifikasi_curah_hujan.xlsx', index=False)

# Save the average annual rainfall result to Excel
average_annual_rainfall.to_excel('rata_rata_curah_hujan.xlsx', index=False)

print("Analysis complete. Results saved to klasifikasi_curah_hujan.xlsx and rata_rata_curah_hujan.xlsx")



