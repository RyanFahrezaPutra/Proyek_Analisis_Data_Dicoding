import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

def rainy_days_per_year(data):
    return data[data['RAIN'] > 0].groupby('year')['day'].nunique()

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
                PM10 adalah kualitas udara yang cukup berbahaya. berdasarkan hasil 
                visualisai yang didapat, PM10 ini memuncak di tahun 2014, namun di tahun 2017 
                sudah menurun dan bisa dipastikan bahwa kualitas udara jadi lebih bersih dan lebih baik.
            """)

        # Plot rainy days per year
        st.header('Rainy Days per Year')
        rainy_days_data = rainy_days_per_year(data)
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.bar(rainy_days_data.index, rainy_days_data.values, color='blue')
        ax2.set_xlabel('Year')
        ax2.set_ylabel('Rainy Days')
        ax2.set_title('Jumlah Hari Hujan per Tahun di Guanyuan (2013-2017)')
        ax2.grid(axis='y')
        st.pyplot(fig2)
        st.write("""
                **Analisis:**
                Sepertinya kekurangan data pada tahun 2017 sehingga curah hujan mengecil, 
                ataupun curah hujan memang tak nampak pada tahun itu. dilihat dari jumlah PM10 dan data 
                curah hujan, tidak memiliki kaitan yang 
                signifikan satu sama lain. bisa disimpulkan disini 
                bahwa curah hujan tidak terlalu berpengaruh.
            """)

if __name__ == "__main__":
    main()
    st.set_option('deprecation.showPyplotGlobalUse', False)  # Disable the warning globally
