import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt
import base64

# Fungsi untuk memprediksi kebutuhan energi
def predict_energy_demand(features, historical_energy, algorithm='Linear Regression'):
    if algorithm == 'Linear Regression':
        model = LinearRegression()
    elif algorithm == 'Random Forest':
        model = RandomForestRegressor()
    elif algorithm =='SVM':
        model = SVR()
    elif algorithm == 'KNN':
        model = KNeighborsRegressor()
    model.fit(features, historical_energy)
    predicted_demand = model.predict(features)
    return predicted_demand

# Function to create a download link for a DataFrame as a CSV file
def download_link(df, filename="dataset.csv", text="Download Dataset"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Binarize and convert to base64
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def main():
    st.set_page_config(page_title="EcoInsight", page_icon="D:\project\c\image\ICO.ico")
    st.markdown('ECOINSIGHT - PREDIKSI KEBUTUHAN ENERGI')
    st.sidebar.image('D:\project\c\image\eco.png', use_column_width=True)
    st.sidebar.header('EcoInsight')

    st.markdown(
    """
    <style>
    /* CSS untuk mengatur judul di tengah */
    .title-wrapper {
        text-align: center;
        font-family: 'Arial', sans-serif; /* Atur jenis font di sini */
        font-size: 50px; /* Atur ukuran font di sini */
        color: #13f031; /* Atur warna teks */
    }

    /* CSS untuk mengatur tata letak dan jenis font teks */
    .content {
        text-align: center;
        font-family: 'Arial', sans-serif; /* Atur jenis font di sini */
        font-size: 20px; /* Atur ukuran font di sini */
        color: #ECF6D9 ; /* Atur warna teks */
    }
    </style>
    """,
    unsafe_allow_html=True
)

    # Menampilkan judul di tengah halaman dengan jenis font yang diatur
    st.markdown("<h1 class='title-wrapper'>EcoInsight</h1>", unsafe_allow_html=True)

    # Menampilkan penjelasan tentang DATATICS dengan tata letak dan ukuran font yang diatur
    st.markdown("<div class='content'>EcoInsight adalah sebuah model prediksi yang digunakan untuk mengoptimalkan kebutuhan energi suatu industri dengan pendekatan berkelanjutan yang menggunakan algoritma machine learning sebagai acuannya berfungsi untuk mengoptimalkan konsumsi energi suatu industri, industri tersbut dapat membuat kontribusi yang signifikan pada pembangunan berkelanjutan. Penggunaan yang lebih efisien dari sumber daya energi dapat membantu mengurangi emisi gas rumah kaca dan dampak lingkungan lainnya, serta meningkatkan keberlanjutan jangka panjang industri itu sendiri. </div>", unsafe_allow_html=True)
                         
    data_contoh = pd.DataFrame({
        "Tanggal": ["5/21/2024", "5/21/2024", "5/21/2024", "5/21/2024", "5/21/2024"],
        "Waktu": ["7:00", "8:00", "9:00", "10:00", "11:00"],
        "Suhu (C)": [25, 26, 27, 28, 29],
        "Kelembaban (%)": [60, 50, 30, 40, 50],
        "Produksi (unit)": [1000, 1200, 1300, 2000, 1500],
        "Konsumsi Energi (kWh)": [250, 300, 400, 500, 700],
        "Emisi Karbon (ton)": [0.5, 0.6, 0.7, 0.8, 0.9],
        "Konsumsi Air (m3)": [20, 25, 30, 28, 27]
    })

    st.write('silahakan download file dataset contoh:')
    st.markdown(download_link(data_contoh, filename="example_dataset.csv", text="Unduh sample Dataset CSV"), unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Unggah file CSV", type="csv")

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write('File yang diunggah:')
        st.write(data)

        required_columns = ['Suhu (C)', 'Konsumsi Energi (kWh)']
        optional_columns = ['Kelembaban (%)', 'Kecepatan Angin (km/h)', 'Tekanan Udara (hPa)', 'Curah Hujan (mm)', 'Radiasi Matahari (W/m²)']

        for col in required_columns:
            if col not in data.columns:
                st.error(f"Kolom yang diperlukan '{col}' tidak ada dalam file CSV.")
                return

        # Ekstrak fitur yang diperlukan
        features = data[required_columns[0]].values.reshape(-1, 1)
        historical_energy = data[required_columns[1]]

        # Tambahkan fitur opsional jika tersedia
        for col in optional_columns:
            if col in data.columns:
                features = np.column_stack((features, data[col].values))

                # Pilihan algoritma
        algorithm = st.selectbox("Pilih Algoritma", ["Linear Regression", "Random Forest", "SVM", "KNN"])

        # Prediksi kebutuhan energi
        predicted_demand = predict_energy_demand(features, historical_energy, algorithm)

        # Tambahkan hasil prediksi ke dalam DataFrame
        data['Prediksi Kebutuhan Energi (kWh)'] = predicted_demand

        st.write('Hasil Prediksi:')
        st.write(data)

        # Buat grafik prediksi
        plt.figure(figsize=(10, 5))
        plt.plot(data['Tanggal'] + ' ' + data['Waktu'], data['Konsumsi Energi (kWh)'], label='Konsumsi Energi Aktual')
        plt.plot(data['Tanggal'] + ' ' + data['Waktu'], data['Prediksi Kebutuhan Energi (kWh)'], label='Prediksi Kebutuhan Energi', linestyle='--')
        plt.xlabel('Waktu')
        plt.ylabel('Konsumsi Energi (kWh)')
        plt.title('Prediksi Kebutuhan Energi')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(plt)

        # Simpan hasil prediksi ke file CSV baru
        result_file_path = "predicted_" + uploaded_file.name
        data.to_csv(result_file_path, index=False)

        # Membaca file prediksi sebagai binary untuk diunduh
        with open(result_file_path, 'rb') as f:
            st.download_button(
                label="Download hasil prediksi sebagai CSV",
                data=f,
                file_name=result_file_path,
                mime='text/csv'
            )

if __name__ == '__main__':
    main()

