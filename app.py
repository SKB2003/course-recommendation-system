import streamlit as st
import pandas as pd
from recommend import get_resume_recommendations, get_filtered_courses
from resume_parser import parse_resume

st.set_page_config(page_title="Course Recommender", layout="wide")

st.title("🎯 AI-Powered Course Recommendation System")

st.sidebar.title("📁 Uploads & Filters")
dataset_file = st.sidebar.file_uploader("Upload a Course Dataset (CSV)", type="csv")
resume_file = st.sidebar.file_uploader("Upload Resume (Text File)", type=["txt"])
selected_domain = st.sidebar.text_input("Enter Preferred Domain (e.g. Data Science, Cloud)")

if dataset_file:
    df = pd.read_csv(dataset_file)
else:
    df = pd.read_csv("10k_bigdata_course_dataset.csv")

if selected_domain:
    filtered_courses = get_filtered_courses(df, selected_domain)
    st.subheader("📌 Courses Based on Domain Filter")
    st.write(filtered_courses)

if resume_file:
    resume_text = resume_file.read().decode("utf-8")
    extracted_skills = parse_resume(resume_text)
    st.subheader("🧠 Resume-Based Course Recommendations")
    st.write("**Extracted Skills from Resume:**", extracted_skills)
    recommended_courses = get_resume_recommendations(df, extracted_skills)
    st.write(recommended_courses)
