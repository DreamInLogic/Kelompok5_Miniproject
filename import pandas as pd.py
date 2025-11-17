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


