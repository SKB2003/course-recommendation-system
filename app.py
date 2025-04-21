import streamlit as st
import pandas as pd
from recommend import get_resume_recommendations, get_filtered_courses
from utils import read_resume_text, load_course_data

st.set_page_config(page_title="AI Course Recommender", layout="wide")
st.title("🎓 AI-Powered Course Recommendation System")

# Load default dataset or uploaded one
if 'df' not in st.session_state:
    st.session_state.df = load_course_data("data/10k_bigdata_course_dataset.csv")

# Sidebar upload option for new dataset
with st.sidebar:
    st.header("📂 Upload New Course Dataset")
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.success("Dataset loaded successfully!")

# Tabs for each feature
resume_tab, user_tab = st.tabs(["📄 Resume-Based Recommendation", "🔍 User-Based Filtering"])

# ========== Resume-Based Recommendation ==========
with resume_tab:
    st.subheader("Upload Your Resume (.txt)")
    resume_file = st.file_uploader("Choose your resume file", type="txt")

    if resume_file is not None:
        resume_text = read_resume_text(resume_file)
        top_courses = get_resume_recommendations(resume_text, st.session_state.df)
        st.success("Top 10 Recommended Courses Based on Your Resume")
        st.dataframe(top_courses)

# ========== User-Based Filtering ==========
with user_tab:
    st.subheader("Filter Courses Based on Your Preference")
    df = st.session_state.df

    col1, col2, col3 = st.columns(3)
    domain = col1.selectbox("Domain", ["All"] + sorted(df['domain'].dropna().unique().tolist()))
    platform = col2.selectbox("Platform", ["All"] + sorted(df['platform'].dropna().unique().tolist()))
    level = col3.selectbox("Level", ["All"] + sorted(df['level'].dropna().unique().tolist()))

    col4, col5 = st.columns(2)
    duration = col4.slider("Max Duration (Hours)", 1, 100, 50)
    price = col5.slider("Max Price", 0, 100, 50)

    filtered_courses = get_filtered_courses(df, domain, platform, level, duration, price)
    st.success(f"Found {len(filtered_courses)} matching courses")
    st.dataframe(filtered_courses.reset_index(drop=True))
