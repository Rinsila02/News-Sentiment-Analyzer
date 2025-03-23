import streamlit as st
import pandas as pd
import requests
from gtts import gTTS
import os
import time
from langdetect import detect
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from deep_translator import GoogleTranslator

analyzer = SentimentIntensityAnalyzer()
translator = GoogleTranslator(source="auto", target="hi")

def get_news_articles(company_name, newsapi_key, gnews_key):
    articles = []

    url_newsapi = f"https://newsapi.org/v2/everything?q={company_name}&language=en&apiKey={newsapi_key}"
    response = requests.get(url_newsapi)
    if response.status_code == 200:
        data = response.json()
        for article in data["articles"]:
            if detect(article["title"]) == "en":
                articles.append({
                    "Title": article["title"],
                    "Summary": article.get("description", "No Summary"),
                    "Link": article["url"]
                })

    url_gnews = f"https://gnews.io/api/v4/search?q={company_name}&lang=en&token={gnews_key}"
    response = requests.get(url_gnews)
    if response.status_code == 200:
        data = response.json()
        for article in data["articles"]:
            if detect(article["title"]) == "en":
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
    sentiment_counts = df["Sentiment"].value_counts()

    fig, ax = plt.subplots()
    sentiment_counts.plot(kind="bar", color=["green", "red", "gray"], ax=ax)
    ax.set_title("Sentiment Distribution")
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Count")
    st.pyplot(fig)

def text_to_speech(text):
    tts = gTTS(text=text, lang="hi", slow=False)
    filename = "summary.mp3"
    tts.save(filename)
    return filename

def translate_text(text, target_lang="hi"):
    return GoogleTranslator(source="auto", target=target_lang).translate(text)

st.title("🔍 News Sentiment Analyzer")

company_name = st.text_input("Enter Company Name", "Tata Group")
newsapi_key = "7f4483bf3be942aea2fecbc28fe061f2"
gnews_key = "01ab171369773ded4e52412adc58b4a7"

df = None

if st.button("Fetch News"):
    st.write(f"Fetching news for: **{company_name}**")

    df = get_news_articles(company_name, newsapi_key, gnews_key)

    if df.empty:
        st.warning("No articles found. Try a different company.")
    else:
        df["Sentiment"] = df["Summary"].apply(get_sentiment)
        st.write("### Sentiment Analysis Report")
        st.dataframe(df)

        st.write("### Comparative Sentiment Analysis")
        comparative_analysis(df)

        summary_text = " ".join(df["Summary"].tolist())
        st.write("### Summary Text (Original):")
        st.write(summary_text)

        translated_summary = translate_text(summary_text, target_lang="hi")
        st.write("### Translated Summary Text (Hindi):")
        st.write(translated_summary)

        audio_file = text_to_speech(translated_summary)
        st.audio(audio_file)
