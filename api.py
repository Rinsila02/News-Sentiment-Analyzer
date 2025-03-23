import os
import requests
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from gtts import gTTS

app = FastAPI()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "7f4483bf3be942aea2fecbc28fe061f2")
GNEWS_KEY = os.getenv("GNEWS_KEY", "01ab171369773ded4e52412adc58b4a7")

analyzer = SentimentIntensityAnalyzer()

def get_news_articles(company_name):
    articles = []

    url_newsapi = f"https://newsapi.org/v2/everything?q={company_name}&language=en&apiKey={NEWSAPI_KEY}"
    response = requests.get(url_newsapi)
    if response.status_code == 200:
        data = response.json()
        for article in data.get("articles", []):
            articles.append({
                "Title": article["title"],
                "Summary": article.get("description", "No Summary"),
                "Link": article["url"]
            })

    url_gnews = f"https://gnews.io/api/v4/search?q={company_name}&lang=en&token={GNEWS_KEY}"
    response = requests.get(url_gnews)
    if response.status_code == 200:
        data = response.json()
        for article in data.get("articles", []):
            articles.append({
                "Title": article["title"],
                "Summary": article.get("description", "No Summary"),
                "Link": article["url"]
            })

    return pd.DataFrame(articles[:10])

def get_sentiment(text):
    if not text or text.strip() == "":
        return "Neutral"
    score = analyzer.polarity_scores(text)["compound"]
    return "Positive" if score > 0.05 else "Negative" if score < -0.05 else "Neutral"

def comparative_analysis(df):
    sentiment_counts = df["Sentiment"].value_counts().to_dict()
    total_articles = len(df)
    analysis = {
        "Total Articles": total_articles,
        "Positive": sentiment_counts.get("Positive", 0),
        "Negative": sentiment_counts.get("Negative", 0),
        "Neutral": sentiment_counts.get("Neutral", 0),
    }
    return analysis

def text_to_speech(text):
    tts = gTTS(text=text, lang="hi")
    filename = "summary.mp3"
    tts.save(filename)
    return filename

def fetch_news_and_analyze(company_name):
    df = get_news_articles(company_name)
    if df.empty:
        return {"error": "No articles found."}

    df["Sentiment"] = df["Summary"].apply(get_sentiment)
    analysis = comparative_analysis(df)
    summary_text = " ".join(df["Summary"].dropna().tolist())
    audio_file = text_to_speech(summary_text)

    return {
        "news": df.to_dict(orient="records"),
        "analysis": analysis,
        "tts_file": audio_file
    }

@app.get("/")
def home():
    return {"message": "API is running successfully!"}

@app.get("/fetch_news/{company_name}")
def fetch_news(company_name: str):
    return fetch_news_and_analyze(company_name)

@app.get("/play_tts")
def play_tts():
    tts_file_path = "summary.mp3"

    if os.path.exists(tts_file_path):
        return FileResponse(tts_file_path, media_type="audio/mpeg")
    else:
        return {"error": "TTS file not found"}
