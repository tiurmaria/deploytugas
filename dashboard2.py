import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#PERTANYAAN 1

# Load the dataset
df_aot_chang = pd.read_csv('q1.csv')

# Filter data for the 4th quarter of 2016
df_q4_2016 = df_aot_chang[
    (df_aot_chang['month_aot'] >= 10) & (df_aot_chang['month_aot'] <= 12) & 
    (df_aot_chang['year_aot'] == 2016)
]

# Calculate the sum of PM2.5 concentrations for each station
sum_pm25_aot = df_q4_2016['PM2.5_aot'].sum()
sum_pm25_chang = df_q4_2016['PM2.5_chang'].sum()

# Display the sums in Streamlit
st.title("Total PM2.5 Concentration in Q4 2016")
st.write("### Data Summary")
st.write(f"Total PM2.5 Concentration for Aotizhongxin: **{sum_pm25_aot}**")
st.write(f"Total PM2.5 Concentration for Changping: **{sum_pm25_chang}**")

# Create a bar chart
stations = ['Aotizhongxin', 'Changping']
sums = [sum_pm25_aot, sum_pm25_chang]

fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(stations, sums, color=['skyblue', 'lightcoral'])
ax.set_xlabel('Station')
ax.set_ylabel('Total PM2.5 Concentration')
ax.set_title('Total PM2.5 Concentration in Q4 2016')

# Add labels to the bars
for i, v in enumerate(sums):
    ax.text(i, v, str(v), ha='center', va='bottom')

# Display the chart in Streamlit
st.pyplot(fig)


#PERTANYAAN 2

# Load the dataset
df_aot_specific = pd.read_csv('q2.csv')

# Group data by year and calculate the average NO2 concentration for each year
yearly_avg_no2 = df_aot_specific.groupby('year_aot')['NO2_aot'].mean()

# Convert the index (years) to string to prevent formatting as thousands
yearly_avg_no2.index = yearly_avg_no2.index.astype(str)

# Streamlit App Title
st.title("Development of NO2 Concentration at Aotizhongxin Station Over the Years")

# Display the data summary
st.write("### Yearly Average NO2 Concentration")
st.dataframe(yearly_avg_no2.reset_index())

# Plot the development of NO2 concentration over the years
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(yearly_avg_no2.index, yearly_avg_no2.values, marker='o')
ax.set_xlabel('Year')
ax.set_ylabel('Average NO2 Concentration')
ax.set_title('Development of NO2 Concentration at Aotizhongxin Station Over the Years')
ax.grid(True)

# Display the plot in Streamlit
st.pyplot(fig)



# ANALISIS LANJUTAN
import seaborn as sns

# Load the dataset
data_aot = pd.read_csv('q3.csv')

# Define the NO2 concentration categories
def categorize_no2(value):
    if value <= 40:  # Low
        return 'Rendah'
    elif 41 <= value <= 100:  # Medium
        return 'Sedang'
    else:  # High
        return 'Tinggi'

# Add the category column to the data
data_aot['NO2_category'] = data_aot['NO2'].apply(categorize_no2)

# Filter data for years between 2013 and 2017
filtered_data = data_aot[(data_aot['year'] >= 2013) & (data_aot['year'] <= 2017)]

# Convert 'year' column to string to prevent thousand separators
filtered_data['year'] = filtered_data['year'].astype(str)

# Group the data by year and NO2 category, then calculate the average NO2
grouped_data = filtered_data.groupby(['year', 'NO2_category'])['NO2'].mean().reset_index()

# Streamlit app title
st.title("Rata-rata Konsentrasi NO2 Berdasarkan Kategori (2013–2017)")

# Display the grouped data in Streamlit
st.write("### Rata-rata Konsentrasi NO2 per Tahun dan Kategori")
st.dataframe(grouped_data)

# Create the bar plot with Seaborn
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=grouped_data, x='year', y='NO2', hue='NO2_category', palette='viridis', ax=ax)

# Add data labels on each bar
for container in ax.containers:
    ax.bar_label(container, fmt='%.2f', label_type='edge', fontsize=10, padding=2)

# Add title and labels to the plot
ax.set_title('Rata-rata Konsentrasi NO2 Berdasarkan Kategori (2013–2017)', fontsize=14)
ax.set_xlabel('Tahun', fontsize=12)
ax.set_ylabel('Rata-rata Konsentrasi NO2 (µg/m³)', fontsize=12)
ax.legend(title='Kategori NO2')
ax.grid(axis='y', linestyle='--', alpha=0.6)

# Display the plot in Streamlit
st.pyplot(fig)
