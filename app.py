import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go

# Memuat model yang sudah dilatih
model = joblib.load('prediksi_skor_ujian.pkl')

# Konfigurasi halaman
st.set_page_config(page_title="Prediksi Performa Siswa", page_icon="🎓", layout="centered")

# CSS styling yang ditingkatkan
st.markdown("""
<style>
    /* Styling kontainer utama */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Styling header */
    .main-header {
        background: linear-gradient(to right, #81C784, #A5D6A7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 2.5em;
        font-weight: 800;
        margin: 1em 0;
        padding: 10px;
    }
    
    .subheader {
        color: #FFFFFF;
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 2em;
    }
    
    /* Styling expander modern */
    .stExpander {
        background: white;
        border-radius: 15px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        margin: 1em 0;
        transition: all 0.3s ease;
    }
    
    .stExpander:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }
    
    .stExpander > div > div {
        border: none !important;
    }
    
    /* Styling input */
    .stNumberInput, .stSelectbox {
        background: rgba(255,255,255,0.7);
        border-radius: 10px;
        padding: 5px;
        transition: all 0.3s ease;
    }
    
    .stNumberInput:focus, .stSelectbox:focus {
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.5);
    }
    
    /* Styling tombol */
    .stButton > button {
        background: linear-gradient(to right, #4CAF50, #45a049);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Styling kontainer hasil */
    .result-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 2em 0;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* Progress bar animasi */
    .score-progress {
        height: 30px;
        background: linear-gradient(to right, #FF5252, #FFA726, #FFD740, #69F0AE);
        border-radius: 15px;
        overflow: hidden;
        position: relative;
    }
    
    .score-marker {
        position: absolute;
        height: 100%;
        width: 4px;
        background: #2C3E59;
        left: 0;
        transition: left 1s ease;
    }
</style>
""", unsafe_allow_html=True)

# background
page_bg_img = """
<style>
    [data-testid="stAppViewContainer"]{
    background-image: url("https://i.pinimg.com/originals/6e/38/a5/6e38a5ea916137f9595451424d1fff48.jpg");
    background-size: cover
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🎓 Sistem Prediksi Performa Siswa</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Menganalisis Potensi Akademik Performa Siswa</p>', unsafe_allow_html=True)

# Expander Faktor Akademik dengan Styling Modern
with st.expander("📚 Faktor Akademik Utama", expanded=True):
    st.markdown("### 📊 Data Akademik")
    
    col1, col2 = st.columns(2)
    
    with col1:
        jam_belajar = st.number_input("⏰ Jam Belajar per Minggu", 
                                     min_value=0, max_value=50, value=23,
                                     help="Masukkan jumlah jam yang digunakan untuk belajar dalam satu minggu")
        kehadiran = st.number_input("📅 Persentase Kehadiran di Kelas", 
                                   min_value=0, max_value=100, value=84,
                                   help="Masukkan persentase kehadiran dalam kegiatan pembelajaran")
        jam_tidur = st.number_input("🌙 Rata-rata Jam Tidur per Hari",
                                   min_value=0, max_value=10, value=7,
                                   help="Masukkan rata-rata jam tidur dalam sehari")
    
    with col2:
        skor_sebelumnya = st.number_input("📊 Nilai Ujian Sebelumnya",
                                         min_value=0, max_value=100, value=73,
                                         help="Masukkan nilai ujian terakhir yang diperoleh")
        sesi_bimbingan = st.number_input("👨‍🏫 Jumlah Sesi Bimbingan Belajar",
                                        min_value=0, max_value=15, value=0,
                                        help="Masukkan jumlah sesi bimbingan belajar yang telah diikuti")
        aktivitas_fisik = st.number_input("🏃‍♂️ Jam Olahraga per Minggu",
                                         min_value=0, max_value=10, value=3,
                                         help="Masukkan jumlah jam yang digunakan untuk aktivitas fisik/olahraga dalam seminggu")

# Expander Faktor Pendukung dengan Styling Modern
with st.expander("🔍 Faktor Pendukung", expanded=True):
    st.markdown("### 🌈 Informasi Pendukung")
    
    col3, col4 = st.columns(2)
    
    with col3:
        keterlibatan_ortu = st.selectbox("👨‍👩‍👧‍👦 Tingkat Keterlibatan Orangtua", 
                                        ['Low', 'Medium', 'High'])
        akses_sumber_belajar = st.selectbox("📚 Ketersediaan Akses Pembelajaran",
                                           ['Low', 'Medium', 'High'])
        ekstrakurikuler = st.selectbox("🎭 Mengikuti Kegiatan Ekstrakurikuler",
                                      ['Yes', 'No'])
        tingkat_motivasi = st.selectbox("🎯 Tingkat Motivasi Belajar",
                                       ['Low', 'Medium', 'High'])
        akses_internet = st.selectbox("🌐 Akses Internet Memadai",
                                     ['Yes', 'No'])
        pendapatan_keluarga = st.selectbox("💰 Tingkat Pendapatan Keluarga",
                                          ['Low', 'Medium', 'High'])
    
    with col4:
        kualitas_guru = st.selectbox("👩‍🏫 Kualitas Pengajaran Guru",
                                    ['Low', 'Medium', 'High'])
        tipe_sekolah = st.selectbox("🏫 Jenis Sekolah",
                                   ['Public', 'Private'])
        pengaruh_teman = st.selectbox("👥 Pengaruh Lingkungan Pertemanan",
                                     ['Negative', 'Neutral', 'Positive'])
        kesulitan_belajar = st.selectbox("❓ Mengalami Kesulitan Belajar",
                                        ['Yes', 'No'])
        pendidikan_ortu = st.selectbox("🎓 Tingkat Pendidikan Orangtua",
                                      ['High School', 'College', 'Postgraduate'])
        jarak_rumah = st.selectbox("🏠 Jarak Rumah ke Sekolah",
                                  ['Near', 'Moderate', 'Far'])

st.markdown("---")

# Tombol Prediksi
if st.button("🚀 Analisis Prediksi Nilai", use_container_width=True):
    # Membuat DataFrame input
    input_data = pd.DataFrame({
        'Jam_belajar': [jam_belajar],
        'Kehadiran': [kehadiran],
        'Jam_tidur': [jam_tidur],
        'Ekstrakurikuler': [1 if ekstrakurikuler == 'Yes' else 0],
        'Skor_sebelumnya': [skor_sebelumnya],
        'Tingkat_motivasi': [1 if tingkat_motivasi == 'Low' else 2 if tingkat_motivasi == 'Medium' else 3],
        'Akses_internet': [1 if akses_internet == 'Yes' else 0],
        'Sesi_bimbingan': [sesi_bimbingan],
        'Pendapatan_keluarga': [1 if pendapatan_keluarga == 'Low' else 2 if pendapatan_keluarga == 'Medium' else 3],
        'Kualitas_guru': [1 if kualitas_guru == 'Low' else 2 if kualitas_guru == 'Medium' else 3],
        'Tipe_sekolah': [1 if tipe_sekolah == 'Public' else 2],
        'Pengaruh_teman': [1 if pengaruh_teman == 'Positive' else 2 if pengaruh_teman == 'Neutral' else 3],
        'Aktivitas_fisik': [aktivitas_fisik],
        'Kesulitan_belajar': [1 if kesulitan_belajar == 'Yes' else 0],
        'Pendidikan_keluarga': [1 if pendidikan_ortu == 'High School' else 2 if pendidikan_ortu == 'College' else 3],
        'Jarak_rumah': [1 if jarak_rumah == 'Near' else 2 if jarak_rumah == 'Moderate' else 3],
        'Keterlibatan_Keluarga': [1 if keterlibatan_ortu == 'Low' else 2 if keterlibatan_ortu == 'Medium' else 3],
        'Akses_pembelajaran': [1 if akses_sumber_belajar == 'Low' else 2 if akses_sumber_belajar == 'Medium' else 3],
    })

    # # Persiapan data untuk prediksi
    # data_encoded = pd.get_dummies(input_data)
    # missing_cols = set(model.feature_names_in_) - set(data_encoded.columns)
    # for col in missing_cols:
    #     data_encoded[col] = 0
    # data_encoded = data_encoded[model.feature_names_in_]

    # # Melakukan prediksi
    # predicted_score = model.predict(data_encoded)[0]
    # predicted_score = max(0, min(predicted_score, 100))

    # Persiapan data untuk prediksi
    data_encoded = pd.get_dummies(input_data)
    missing_cols = set(model.feature_names_in_) - set(data_encoded.columns)
    for col in missing_cols:
        data_encoded[col] = 0
    data_encoded = data_encoded[model.feature_names_in_]

    # # Melakukan prediksi
    # predicted_score = model.predict(data_encoded)[0]
    # predicted_score = max(0, min(predicted_score, 100))
    # Melakukan prediksi
    predicted_score = model.predict(data_encoded)[0]  # Hasil prediksi berupa array
    predicted_score = int(predicted_score)  # Pastikan hasil prediksi berupa angka scalar
    predicted_score = max(0, min(predicted_score, 100))  # Batasan skor antara 0-100


    # Menampilkan hasil dengan visualisasi progress kustom
    st.markdown('<div class="result-container">', unsafe_allow_html=True)
    
    # Visualisasi Progress Kustom
    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <h2 style="color: #FFFFFF; text-align: center;">Prediksi Skor Ujian</h2>
        <div class="score-progress" style="height: 30px; background: linear-gradient(to right, #FF5252, #FFA726, #FFD740, #69F0AE); border-radius: 15px; overflow: hidden; position: relative;">
            <div class="score-marker" style="position: absolute; height: 100%; width: 4px; background: #2C3E50 ; left: {predicted_score}%; transition: left 1s ease;"></div>
        </div>
        <h3 style="text-align: center; color: #FFFFFF;">{predicted_score:.2f} / 100</h3>
    </div>
    """, unsafe_allow_html=True)

    # Pesan Interpretasi
    if predicted_score < 50:
        st.error("🚨 Perlu Perhatian Khusus\n\nNilai ini menunjukkan perlunya peningkatan yang signifikan dalam strategi belajar. Mari kita identifikasi area yang perlu diperbaiki dan susun rencana belajar yang lebih efektif.")
    elif 50 <= predicted_score < 65:
        st.warning("🌱 Potensi Berkembang\n\nAnda berada di jalur yang tepat! Dengan sedikit penyesuaian dan konsistensi dalam belajar, Anda dapat meningkatkan hasil belajar menjadi lebih baik.")
    elif 65 <= predicted_score < 70:
        st.success("👏 Prestasi Membanggakan\n\nKerja keras Anda telah membuahkan hasil yang baik! Pertahankan semangat belajar ini dan terus tingkatkan kualitas pembelajaran Anda.")
    else:
        st.balloons()
        st.success("🌟 Prestasi Luar Biasa\n\nAnda telah menunjukkan performa akademik yang sangat memuaskan! Terus pertahankan semangat belajar dan jadilah inspirasi bagi teman-teman Anda.")

    st.markdown('</div>', unsafe_allow_html=True)

    # Expander Informasi Detail Faktor Prediksi
    with st.expander("ℹ️ Tentang Faktor Prediksi"):
        st.markdown("""
        ### 🎯 Detail 18 Faktor Prediksi Performa Akademik

        #### Faktor Akademik Utama
        | Faktor | Deskripsi Detail | Dampak Akademik |
        |--------|-----------------|-----------------|
        | ⏰ Jam Belajar | Waktu yang dihabiskan untuk belajar mandiri | Menentukan kedalaman penguasaan materi |
        | 📅 Persentase Kehadiran | Konsistensi dalam menghadiri kelas | Memastikan pemahaman materi secara komprehensif |
        | 🌙 Jam Tidur | Kualitas dan kuantitas istirahat | Mempengaruhi konsentrasi dan daya serap informasi |
        | 📊 Skor Ujian Sebelumnya | Rekam jejak akademik terdahulu | Mengindikasikan potensi dan kemampuan awal |
        | 👨‍🏫 Sesi Bimbingan | Pengayaan pengetahuan melalui tutorial tambahan | Memperdalam pemahaman konsep sulit |
        | 🏃‍♂️ Aktivitas Fisik | Waktu olahraga dan aktivitas fisik | Meningkatkan kesehatan mental dan fokus belajar |

        #### Faktor Pendukung
        | Faktor | Deskripsi Detail | Dampak Akademik |
        |--------|-----------------|-----------------|
        | 👨‍👩‍👧‍👦 Keterlibatan Orangtua | Dukungan dan perhatian orangtua | Memotivasi dan membimbing perkembangan akademik |
        | 📚 Akses Sumber Belajar | Ketersediaan materi dan sumber informasi | Memperluas kesempatan belajar dan pengetahuan |
        | 🎭 Ekstrakurikuler | Partisipasi dalam kegiatan di luar akademik | Mengembangkan keterampilan soft skills |
        | 🎯 Motivasi Belajar | Semangat dan keinginan untuk berkembang | Menentukan konsistensi dan kualitas belajar |
        | 🌐 Akses Internet | Ketersediaan koneksi online untuk belajar | Memfasilitasi akses informasi dan sumber belajar |
        | 💰 Pendapatan Keluarga | Kondisi ekonomi keluarga | Mempengaruhi dukungan dan sumber daya belajar |
        | 👩‍🏫 Kualitas Guru | Kemampuan dan metode pengajaran | Menentukan kualitas transfer pengetahuan |
        | 🏫 Tipe Sekolah | Jenis institusi pendidikan | Mempengaruhi standar dan kualitas pendidikan |
        | 👥 Pengaruh Lingkungan | Kualitas interaksi sosial | Menstimulasi pertumbuhan intelektual |
        | ❓ Kesulitan Belajar | Tantangan dalam memahami materi | Mengidentifikasi kebutuhan intervensi khusus |
        | 🎓 Pendidikan Orangtua | Latar belakang pendidikan keluarga | Mempengaruhi orientasi dan dukungan akademik |
        | 🏠 Jarak Rumah ke Sekolah | Proximity ke institusi pendidikan | Mempengaruhi waktu dan energi belajar |
        """)