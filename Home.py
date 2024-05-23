import streamlit as st


st.set_page_config(
    page_title="DATATICS",
    page_icon="D:\project\c\image\ICO.ico",
)


st.sidebar.image('D:\project\c\image\eco.png', use_column_width=True)

# Menambahkan CSS untuk mengatur tata letak dan jenis font judul di tengah
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
        color: #333333; /* Atur warna teks */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Menampilkan judul di tengah halaman dengan jenis font yang diatur
st.markdown("<h1 class='title-wrapper'>APA ITU DATATICS?</h1>", unsafe_allow_html=True)

# Menampilkan penjelasan tentang DATATICS dengan tata letak dan ukuran font yang diatur
st.markdown("<div class='content'>DATATICS adalah platform yang didedikasikan untuk menganalisis dan memahami data dengan lebih baik. Kami menyediakan berbagai alat dan sumber daya untuk membantu Anda dalam proses analisis data, mulai dari pemrosesan data hingga visualisasi dan pembuatan model prediksi. <br><br> Dengan DATATICS, Anda dapat menjelajahi berbagai teknik dan konsep analisis data, serta mengembangkan keterampilan Anda dalam bidang data science. Bergabunglah dengan komunitas kami dan temukan berbagai peluang baru dalam dunia data! <br><br> Jika Anda tertarik untuk mulai belajar dan mengembangkan keterampilan analisis data, DATATICS adalah tempat yang tepat untuk memulai!</div>", unsafe_allow_html=True)


