import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Fungsi untuk memuat data
def load_data():
    wanliu_df = pd.read_csv("https://raw.githubusercontent.com/puanbening/airquality/main/dashboard/Air-quality-dataset/PRSA_Data_20130301-20170228/PRSA_Data_Wanliu_20130301-20170228.csv")
    return wanliu_df

# Fungsi utama untuk dashboard
def dashboard():
    st.header("Wanliu Station - Air Quality Dashboard ☁️ ")
    st.markdown("""#### Selamat datang di dashboard kualitas udara Stasiun Wanliu. 
        Di sini, Anda dapat menemukan informasi mengenai rata-rata suhu, kadar polutan, dan hubungan antar keduanya dari tahun 2013 hingga 2017.""")
    
    wanliu_df = load_data()

    # Visualisasi Rata-rata Suhu Tahunan
    st.subheader("Rata-rata Suhu Tahunan")
    temp_yearly = wanliu_df[wanliu_df['year'].between(2013, 2017)].groupby('year').agg({'TEMP': 'mean'}).reset_index()
    temp_yearly.rename(columns={"year": "Tahun", "TEMP": "Rata-rata Suhu (°C)"}, inplace=True)
    temp_yearly['Rata-rata Suhu (°C)'] = temp_yearly['Rata-rata Suhu (°C)'].astype(float).apply(lambda x: f"{x:.1f}")

    # Menghitung suhu terendah dan tertinggi
    lowest_temp = temp_yearly['Rata-rata Suhu (°C)'].astype(float).min()
    highest_temp = temp_yearly['Rata-rata Suhu (°C)'].astype(float).max()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Suhu Terendah", value=f"{lowest_temp:.1f} °C")

    with col2:
        st.metric("Suhu Tertinggi", value=f"{highest_temp:.1f} °C")

    # Menampilkan grafik rata-rata suhu tahunan
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(temp_yearly['Tahun'], temp_yearly['Rata-rata Suhu (°C)'].astype(float), marker='o', linewidth=2, color="#72BCD4")
    ax.set_title("Rata-rata Suhu Tahunan di Stasiun Wanliu (2013-2017)", loc="center", fontsize=14)
    ax.set_xlabel("Tahun", fontsize=9)
    ax.set_ylabel("Rata-rata Suhu (°C)", fontsize=9)
    ax.tick_params(axis='x', labelsize=9)

  
    ax.set_xticks(temp_yearly['Tahun'])  
    ax.tick_params(axis='y', labelsize=9)
    plt.tight_layout()
    st.pyplot(fig)

    # Visualisasi Rata-rata Kadar Polutan
    st.subheader("Rata-rata Kadar Polutan Tahunan")
    pollutant_yearly = wanliu_df.groupby('year').agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'SO2': 'mean',
        'NO2': 'mean',
        'O3': 'mean'
    }).reset_index()
    pollutant_yearly.rename(columns={"year": "Tahun"}, inplace=True)

    cols_to_format = ['PM2.5', 'PM10', 'SO2', 'NO2', 'O3']
    for col in cols_to_format:
        pollutant_yearly[col] = pollutant_yearly[col].astype(float).apply(lambda x: f"{x:.2f}")

    fig, ax = plt.subplots(figsize=(10, 6))
    for col in cols_to_format:
        ax.plot(pollutant_yearly['Tahun'], pollutant_yearly[col].astype(float), marker='o', label=col)
    
    ax.set_title("Rata-rata Kadar Polutan di Stasiun Wanliu", fontsize=14)
    ax.set_xlabel("Tahun", fontsize=9)
    ax.set_ylabel("Kadar Polutan", fontsize=9)
    ax.legend(title="Polutan", fontsize=9)

    ax.set_xticks(pollutant_yearly['Tahun'])
    ax.tick_params(axis='x', labelsize=9)
    ax.tick_params(axis='y', labelsize=9)
    plt.tight_layout()
    st.pyplot(fig)

    # Hubungan Suhu dengan Polutan
    st.subheader("Hubungan Suhu dengan Kadar Polutan")
    combined_data = pd.merge(pollutant_yearly, temp_yearly, on='Tahun')

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['blue', 'orange', 'green', 'red', 'purple']
    labels = ['PM2.5', 'PM10', 'SO2', 'NO2', 'O3']
    for col, color, label in zip(cols_to_format, colors, labels):
        ax.scatter(combined_data['Rata-rata Suhu (°C)'].astype(float), combined_data[col].astype(float), color=color, alpha=0.5, label=label)

    ax.set_title('Hubungan Kadar Polutan dengan Suhu', fontsize=14)
    ax.set_xlabel('Suhu (°C)', fontsize=9)
    ax.set_ylabel('Kadar Polutan', fontsize=9)
    ax.legend(title="Polutan", fontsize=9)
    ax.grid()
    plt.tight_layout()
    st.pyplot(fig)

# Panggil fungsi dashboard
if __name__ == "__main__":
    dashboard()
