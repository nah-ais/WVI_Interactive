import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Konfigurasi Halaman & Gaya (CSS)
st.set_page_config(page_title="WVI Dashboard", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Fungsi Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('Data_WVI_Dashboard_Final.csv')
    return df

df = load_data()

# 3. Sidebar Filter
st.sidebar.title("🔍 Filter Dashboard")
wilayah_list = df['Wilayah'].unique().tolist()
selected_wilayah = st.sidebar.multiselect("Pilih Wilayah", wilayah_list, default=wilayah_list)

# Filter dataframe
df_filt = df[df['Wilayah'].isin(selected_wilayah)]

# 4. Header & KPI Cards
st.title("📊 Dashboard Topic Modeling - WVI")
st.caption("Visualisasi hasil analisis topik dari tanggapan masyarakat terkait bencana banjir.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Tanggapan", f"{len(df_filt)} data")
with col2:
    top_topic = df_filt['topic_category'].mode()[0] if not df_filt.empty else "N/A"
    st.metric("Topik Utama", f"T{df_filt['topic_id'].mode()[0]}" if not df_filt.empty else "-", help=top_topic)
with col3:
    fem_pct = (len(df_filt[df_filt['Jenis Kelamin']=='Perempuan'])/len(df_filt)*100) if not df_filt.empty else 0
    st.metric("Responden Perempuan", f"{fem_pct:.1f}%")
with col4:
    age_top = df_filt['Umur'].mode()[0] if not df_filt.empty else "N/A"
    st.metric("Kelompok Usia Terbanyak", age_top)

st.markdown("---")

# 5. Visualisasi Utama
c1, c2 = st.columns([3, 2])

with c1:
    st.subheader("📍 Heatmap: Topik vs Wilayah")
    hm_data = df_filt.groupby(['Wilayah', 'topic_category']).size().reset_index(name='Jumlah')
    fig_hm = px.density_heatmap(
        hm_data, x="topic_category", y="Wilayah", z="Jumlah",
        color_continuous_scale="YlOrBr", text_auto=True,
        labels={'topic_category': 'Kategori Topik'}
    )
    fig_hm.update_layout(height=450)
    st.plotly_chart(fig_hm, use_container_width=True)

with c2:
    st.subheader("🍰 Distribusi Gender")
    fig_pie = px.pie(
        df_filt, names='Jenis Kelamin', hole=0.5,
        color_discrete_sequence=['#EF9F27', '#FAC775']
    )
    fig_pie.update_layout(height=450, legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5))
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# 6. Grafik Bar Bawah
b1, b2 = st.columns(2)

with b1:
    st.subheader("📈 Frekuensi per Kategori Topik")
    counts = df_filt['topic_category'].value_counts().reset_index()
    counts.columns = ['Topik', 'Jumlah']
    fig_bar = px.bar(counts, x='Jumlah', y='Topik', orientation='h', color='Jumlah', color_continuous_scale='Viridis')
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

with b2:
    st.subheader("👥 Kelompok Usia")
    age_counts = df_filt['Umur'].value_counts().reset_index()
    fig_age = px.bar(age_counts, x='Umur', y='count', color='Umur', color_discrete_sequence=px.colors.qualitative.Prism)
    fig_age.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_age, use_container_width=True)

# 7. Detail Data
with st.expander("📄 Lihat Detail Data Tanggapan"):
    st.dataframe(df_filt[['Wilayah', 'Umur', 'Jenis Kelamin', 'topic_category', 'Tanggapan']], use_container_width=True)
