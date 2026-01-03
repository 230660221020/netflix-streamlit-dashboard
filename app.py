import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    layout="wide"
)

# ===============================
# CUSTOM CSS (NETFLIX STYLE)
# ===============================
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3 {
    color: #E50914;
}

.metric-card {
    background-color: #1F2933;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.5);
}

.metric-title {
    font-size: 16px;
    color: #AAAAAA;
}

.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# LOAD DATA
# ===============================
@st.cache_data
def load_data():
    df = pd.read_csv("NetFlix.csv")
    return df

df = load_data()

# ===============================
# DATA CLEANING
# ===============================
df["duration"] = df["duration"].astype(str)
df["duration_number"] = df["duration"].str.extract(r"(\d+)").astype(float)
df = df.dropna(subset=["duration_number", "release_year", "type"])

# ===============================
# K-MEANS CLUSTERING (REAL-TIME)
# ===============================
features = df[["release_year", "duration_number"]]

scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=3, random_state=42)
df["cluster"] = kmeans.fit_predict(scaled_features)

# ===============================
# HEADER
# ===============================
st.title("🎬 Netflix Analytics Dashboard")
st.markdown(
    "Dashboard interaktif untuk analisis dan segmentasi konten Netflix menggunakan pendekatan Big Data."
)

# ===============================
# METRIC CARDS
# ===============================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Konten</div>
        <div class="metric-value">{df.shape[0]}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Rata-rata Durasi</div>
        <div class="metric-value">{df['duration_number'].mean():.1f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Jumlah Cluster</div>
        <div class="metric-value">{df['cluster'].nunique()}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ===============================
# FILTER
# ===============================
selected_type = st.selectbox(
    "Pilih Tipe Konten",
    options=df["type"].unique()
)

filtered_df = df[df["type"] == selected_type]

# ===============================
# VISUALISASI — HISTOGRAM
# ===============================
st.subheader("📊 Distribusi Durasi Konten")

fig1, ax1 = plt.subplots()
ax1.hist(filtered_df["duration_number"], bins=30)
ax1.set_xlabel("Durasi")
ax1.set_ylabel("Jumlah Konten")
st.pyplot(fig1)

# ===============================
# VISUALISASI — BAR CHART
# ===============================
st.subheader("📦 Jumlah Konten per Tahun Rilis")

year_count = filtered_df["release_year"].value_counts().sort_index()

fig2, ax2 = plt.subplots()
ax2.bar(year_count.index, year_count.values)
ax2.set_xlabel("Tahun Rilis")
ax2.set_ylabel("Jumlah Konten")
st.pyplot(fig2)

# ===============================
# VISUALISASI — CLUSTERING
# ===============================
st.subheader("🧩 Segmentasi Konten Netflix (K-Means)")

fig3, ax3 = plt.subplots()
ax3.scatter(
    df["release_year"],
    df["duration_number"],
    c=df["cluster"],
    alpha=0.6
)
ax3.set_xlabel("Tahun Rilis")
ax3.set_ylabel("Durasi")
st.pyplot(fig3)

# ===============================
# INTERPRETASI
# ===============================
st.markdown("""
### 📌 Interpretasi Cluster
- **Cluster 0**: Konten berdurasi pendek
- **Cluster 1**: Konten berdurasi menengah
- **Cluster 2**: Konten berdurasi panjang

Segmentasi ini membantu memahami karakteristik konten Netflix dan mendukung strategi rekomendasi.
""")

st.caption("UAS Big Data | Sistem Informasi | Universitas Sebelas April")
