import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the Excel file
file_path = 'data jumlah curah hujan maksimum per bulan berdasarkan stasiun v1.xlsx'
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
