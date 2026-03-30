import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Konfigurasi Halaman (Wide Layout, Tanpa Sidebar)
st.set_page_config(page_title="WVI Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. Custom CSS untuk Tata Letak Modern (Mereplikasi Tampilan HTML)
st.markdown("""
    <style>
    /* Mengubah background halaman menjadi abu-abu muda */
    .main { background-color: #f8f9fa; }
    
    /* Menghapus margin default Streamlit agar lebih rapat */
    [data-testid="stHeader"], [data-testid="stSidebar"] { display: none; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }

    /* Styling Gaya Kartu Putih untuk Visualisasi */
    .plot-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Styling Judul dan Subjudul */
    h1 { color: #2c3e50; font-size: 24px; font-weight: 700; margin-bottom: 5px; }
    h3 { color: #5f6c7b; font-size: 16px; font-weight: 500; margin-top: 0; margin-bottom: 25px; }
    
    /* Menghilangkan border pada Chart */
    .js-plotly-plot .plotly .modebar { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Dashboard
st.markdown("<h1>Dashboard Topic Modeling WVI</h1>", unsafe_allow_html=True)
st.markdown("<h3>Analisis distribusi topik hasil tanggapan masyarakat terkait bencana banjir di tiga wilayah.</h3>", unsafe_allow_html=True)
st.markdown("---")

# 4. Perhitungan Data Berdasarkan CSV (Agar Sesuai Referensi HTML)
@st.cache_data
def get_calculated_data():
    df = pd.read_csv('Data_WVI_Dashboard_Final.csv')
    
    # a. Matriks Heatmap (Wilayah vs Topik ID)
    hm_pivot = df.groupby(['Wilayah', 'topic_id']).size().unstack(fill_value=0)
    
    # Pengurutan Baris (Wilayah) dan Kolom (Topik 0-5)
    hm_pivot = hm_pivot.reindex(index=['Sibolga Utara', 'Tapsel', 'Tapteng'], 
                                columns=[0, 1, 2, 3, 4, 5], fill_value=0)
    
    # b. Data Doughnut Chart (Total per Wilayah)
    region_counts = df['Wilayah'].value_counts().reindex(['Sibolga Utara', 'Tapsel', 'Tapteng']).reset_index()
    region_counts.columns = ['Wilayah', 'Jumlah']
    
    return hm_pivot, region_counts

# Load data hasil kalkulasi
hm_pivot, region_counts = get_calculated_data()

# 5. Visualisasi Utama (Layout Kolom)
col1, col2 = st.columns([2, 1])

with col1:
    # --- VISUALISASI 1: HEATMAP (Mereplikasi Warna dan Label HTML) ---
    st.markdown("<div class='plot-container'>", unsafe_allow_html=True)
    st.markdown("#### Matriks Distribusi Topik per Wilayah")
    
    # Label Kolom Topik Lengkap
    topic_labels = [
        'T0 Keluhan Kes.', 'T1 Kerusakan Infra.', 'T2 Dampak Psikosos.', 
        'T3 Deskripsi Umum', 'T4 Kecemasan Harian', 'T5 Logistik'
    ]
    
    fig_hm = px.imshow(
        hm_pivot,
        x=topic_labels,
        y=hm_pivot.index,
        # Menggunakan skala warna hangat (YlOrBr) sesuai referensi HTML
        color_continuous_scale='YlOrBr', 
        text_auto=True, # Menampilkan angka di dalam kotak
        labels=dict(x="Kategori Topik", y="Wilayah", color="Jumlah"),
        aspect="auto"
    )
    
    # Penyesuaian tata letak Plotly
    fig_hm.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=20),
        coloraxis_showscale=False, # Sembunyikan colorbar agar bersih
        height=450
    )
    fig_hm.update_xaxes(tickangle=0, side="bottom")
    
    st.plotly_chart(fig_hm, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    # --- VISUALISASI 2: DOUGHNUT CHART (Mereplikasi Tampilan HTML) ---
    st.markdown("<div class='plot-container'>", unsafe_allow_html=True)
    st.markdown("#### Proporsi Responden per Wilayah")
    
    fig_donut = go.Figure(data=[go.Pie(
        labels=region_counts['Wilayah'],
        values=region_counts['Jumlah'],
        hole=.6, # Membuat lubang di tengah (Doughnut)
        # Warna khusus sesuai referensi HTML
        marker=dict(colors=['#5470c6', '#91cc75', '#fac858']),
        textinfo='percent+label',
        textposition='outside',
        showlegend=False
    )])
    
    fig_donut.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=10),
        height=450
    )
    
    st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

# 6. Catatan Kaki (Footer)
st.markdown("---")
st.caption("Dashboard ini bersifat statis dan mereplikasi tampilan visual dari laporan HTML referensi WVI.")
