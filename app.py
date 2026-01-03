import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    layout="wide"
)

# ======================
# NETFLIX MODERN CSS
# ======================
st.markdown("""
<style>
.stApp {
    background-color: #0f0f0f;
    color: white;
}

h1, h2, h3 {
    color: #E50914;
    font-weight: 700;
}

.card {
    background: linear-gradient(135deg, #1f1f1f, #141414);
    padding: 24px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}

.card-title {
    font-size: 16px;
    color: #b3b3b3;
}

.card-value {
    font-size: 40px;
    font-weight: bold;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# ======================
# LOAD & PREPROCESS DATA
# ======================
df = pd.read_csv("NetFlix.csv")

df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
df["year_added"] = df["date_added"].dt.year
df["duration"] = df["duration"].astype(str)
df["duration_number"] = df["duration"].str.extract("(\d+)")[0].astype(float)

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.title("🎬 Netflix Filter")

content_type = st.sidebar.radio(
    "Jenis Konten",
    ["All", "Movie", "TV Show"]
)

year_range = st.sidebar.slider(
    "Tahun Rilis",
    int(df["release_year"].min()),
    int(df["release_year"].max()),
    (2015, 2020)
)

filtered_df = df.copy()

if content_type != "All":
    filtered_df = filtered_df[filtered_df["type"] == content_type]

filtered_df = filtered_df[
    (filtered_df["release_year"] >= year_range[0]) &
    (filtered_df["release_year"] <= year_range[1])
]

# ======================
# HEADER WITH LOGO
# ======================
col_logo, col_title = st.columns([1, 6])

with col_logo:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg",
        width=90
    )

with col_title:
    st.title("Netflix Content Analytics")
    st.caption("Dashboard analitik interaktif untuk eksplorasi konten Netflix")

st.divider()

# ======================
# METRIC CARDS
# ======================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Total Konten</div>
        <div class="card-value">{len(filtered_df)}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Movie</div>
        <div class="card-value">{(filtered_df["type"] == "Movie").sum()}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">TV Show</div>
        <div class="card-value">{(filtered_df["type"] == "TV Show").sum()}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ======================
# CHARTS SECTION
# ======================
col_left, col_right = st.columns(2)

# Distribusi Jenis Konten
with col_left:
    st.subheader("Distribusi Jenis Konten")
    type_counts = filtered_df["type"].value_counts().reset_index()
    type_counts.columns = ["Type", "Count"]

    fig_type = px.bar(
        type_counts,
        x="Type",
        y="Count",
        color="Type",
        color_discrete_sequence=["#E50914", "#b3b3b3"]
    )
    st.plotly_chart(fig_type, use_container_width=True)

# Top Genre
with col_right:
    st.subheader("Top 10 Genre Netflix")
    genres = filtered_df["genres"].dropna().str.split(", ").explode()
    top_genres = genres.value_counts().head(10).reset_index()
    top_genres.columns = ["Genre", "Count"]

    fig_genre = px.bar(
        top_genres,
        x="Genre",
        y="Count",
        color="Count",
        color_continuous_scale="reds"
    )
    st.plotly_chart(fig_genre, use_container_width=True)

# ======================
# TREND LINE
# ======================
st.subheader("Tren Penambahan Konten per Tahun")

yearly = filtered_df["year_added"].value_counts().sort_index().reset_index()
yearly.columns = ["Year", "Total"]

fig_trend = px.line(
    yearly,
    x="Year",
    y="Total",
    markers=True
)

st.plotly_chart(fig_trend, use_container_width=True)

# ======================
# CLUSTERING SECTION
# ======================
st.divider()
st.subheader("🔍 Segmentasi Konten Netflix (Clustering)")
st.write(
    "Konten dikelompokkan menggunakan metode K-Means "
    "berdasarkan tahun rilis dan durasi."
)

cluster_df = filtered_df[
    ["release_year", "duration_number"]
].dropna()

scaler = StandardScaler()
scaled_features = scaler.fit_transform(cluster_df)

kmeans = KMeans(n_clusters=3, random_state=42)
cluster_df["cluster"] = kmeans.fit_predict(scaled_features)

fig_cluster = px.scatter(
    cluster_df,
    x="release_year",
    y="duration_number",
    color="cluster",
    labels={
        "release_year": "Tahun Rilis",
        "duration_number": "Durasi",
        "cluster": "Cluster"
    },
    title="Clustering Konten Netflix"
)

st.plotly_chart(fig_cluster, use_container_width=True)
