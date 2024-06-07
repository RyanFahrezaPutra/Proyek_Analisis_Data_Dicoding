import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    try:
        file_path = "dashboard/main_data.csv"
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error("Failed to load data. File not found.")
        return None

def pm10_distribution(data):
    data['year'] = pd.to_datetime(data['year'], format='%Y').dt.year
    return data.groupby('year')['PM10'].mean()

def feature_distribution(data):
    features = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    total = data[features].sum().sum()
    proportions = data[features].sum() / total
    return proportions

# Main function to run the dashboard
def main():
    st.title('Dashboard Kualitas Udara di Guanyuan')
    st.write("Analisis Data Kualitas Udara di Guanyuan berdasarkan Data PM10 dan Jumlah Hari Hujan per Tahun.")

    # Load data
    data = load_data()

    if data is not None:
        # Plot PM10 distribution
        st.header('PM10 Distribution')
        pm10_data = pm10_distribution(data)
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        ax1.plot(pm10_data.index, pm10_data.values, marker='o', color='red')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('PM10')
        ax1.set_title('Rata-rata Bulanan PM10 di Guanyuan (2013-2017)')
        ax1.grid(True)
        st.pyplot(fig1)
        st.write("""
                **Analisis:**
                PM10 adalah kualitas udara yang cukup berbahaya. Berdasarkan hasil 
                visualisasi yang didapat, PM10 ini memuncak di tahun 2014, namun di tahun 2017 
                sudah menurun dan bisa dipastikan bahwa kualitas udara jadi lebih bersih dan lebih baik.
            """)

        # Plot feature distribution
        st.header('Feature Distribution')
        feature_data = feature_distribution(data)
        fig2, ax2 = plt.subplots(figsize=(10, 8))
        ax2.pie(feature_data, labels=feature_data.index, autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax2.set_title('Distribusi Fitur')
        st.pyplot(fig2)
        st.write("""
                **Analisis:**
                Dari visualisasi yang kita lihat, komponen yang paling sedikit terdapat pada guangyan 
                adalah SO2 dengan hanya 1,1%. berbeda jauh dengan komponen terbanyak yaitu CO yang mencapai 77,1%.
            """)

if __name__ == "__main__":
    main()
    st.set_option('deprecation.showPyplotGlobalUse', False)  # Disable the warning globally
