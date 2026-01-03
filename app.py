import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    layout="wide"
)

# ======================
# MODERN NETFLIX CSS
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
# SIDEBAR
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
# TITLE
# ======================
st.title("📊 Netflix Content Analytics")
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
# CHARTS (PLOTLY)
# ======================
col_left, col_right = st.columns(2)

# Content Type Chart
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

# Top Genres
with col_right:
    st.subheader("Top 10 Genre")
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
