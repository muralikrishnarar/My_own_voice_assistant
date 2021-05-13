import speech_recognition as sr
import pyttsx3
from datetime import datetime
import wikipedia
import webbrowser
from googleapiclient.discovery import build
import requests
import json

api_key = 'AIzaSyDLXnvSP2Exf4JZAdDpT-WuCK4HLRGQiDc'
youtube = build('youtube', 'v3', developerKey=api_key)
help_command = "I am Friday. How can I help you ?"
engine = pyttsx3.init('sapi5')
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[1].id)
r = sr.Recognizer()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wish_me():
    """  This Function is used for wishing the person greeting oof the day based on
      what time it is.
      Input : it take hour from datetime now in 24 hour format
      Output: Speak out Greetings
      """
    hour = int(datetime.now().hour)
    if hour <= 12:
        speak("Good morning")
    elif 12 < hour <= 18:
        speak("Good Afternoon")
    elif 18 < hour <= 24:
        speak("Good Evening")
    else:
        speak("You are not earth ")
    speak(help_command)


def take_command():
    with sr.Microphone() as source:
        speak("I am Listening....")
        r.pause_threshold = 1
        text = r.listen(source)

        try:
            recognised_text = r.recognize_google(text)
            print(recognised_text)
            speak(recognised_text)

        except sr.UnknownValueError or sr.RequestError:
            speak("Can you Repeat please?")
    return recognised_text


def wiki_search():
    search_text = take_command()
    qurey = wikipedia.summary(search_text, sentences=2)
    speak(qurey)


def youtube_search():
    search_text = take_command()
    webbrowser.open("https://www.youtube.com/results?search_query=" + search_text)


def google_search():
    search_text = take_command()
    webbrowser.open(
        "https://www.google.com/search?sxsrf=ALeKk03Fqt3NF54kl8uSLFa9vIcsisZ2vg%3A1606455271216&source=hp&ei=54_AX9TgCuiC4-EP-oW5oAk&q=" + search_text + "&oq=orange+fruit&gs_lcp=CgZwc3ktYWIQAzILCC4QsQMQyQMQkwIyBwgAEBQQhwIyBQgAELEDMgIIADIHCAAQFBCHAjICCAAyBQgAELEDMgIIADICCAAyAggAOgQIIxAnOgQIABBDOgUIABCRAjoLCC4QsQMQxwEQowI6DQguELEDEMcBEKMCEEM6BwgAELEDEENQoAVY4hhgnRpoAHAAeAGAAZAFiAGyD5IBBzAuOS41LTGYAQCgAQGqAQdnd3Mtd2l6&sclient=psy-ab&ved=0ahUKEwiU8KSegKLtAhVowTgGHfpCDpQQ4dUDCAc&uact=5")


def play_youtube():
    query = take_command()
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=query
    )
    response = request.execute()
    search_text = response['items'][0]['id']['videoId']
    webbrowser.open("https://www.youtube.com/watch?v=" + search_text)


def share_price():
    query = take_command()
    url = (
            "https://financialmodelingprep.com/api/v3/search?query=" + query + "&limit=10&exchange=NASDAQ&apikey=674878522f196363484492950df596a9")
    response = requests.request("GET", url)
    a = json.loads(response.text)
    symbol = a[0]['symbol']
    speak(f"Symbol is {symbol}")
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + a[0][
        'symbol'] + "&interval=5min&apikey=2AQZO0C0U4FWMEF3"
    speak(100)
    response = requests.request("GET", url)

    a = json.loads(response.text)

    for x in a['Time Series (5min)']:
        for y in a['Time Series (5min)'][str(x)]:
            speak(f"{y[3:]} at {float(a['Time Series (5min)'][str(x)][str(y)])}")

        break
def covid_data():
    url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"
    query = take_command()

    querystring = {"country": query.title()}

    headers = {
        'x-rapidapi-key': "dbf3e507dfmshe181f5af81fe1b7p11ecf5jsna07124f3def4",
        'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    a = json.loads(response.text)
    speak(f"Total number of recovered are {float(a['data']['recovered'])}")
    speak(f"Total number of deaths are {float(a['data']['deaths'])}")
    speak(f"Total number of confirmed cases are {float(a['data']['confirmed'])}")


if __name__ == '__main__':
    wish_me()
    while True:
        search_text = take_command()
        if 'wikipedia' in search_text.lower():
            wiki_search()
        elif 'youtube' in search_text.lower():
            youtube_search()
        elif 'google' in search_text.lower():
            google_search()
        elif 'play' in search_text.lower():
            play_youtube()
        elif 'share' in search_text.lower() or 'stock' in search_text.lower():
            share_price()
        elif 'covid' in search_text.lower() or 'covid19' in search_text.lower() :
            covid_data()
        elif 'stop' in search_text.lower():
            exit(0)
         
