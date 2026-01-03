import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ======================
# CONFIG PAGE
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
</style>
""", unsafe_allow_html=True)

# ======================
# LOAD DATA
# ======================
filtered_df = pd.read_csv("NetFlix.csv")

# Cleaning ringan (supaya aman di dashboard)
filtered_df["date_added"] = pd.to_datetime(filtered_df["date_added"], errors="coerce")
filtered_df["year_added"] = filtered_df["date_added"].dt.year
filtered_df["duration"] = filtered_df["duration"].astype(str)
filtered_df["duration_number"] = filtered_df["duration"].str.extract("(\d+)")[0].astype(float)
filtered_df = pd.read_csv("NetFlix.csv")
st.sidebar.header("🎬 Filter Konten")

content_type = st.sidebar.selectbox(
    "Pilih Jenis Konten",
    ["All", "Movie", "TV Show"]
)

year_range = st.sidebar.slider(
    "Pilih Tahun Rilis",
    int(filtered_df["release_year"].min()),
    int(filtered_df["release_year"].max()),
    (2010, 2020)
)

# Apply filter
filtered_filtered_df = filtered_df.copy()

if content_type != "All":
    filtered_filtered_df = filtered_filtered_df[filtered_filtered_df["type"] == content_type]

filtered_filtered_df = filtered_filtered_df[
    (filtered_filtered_df["release_year"] >= year_range[0]) &
    (filtered_filtered_df["release_year"] <= year_range[1])
]


# ======================
# TITLE
# ======================
st.title("📊 Netflix Content Analytics Dashboard")
st.write("Analisis konten Netflix berdasarkan jenis, genre, negara, dan tren waktu.")

# ======================
# METRICS
# ======================
col1, col2, col3 = st.columns(3)
col1.metric("Total Konten", len(filtered_df))
col2.metric("Total Movie", (filtered_df["type"] == "Movie").sum())
col3.metric("Total TV Show", (filtered_df["type"] == "TV Show").sum())

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

genres = filtered_df["genres"].str.split(", ").explode()
top_genres = genres.value_counts().head(10)

fig2, ax2 = plt.subplots()
top_genres.plot(kind="bar", ax=ax2)
ax2.set_xlabel("Genre")
ax2.set_ylabel("Jumlah")
st.pyplot(fig2)

# ======================
# CHART 3: TREND
# ======================
st.subheader("Tren Penambahan Konten per Tahun")

yearly = filtered_df["year_added"].value_counts().sort_index()

fig3, ax3 = plt.subplots()
ax3.plot(yearly.index, yearly.values)
ax3.set_xlabel("Tahun")
ax3.set_ylabel("Jumlah Konten")
st.pyplot(fig3)



