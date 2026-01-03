import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    layout="wide"
)

# ======================
# NETFLIX STYLE CSS
# ======================
st.markdown("""
<style>
.stApp {
    background-color: #141414;
    color: white;
}

h1, h2, h3 {
    color: #E50914;
}

.metric-card {
    background-color: #1f1f1f;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.4);
}

.metric-title {
    font-size: 18px;
    color: #b3b3b3;
}

.metric-value {
    font-size: 36px;
    font-weight: bold;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# ======================
# LOAD DATA
# ======================
df = pd.read_csv("NetFlix.csv")

# Safe preprocessing
df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
df["year_added"] = df["date_added"].dt.year
df["duration"] = df["duration"].astype(str)
df["duration_number"] = df["duration"].str.extract("(\d+)")[0].astype(float)

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.header("🎬 Filter Konten")

content_type = st.sidebar.selectbox(
    "Pilih Jenis Konten",
    ["All", "Movie", "TV Show"]
)

year_range = st.sidebar.slider(
    "Pilih Tahun Rilis",
    int(df["release_year"].min()),
    int(df["release_year"].max()),
    (2010, 2020)
)

filtered_df = df.copy()

if content_type != "All":
    filtered_df = filtered_df[filtered_df["type"] == content_type]

filtered_df = filtered_df[
    (filtered_df["release_year"] >= year_range[0]) &
    (filtered_df["release_year"] <= year_range[1])
]

# ======================
# TITLE
# ======================
st.title("📊 Netflix Content Analytics Dashboard")
st.write("Dashboard interaktif untuk menganalisis konten Netflix berdasarkan jenis, genre, negara, dan tren waktu.")

st.divider()

# ======================
# METRIC CARDS
# ======================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Konten</div>
        <div class="metric-value">{len(filtered_df)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Movie</div>
        <div class="metric-value">{(filtered_df["type"] == "Movie").sum()}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">TV Show</div>
        <div class="metric-value">{(filtered_df["type"] == "TV Show").sum()}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ======================
# CHART 1: CONTENT TYPE
# ======================
st.subheader("Distribusi Jenis Konten")

type_counts = filtered_df["type"].value_counts()

fig1, ax1 = plt.subplots()
type_counts.plot(kind="bar", ax=ax1)
ax1.set_xlabel("Jenis Konten")
ax1.set_ylabel("Jumlah")
st.pyplot(fig1)

# ======================
# CHART 2: TOP GENRES
# ======================
st.subheader("Top 10 Genre Netflix")

genres = filtered_df["genres"].dropna().str.split(", ").explode()
top_genres = genres.value_counts().head(10)

fig2, ax2 = plt.subplots()
top_genres.plot(kind="bar", ax=ax2)
ax2.set_xlabel("Genre")
ax2.set_ylabel("Jumlah")
st.pyplot(fig2)

# ======================
# CHART 3: TREND PER YEAR
# ======================
st.subheader("Tren Penambahan Konten per Tahun")

yearly = filtered_df["year_added"].value_counts().sort_index()

fig3, ax3 = plt.subplots()
ax3.plot(yearly.index, yearly.values)
ax3.set_xlabel("Tahun")
ax3.set_ylabel("Jumlah Konten")
st.pyplot(fig3)
