News Sentiment Analyzer
📌 Overview
The News Sentiment Analyzer is a Streamlit-based web application that fetches news articles about a company, performs sentiment analysis, translates the summary into Hindi, and generates a Hindi audio output.

✨ Features
Fetches news articles from NewsAPI and GNews.

Analyzes the sentiment of the articles (Positive, Negative, Neutral).

Provides a comparative sentiment analysis through a bar chart.

Translates the summarized text into Hindi.

Converts the translated summary into speech using gTTS.

🛠️ Tech Stack
Frontend: Streamlit

Backend: Python

APIs: NewsAPI, GNews

Libraries:

streamlit

requests

gtts

langdetect

vaderSentiment

matplotlib

googletrans

🚀 Installation & Setup
Prerequisites

Install Python (>=3.7)

Get API keys from:
NewsAPI
GNews

Steps to Run Locally

Clone the repository:
git clone https://github.com/Rinsila02/News-Sentiment-Analyzer.git  
cd News-Sentiment-Analyzer  

Create a virtual environment (optional but recommended):
python -m venv venv  
source venv/bin/activate  # For macOS/Linux  
venv\Scripts\activate  # For Windows

Install dependencies:
pip install -r requirements.txt  

Run the Streamlit app:
streamlit run app.py  

Open in browser: The app will start on http://localhost:8501.

🏗️ Deployment (Hugging Face Spaces)
The app is deployed on Hugging Face Spaces. You can access it here.

🤝 Contributing
Pull requests are welcome!

📬 Contact
For any queries, reach out via email at rinsilanabeesa2002@gmail.com
