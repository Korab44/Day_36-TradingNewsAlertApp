import requests
import datetime as dt
from twilio.rest import Client
import os

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

alpha_api_key = os.getenv("ALPHA_KEY")
news_api_key = os.getenv("NEWS_KEY")

twilio_sid = os.getenv("TWILIO_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH")

current_date = dt.datetime.now()
previous_date = current_date - dt.timedelta(days=1)
compared_date = current_date - dt.timedelta(days=2)
c_date = compared_date.strftime('%Y-%m-%d')
p_date = previous_date.strftime('%Y-%m-%d')

stock_endpoint = f'https://www.alphavantage.co/query'
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": COMPANY_NAME,
    "apikey": alpha_api_key,
}
r = requests.get(stock_endpoint, stock_params)
r.raise_for_status()
now_date = float(r.json()["Time Series (Daily)"][p_date]["4. close"])
previous_date = float(r.json()["Time Series (Daily)"][c_date]["4. close"])

difference = abs(now_date - previous_date)
diff_precent = (difference / now_date) * 100
if diff_precent > 5:
    news_params = {
        "q": COMPANY_NAME,
        "apiKey": news_api_key
    }
    response = requests.get("https://newsapi.org/v2/everything", params=news_params)
    data_articles = response.json()["articles"]
    three_articles = data_articles[:3]
    formatted_aritcles = [f'Headline: {article["title"]}. \nBrief: {article["description"]}.' for article in three_articles]
    client = Client(twilio_sid, twilio_auth_token)
    for article in formatted_aritcles:
        message = client.messages.create(
            body=article,
            from_="+19707139915",
            to="+38344244111"
        )



