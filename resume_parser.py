import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")

def parse_resume(text):
    text = re.sub(r"[^a-zA-Z ]", "", text)
    text = text.lower()
    stop_words = set(stopwords.words("english"))
    words = [word for word in text.split() if word not in stop_words and len(word) > 2]
    return list(set(words))
