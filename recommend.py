import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_resume_recommendations(resume_text, df):
    df = df.copy()
    df = df.dropna(subset=['course_name', 'domain', 'prerequisites'])
    df['combined'] = df['course_name'].astype(str) + ' ' + df['domain'].astype(str) + ' ' + df['prerequisites'].astype(str)

    combined_text = [resume_text] + df['combined'].tolist()
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(combined_text)

    cos_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    df['similarity'] = cos_sim[0]
    top_courses = df.sort_values(by='similarity', ascending=False).head(10)

    return top_courses[['course_id','course_name','domain','similarity','platform','level','duration_hours','price','prerequisites']]

def get_filtered_courses(df, domain, platform, level, duration, price):
    query = df.copy()
    if domain != "All":
        query = query[query['domain'] == domain]
    if platform != "All":
        query = query[query['platform'] == platform]
    if level != "All":
        query = query[query['level'] == level]

    query = query[(query['duration_hours'] <= duration) & (query['price'] <= price)]
    return query[['course_id','course_name','domain','platform','level','duration_hours','price','prerequisites']].head(50)
