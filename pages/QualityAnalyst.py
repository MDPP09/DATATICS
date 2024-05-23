import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from fpdf import FPDF
import base64

# Fungsi untuk melatih model dan membuat prediksi
def train_and_evaluate(data):
    data['Quality'] = data['Height'].apply(lambda x: 1 if 19 <= x <= 21 else 0)
    X = data[['Length', 'Width', 'Height']]
    y = data['Quality']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred, output_dict=True)
    return conf_matrix, class_report

# Fungsi untuk membuat file PDF dari classification report
def create_pdf_report(conf_matrix, class_report):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Classification Report", ln=True, align='C')
    pdf.cell(200, 10, txt="Confusion Matrix", ln=True, align='L')
    for row in conf_matrix:
        pdf.cell(200, 10, txt=str(row), ln=True, align='L')

    pdf.cell(200, 10, txt="Classification Report Details", ln=True, align='L')
    for key, value in class_report.items():
        if key not in ["accuracy", "macro avg", "weighted avg"]:
            pdf.cell(200, 10, txt=f"Class {key}:", ln=True, align='L')
            pdf.cell(200, 10, txt=f"  Precision: {value['precision']:.2f}", ln=True, align='L')
            pdf.cell(200, 10, txt=f"  Recall: {value['recall']:.2f}", ln=True, align='L')
            pdf.cell(200, 10, txt=f"  F1-Score: {value['f1-score']:.2f}", ln=True, align='L')
            pdf.cell(200, 10, txt=f"  Support: {value['support']}", ln=True, align='L')
            pdf.cell(200, 10, txt="", ln=True, align='L')

    pdf.cell(200, 10, txt=f"Accuracy: {class_report['accuracy']:.2f}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Macro Avg Precision: {class_report['macro avg']['precision']:.2f}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Macro Avg Recall: {class_report['macro avg']['recall']:.2f}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Macro Avg F1-Score: {class_report['macro avg']['f1-score']:.2f}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Weighted Avg Precision: {class_report['weighted avg']['precision']:.2f}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Weighted Avg Recall: {class_report['weighted avg']['recall']:.2f}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Weighted Avg F1-Score: {class_report['weighted avg']['f1-score']:.2f}", ln=True, align='L')

    pdf.output("classification_report.pdf")

# Fungsi untuk mengunduh dataset contoh
def download_sample_data():
    data = {
        'Item_No': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
        'Length': [102.67, 102.5, 95.37, 94.77, 104.26, 105.18, 97.35, 99.35, 90.62, 97.22, 100, 97.23, 105.72, 89.82],
        'Width': [49.53, 51.42, 52.25, 49.24, 47.9, 49.39, 48.05, 44.59, 47.29, 52.14, 54.76, 48.26, 50.04, 45.98],
        'Height': [19.69, 19.63, 21.51, 18.6, 19.46, 20.36, 20.22, 21.03, 19.78, 20.71, 20.62, 19.51, 20.06, 20.3],
        'Operator': ['Op-1'] * 14
    }
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="sample_data.csv">Unduh sample dataset CSV</a>'
    return href

# Fungsi untuk menampilkan classification report dalam format yang mudah dimengerti
def display_classification_report(report):
    st.write("### Classification Report (Laporan Klasifikasi)")

    st.write("**Presisi**: Berapa banyak prediksi positif yang benar.")
    st.write("**Recall**: Berapa banyak data sebenarnya positif yang terdeteksi.")
    st.write("**F1-Skor**: Gabungan dari presisi dan recall. Skor lebih tinggi artinya lebih baik.")
    st.write("**Dukungan**: Jumlah data dalam setiap kategori.")

    for key, value in report.items():
        if key not in ["accuracy", "macro avg", "weighted avg"]:
            st.write(f"**Kelas {key}**:")
            st.write(f"- Presisi: {value['precision']:.2f}")
            st.write(f"- Recall: {value['recall']:.2f}")
            st.write(f"- F1-Skor: {value['f1-score']:.2f}")
            st.write(f"- Dukungan: {value['support']} sampel")
            st.write("")

    st.write(f"**Akurasi**: {report['accuracy']:.2f} - Proporsi prediksi yang benar dari keseluruhan prediksi.")
    st.write(f"**Rata-rata Makro**:")
    st.write(f"- Presisi: {report['macro avg']['precision']:.2f}")
    st.write(f"- Recall: {report['macro avg']['recall']:.2f}")
    st.write(f"- F1-Skor: {report['macro avg']['f1-score']:.2f}")
    st.write(f"**Rata-rata Terbobot**:")
    st.write(f"- Presisi: {report['weighted avg']['precision']:.2f}")
    st.write(f"- Recall: {report['weighted avg']['recall']:.2f}")
    st.write(f"- F1-Skor: {report['weighted avg']['f1-score']:.2f}")

# Streamlit UI
st.set_page_config(page_title="Quality Analyst", page_icon="D:\project\c\image\ICO.ico")
st.markdown('Quality Analyst - analisis kualitas')
st.sidebar.image('D:\project\c\image\eco.png', use_column_width=True)
st.sidebar.header('Quality Analyst')
st.markdown(
    """
    <style>
    .title-wrapper {
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-size: 50px;
        color: #27AFFC ;
    }
    .content {
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-size: 20px;
        color: #C8E5F5 ;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Menampilkan judul dan penjelasan
st.markdown("<h1 class='title-wrapper'>Quality Analyst</h1>", unsafe_allow_html=True)
st.markdown("<div class='content'>Membantu pengguna mengklasifikasikan produk berdasarkan kualitasnya menggunakan machine learning, menyediakan laporan performa model yang mudah dimengerti, dan memudahkan pengguna dalam mengunduh dataset contoh serta hasil laporan dalam format PDF.</div>", unsafe_allow_html=True)

st.markdown(download_sample_data(), unsafe_allow_html=True)

uploaded_file = st.file_uploader("Pilih file CSV atau Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        
        st.write("Dataframe:")
        st.write(df)
        
        if st.button('Analisis'):
            conf_matrix, class_report = train_and_evaluate(df)
            st.write("Confusion Matrix:")
            st.write(conf_matrix)
            
            display_classification_report(class_report)
            
            create_pdf_report(conf_matrix, class_report)
            with open("classification_report.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()
                b64 = base64.b64encode(PDFbyte)
                b64 = base64.b64encode(PDFbyte).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="classification_report.pdf">Unduh Classification Report (PDF)</a>'
                st.markdown(href, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {e}")


