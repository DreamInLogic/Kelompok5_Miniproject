
import pandas as pd
import numpy as np

# Define the path to the uploaded Excel file
file_path = 'Data Jumlah curah hujan UPDATE.xlsx'

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
file_path = 'Data Jumlah curah hujan UPDATE.xlsx'

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

#diagram rata rata curah hujan
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

# diagram curah hujan tertinggi
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Membaca data dari file Excel
file_path = 'Data Jumlah curah hujan UPDATE.xlsx'
df = pd.read_excel(file_path)

# Membersihkan data - menghapus baris dengan nilai curah hujan kosong
df = df.dropna(subset=['Jumlah Curah Hujan'])

# Mengelompokkan data berdasarkan stasiun dan mencari nilai curah hujan tertinggi
max_curah_hujan = df.groupby('Nama Stasiun Hujan')['Jumlah Curah Hujan'].max().reset_index()

# Mencari tahun dan bulan ketika curah hujan tertinggi terjadi untuk setiap stasiun
info_max = []
for stasiun in max_curah_hujan['Nama Stasiun Hujan']:
    data_stasiun = df[df['Nama Stasiun Hujan'] == stasiun]
    max_value = data_stasiun['Jumlah Curah Hujan'].max()
    max_data = data_stasiun[data_stasiun['Jumlah Curah Hujan'] == max_value].iloc[0]
    info_max.append({
        'Stasiun': stasiun,
        'Curah Hujan Tertinggi': max_value,
        'Tahun': max_data['Tahun'],
        'Bulan': max_data['Bulan']
    })

# Membuat DataFrame dari informasi maksimum
df_max_info = pd.DataFrame(info_max)

# Mengurutkan data berdasarkan curah hujan tertinggi
df_max_info = df_max_info.sort_values('Curah Hujan Tertinggi', ascending=False)

# Membuat diagram batang
plt.figure(figsize=(12, 8))
bars = plt.bar(df_max_info['Stasiun'], df_max_info['Curah Hujan Tertinggi'], 
               color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])

# Menambahkan label nilai di atas setiap batang
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.1f} mm',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

# Menambahkan judul dan label
plt.title('Curah Hujan Tertinggi Setiap Stasiun (2015-2024)', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Stasiun Hujan', fontsize=12)
plt.ylabel('Curah Hujan (mm)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)

# Menyesuaikan layout
plt.tight_layout()

# Menyimpan diagram
plt.savefig('diagram_batang_curah_hujan_tertinggi.png', dpi=300, bbox_inches='tight')
plt.show()

# Menyimpan hasil ke file Excel
with pd.ExcelWriter('curah_hujan_tertinggi_per_stasiun.xlsx', engine='openpyxl') as writer:
    df_max_info.to_excel(writer, sheet_name='Curah Hujan Tertinggi', index=False)
    
    # Menambahkan sheet detail data untuk referensi
    df.to_excel(writer, sheet_name='Data Lengkap', index=False)

print("Analisis curah hujan tertinggi per stasiun telah selesai!")
print(f"Diagram batang disimpan sebagai: diagram_batang_curah_hujan_tertinggi.png")
print(f"Hasil analisis disimpan sebagai: curah_hujan_tertinggi_per_stasiun.xlsx")
print("\nRingkasan Curah Hujan Tertinggi per Stasiun:")
print(df_max_info.to_string(index=False))

# diagram pie persebtasi cyrah ujan
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the Excel file
file_path = 'Data Jumlah curah hujan UPDATE.xlsx'
df = pd.read_excel(file_path)

# Clean the data - remove rows with missing rainfall values
df = df.dropna(subset=['Jumlah Curah Hujan'])

# Group by station and calculate total rainfall
station_totals = df.groupby('Nama Stasiun Hujan')['Jumlah Curah Hujan'].sum()

# Calculate percentages
total_rainfall = station_totals.sum()
percentages = (station_totals / total_rainfall * 100).round(2)

# Create pie chart
plt.figure(figsize=(12, 8))
colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99']

# Create pie chart with percentages
wedges, texts, autotexts = plt.pie(percentages, 
                                   labels=station_totals.index, 
                                   colors=colors,
                                   autopct='%1.1f%%',
                                   startangle=90,
                                   textprops={'fontsize': 12})

# Enhance the appearance
plt.title('Persentase Total Curah Hujan per Stasiun (2015-2024)', 
          fontsize=16, fontweight='bold', pad=20)

# Add total rainfall information
total_text = f'Total Curah Hujan: {total_rainfall:.1f} mm'
plt.figtext(0.5, 0.02, total_text, ha='center', fontsize=12, fontweight='bold')

# Create a legend with rainfall amounts
legend_labels = [f'{station}: {rainfall:.1f} mm ({pct:.1f}%)' 
                 for station, rainfall, pct in zip(station_totals.index, station_totals, percentages)]
plt.legend(wedges, legend_labels, title="Stasiun", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

# Adjust layout to prevent legend cutoff
plt.tight_layout()

# Save the chart
plt.savefig('diagram_pie_persentase_curah_hujan.png', dpi=300, bbox_inches='tight')

# Show the chart
plt.show()

# Print the analysis results
print("ANALISIS DATA CURAH HUJAN PER STASIUN (2015-2024)")
print("=" * 50)
print(f"{'Stasiun':<20} {'Total (mm)':<15} {'Persentase':<10}")
print("-" * 50)
for station, total, pct in zip(station_totals.index, station_totals, percentages):
    print(f"{station:<20} {total:<15.1f} {pct:<10.1f}%")
print("-" * 50)
print(f"{'TOTAL':<20} {total_rainfall:<15.1f} {'100.0%':<10}")

# Find the station with highest rainfall
max_station = station_totals.idxmax()
max_rainfall = station_totals.max()
max_percentage = percentages[max_station]

print(f"\nStasiun dengan curah hujan tertinggi: {max_station}")
print(f"Total curah hujan: {max_rainfall:.1f} mm ({max_percentage:.1f}%)")

# Simpan dalam file Excel
# Create a summary DataFrame
summary_df = pd.DataFrame({
    'Nama Stasiun': station_totals.index,
    'Total Curah Hujan (mm)': station_totals.values,
    'Persentase (%)': percentages.values
})

# Sort by total rainfall (descending)
summary_df = summary_df.sort_values('Total Curah Hujan (mm)', ascending=False)

# Add ranking
summary_df['Peringkat'] = range(1, len(summary_df) + 1)

# Reorder columns
summary_df = summary_df[['Peringkat', 'Nama Stasiun', 'Total Curah Hujan (mm)', 'Persentase (%)']]

# Add total row
total_row = pd.DataFrame({
    'Peringkat': [''],
    'Nama Stasiun': ['TOTAL'],
    'Total Curah Hujan (mm)': [total_rainfall],
    'Persentase (%)': [100.0]
})

summary_df = pd.concat([summary_df, total_row], ignore_index=True)

# Save to Excel
output_file = 'persentase_curah_hujan_per_stasiun.xlsx'
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    summary_df.to_excel(writer, sheet_name='Persentase per Stasiun', index=False)
    
    # Get the workbook and worksheet for formatting
    workbook = writer.book
    worksheet = writer.sheets['Persentase per Stasiun']
    
    # Adjust column widths
    worksheet.column_dimensions['A'].width = 10  # Peringkat
    worksheet.column_dimensions['B'].width = 20  # Nama Stasiun
    worksheet.column_dimensions['C'].width = 20  # Total Curah Hujan
    worksheet.column_dimensions['D'].width = 15  # Persentase

print(f"\nData telah disimpan dalam file Excel: {output_file}")
