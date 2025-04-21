from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def get_resume_recommendations(df, extracted_skills):
    df = df.copy()
    
    # Use Course Name only since no Course Description
    df["course_combined"] = df["Course Name"].fillna("")
    
    resume_text = " ".join(extracted_skills)
    
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["course_combined"].tolist() + [resume_text])
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    
    df["similarity_score"] = cosine_sim[0]
    top_recommendations = df.sort_values(by="similarity_score", ascending=False).head(10)
    return top_recommendations[["Course Name", "similarity_score"]]

def get_filtered_courses(df, selected_domain):
    return df[df["Course Name"].str.contains(selected_domain, case=False, na=False)].head(10)
