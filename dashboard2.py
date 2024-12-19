import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
df_aot_chang = pd.read_csv('q1.csv')
df_aot_specific = pd.read_csv('q2.csv')
data_aot = pd.read_csv('q3.csv')

# Header Section
st.title("Analisis Kualitas Udara")
st.write("Selamat datang! Temukan wawasan menarik dari data konsentrasi PM2.5 dan NO2 di berbagai stasiun.")

# Sidebar Section
st.sidebar.image("dicoding gambar.png", use_column_width=True)

# ==================== PERTANYAAN 1 ====================

st.header("Total Konsentrasi PM2.5 di Kuartal 4 Tahun 2016")

# Filter data untuk Kuartal 4 2016
df_q4_2016 = df_aot_chang[
    (df_aot_chang['month_aot'] >= 10) & (df_aot_chang['month_aot'] <= 12) &
    (df_aot_chang['year_aot'] == 2016)
]

# Hitung total konsentrasi PM2.5
sum_pm25_aot = df_q4_2016['PM2.5_aot'].sum()
sum_pm25_chang = df_q4_2016['PM2.5_chang'].sum()

# Tampilkan data di Streamlit
st.subheader("Ringkasan Data")
st.write(f"**Total Konsentrasi PM2.5 untuk Aotizhongxin:** {sum_pm25_aot}")
st.write(f"**Total Konsentrasi PM2.5 untuk Changping:** {sum_pm25_chang}")

# Visualisasi data
stations = ['Aotizhongxin', 'Changping']
sums = [sum_pm25_aot, sum_pm25_chang]
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(stations, sums, color=['skyblue', 'lightcoral'])
ax.set_xlabel('Stasiun', fontsize=12)
ax.set_ylabel('Total Konsentrasi PM2.5', fontsize=12)
ax.set_title('Total Konsentrasi PM2.5 di Kuartal 4 Tahun 2016', fontsize=14)

# Tambahkan label ke setiap bar
for i, v in enumerate(sums):
    ax.text(i, v, f'{v:.0f}', ha='center', va='bottom')

st.pyplot(fig)

with st.expander("Penjelasan Grafik"):
    st.write(
        'Grafik di atas menunjukkan total konsentrasi PM2.5 di dua stasiun, yaitu Aotizhongxin dan Changping, selama kuartal ke-4 tahun 2016 (Q4 2016). '
        'Stasiun Aotizhongxin memiliki total konsentrasi PM2.5 yang lebih tinggi (229486) dibandingkan dengan Changping (198509).')


# ==================== PERTANYAAN 2 ====================

st.header("Perkembangan Konsentrasi NO2 di Stasiun Aotizhongxin")

# Tambahkan filter berdasarkan tahun
selected_year = st.sidebar.slider("Pilih Tahun", min_value=int(df_aot_specific['year_aot'].min()), max_value=int(df_aot_specific['year_aot'].max()), value=(int(df_aot_specific['year_aot'].min()), int(df_aot_specific['year_aot'].max())))
filtered_df_aot_specific = df_aot_specific[(df_aot_specific['year_aot'] >= selected_year[0]) & (df_aot_specific['year_aot'] <= selected_year[1])]

# Tambahkan pilihan kategori konsentrasi NO2
no2_category = st.sidebar.radio("Pilih Kategori Konsentrasi NO2:", ('Rendah', 'Sedang', 'Tinggi'))

# Filter data berdasarkan kategori NO2
def filter_no2_category(row):
    if no2_category == 'Rendah':
        return row['NO2_aot'] <= 40
    elif no2_category == 'Sedang':
        return 41 <= row['NO2_aot'] <= 100
    else:
        return row['NO2_aot'] > 100

filtered_df_aot_specific = filtered_df_aot_specific[filtered_df_aot_specific.apply(filter_no2_category, axis=1)]

# Rata-rata konsentrasi NO2 per tahun
yearly_avg_no2 = filtered_df_aot_specific.groupby('year_aot')['NO2_aot'].mean()
yearly_avg_no2.index = yearly_avg_no2.index.astype(str)

st.subheader("Rata-rata Konsentrasi NO2 Tiap Tahun")
st.dataframe(yearly_avg_no2.reset_index(), use_container_width=True)

# Visualisasi tren konsentrasi NO2
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(yearly_avg_no2.index, yearly_avg_no2.values, marker='o', color='orange')
ax.set_xlabel('Tahun', fontsize=12)
ax.set_ylabel('Rata-rata Konsentrasi NO2 (µg/m³)', fontsize=12)
ax.set_title('Perkembangan Konsentrasi NO2 di Aotizhongxin', fontsize=14)
ax.grid(True)

st.pyplot(fig)

# Penjelasan tambahan
st.write("Pada grafik di atas, Anda dapat melihat bagaimana rata-rata konsentrasi NO2 di Stasiun Aotizhongxin berubah dari tahun ke tahun, difilter berdasarkan kategori pilihan.")

# ==================== ANALISIS LANJUTAN ====================

st.header("Konsentrasi NO2 Berdasarkan Kategori (2013–2017)")

# Kategorisasi konsentrasi NO2
def categorize_no2(value):
    if value <= 40:
        return 'Rendah'
    elif 41 <= value <= 100:
        return 'Sedang'
    else:
        return 'Tinggi'

data_aot['NO2_category'] = data_aot['NO2'].apply(categorize_no2)

# Filter data untuk tahun 2013-2017
filtered_data = data_aot[(data_aot['year'] >= 2013) & (data_aot['year'] <= 2017)]
filtered_data['year'] = filtered_data['year'].astype(str)

# Rata-rata per kategori per tahun
grouped_data = filtered_data.groupby(['year', 'NO2_category'])['NO2'].mean().reset_index()

st.subheader("Rata-rata Konsentrasi NO2 per Tahun dan Kategori")
st.dataframe(grouped_data, use_container_width=True)

# Visualisasi dengan Seaborn
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=grouped_data, x='year', y='NO2', hue='NO2_category', palette='viridis', ax=ax)

# Tambahkan label ke setiap bar
for container in ax.containers:
    ax.bar_label(container, fmt='%.2f', label_type='edge', fontsize=10, padding=2)

ax.set_title('Rata-rata Konsentrasi NO2 Berdasarkan Kategori (2013–2017)', fontsize=14)
ax.set_xlabel('Tahun', fontsize=12)
ax.set_ylabel('Rata-rata Konsentrasi NO2 (µg/m³)', fontsize=12)
ax.legend(title='Kategori NO2')
ax.grid(axis='y', linestyle='--', alpha=0.6)

st.pyplot(fig)

with st.expander("Penjelasan Grafik"):
    st.write(
        'Konsentrasi NO2 terendah ada pada tahun 2017 yaitu sebesar 20.36 µg/m³. '
        'Konsentrasi NO2 tertinggi ada pada tahun 2017 yaitu sebesar 130.16 µg/m³.')

