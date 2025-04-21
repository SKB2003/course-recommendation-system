import streamlit as st
import pandas as pd
from recommend import get_resume_recommendations
from resume_parser import parse_resume

st.set_page_config(page_title="Course Recommender", layout="wide")
st.title("🎯 AI-Powered Course Recommendation System")

st.sidebar.title("📁 Uploads & Filters")

# Uploading files
dataset_file = st.sidebar.file_uploader("Upload a Course Dataset (CSV)", type="csv")
resume_file = st.sidebar.file_uploader("Upload Resume (Text File)", type=["txt"])

# Filters
selected_domain = st.sidebar.text_input("Enter Preferred Domain (e.g. Data Science, Cloud)")
selected_level = st.sidebar.selectbox("Select Level", ["", "Beginner", "Intermediate", "Advanced"])
selected_platform = st.sidebar.selectbox("Select Platform", ["", "Coursera", "Udemy", "edX", "DataCamp"])
price_range = st.sidebar.slider("Select Price Range", 0, 10000, (0, 2000))
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.0, 0.1)

# Load dataset
if dataset_file:
    df = pd.read_csv(dataset_file)
else:
    df = pd.read_csv("10k_bigdata_course_dataset.csv")

# User Input Based Course Filtering
if selected_domain or selected_level or selected_platform or price_range or min_rating:
    st.subheader("📌 User Input Based Course Recommendations")

    filtered_df = df.copy()

    if selected_domain:
        filtered_df = filtered_df[filtered_df['Domain'].str.contains(selected_domain, case=False, na=False)]
    if selected_level:
        filtered_df = filtered_df[filtered_df['Level'].str.lower() == selected_level.lower()]
    if selected_platform:
        filtered_df = filtered_df[filtered_df['Platform'].str.lower() == selected_platform.lower()]
    
    filtered_df = filtered_df[
        (filtered_df['price'] >= price_range[0]) & 
        (filtered_df['price'] <= price_range[1]) & 
        (filtered_df['rating'] >= min_rating)
    ]

    st.write(f"Found {len(filtered_df)} courses matching your preferences:")
    st.dataframe(filtered_df.head(10))

# Resume-Based Recommendation
if resume_file:
    resume_text = resume_file.read().decode("utf-8")
    extracted_skills = parse_resume(resume_text)
    st.subheader("🧠 Resume-Based Course Recommendations")
    st.write("**Extracted Skills from Resume:**", extracted_skills)
    recommended_courses = get_resume_recommendations(df, extracted_skills)
    st.write(recommended_courses)
