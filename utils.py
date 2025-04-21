import pandas as pd

def read_resume_text(file):
    return file.read().decode("utf-8")

def load_course_data(path):
    df = pd.read_csv(path)
    required_cols = ['course_id', 'course_name', 'platform', 'domain', 'level', 'rating', 'enrollments', 'duration_hours', 'language', 'price', 'prerequisites']
    df = df[[col for col in required_cols if col in df.columns]]
    return df
