import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Pengaturan halaman
st.set_page_config(page_title="WVI Topic Modeling Dashboard", layout="wide")

# Custom CSS untuk tampilan modern (mirip HTML referensi)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1, h2, h3 { color: #2c3e50; }
    </style>
    """, unsafe_allow_html=True)

# 1. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('Data_WVI_Dashboard_Final.csv')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("File 'Data_WVI_Dashboard_Final.csv' tidak ditemukan. Pastikan file berada di folder yang sama.")
    st.stop()

# 2. Sidebar Filters
st.sidebar.title("Filter Data")
wilayah_filter = st.sidebar.multiselect("Pilih Wilayah", options=df['Wilayah'].unique(), default=df['Wilayah'].unique())
gender_filter = st.sidebar.multiselect("Pilih Jenis Kelamin", options=df['Jenis Kelamin'].unique(), default=df['Jenis Kelamin'].unique())
umur_filter = st.sidebar.multiselect("Pilih Kelompok Umur", options=df['Umur'].unique(), default=df['Umur'].unique())

# Filter DataFrame
df_filtered = df[
    (df['Wilayah'].isin(wilayah_filter)) &
    (df['Jenis Kelamin'].isin(gender_filter)) &
    (df['Umur'].isin(umur_filter))
]

# 3. Header & KPI
st.title("📊 Dashboard Topic Modeling - WVI")
st.markdown("Visualisasi hasil analisis topik dari tanggapan masyarakat terkait bencana banjir.")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("Total Tanggapan", len(df_filtered))

with kpi2:
    top_topic = df_filtered['topic_category'].mode()[0] if not df_filtered.empty else "-"
    st.metric("Topik Utama", f"T{df_filtered['topic_id'].mode()[0]}" if not df_filtered.empty else "-", help=top_topic)

with kpi3:
    if not df_filtered.empty:
        fem_pct = (len(df_filtered[df_filtered['Jenis Kelamin'] == 'Perempuan']) / len(df_filtered)) * 100
        st.metric("Responden Perempuan", f"{fem_pct:.1f}%")
    else:
        st.metric("Responden Perempuan", "0%")

with kpi4:
    if not df_filtered.empty:
        top_age = df_filtered['Umur'].mode()[0]
        st.metric("Kelompok Usia Dominan", top_age)
    else:
        st.metric("Kelompok Usia Dominan", "-")

st.markdown("---")

# 4. Visualisasi Utama (Grid Layout)
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("📍 Heatmap Topik per Wilayah")
    # Pivot data untuk heatmap
    hm_data = df_filtered.groupby(['Wilayah', 'topic_category']).size().reset_index(name='counts')
    hm_pivot = hm_data.pivot(index='Wilayah', columns='topic_category', values='counts').fillna(0)
    
    fig_hm = px.imshow(
        hm_pivot,
        labels=dict(x="Topik", y="Wilayah", color="Jumlah"),
        color_continuous_scale='YlOrBr', # Warna hangat sesuai referensi HTML
        aspect="auto"
    )
    fig_hm.update_layout(height=400)
    st.plotly_chart(fig_hm, use_container_width=True)

with col_right:
    st.subheader("🍰 Distribusi Gender")
    fig_pie = px.pie(
        df_filtered, 
        names='Jenis Kelamin', 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_layout(showlegend=True, height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

col_bot1, col_bot2 = st.columns(2)

with col_bot1:
    st.subheader("📈 Frekuensi per Kategori Topik")
    topic_counts = df_filtered['topic_category'].value_counts().reset_index()
    topic_counts.columns = ['Topik', 'Jumlah']
    fig_bar = px.bar(
        topic_counts, 
        x='Jumlah', 
        y='Topik', 
        orientation='h',
        color='Jumlah',
        color_continuous_scale='Viridis'
    )
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

with col_bot2:
    st.subheader("👥 Kelompok Usia Responden")
    age_counts = df_filtered['Umur'].value_counts().reset_index()
    age_counts.columns = ['Usia', 'Jumlah']
    fig_age = px.bar(
        age_counts, 
        x='Usia', 
        y='Jumlah',
        color='Usia',
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_age.update_layout(height=400)
    st.plotly_chart(fig_age, use_container_width=True)

# 5. Data Table (Opsional)
with st.expander("Lihat Detail Data Mentah"):
    st.dataframe(df_filtered[['Wilayah', 'Umur', 'Jenis Kelamin', 'topic_category', 'Tanggapan']], use_container_width=True)
