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
