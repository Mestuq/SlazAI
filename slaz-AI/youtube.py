from pickle import FALSE, TRUE
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from youtube_transcript_api import YouTubeTranscriptApi

import logging
import io

import discord
import iniLoad
import os, sys
import iniLoad
import time

import requests
import json


async def youtubeUpdate(client,numberOfCheck):
    logging.warning('Loanching YouTube')
    lista=[]

    # Open Firefox
    #profile_path = '../files_conf/profile/'
    #fp = webdriver.FirefoxProfile(profile_path)
    #driver = webdriver.Firefox(fp, executable_path="/home/pi/Downloads/geckodriver")
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument(r"--user-data-dir=/home/pi/.config/chromium")
    options.add_argument(r'--profile-directory=Default')
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver',options=options)
    # Open your subscriptions
    driver.get("https://www.youtube.com/feed/subscriptions")

    # Wait page to load
    logging.warning('Waiting...')
    time.sleep(15)
    logging.warning('Waiting ended')

    text=''
    # After this text url of any video can be found
    textRecognize='videoId\":\"'
    lookUp=FALSE;
    grabbedUrl=''

    amountOfLoading=0
    # Find all the videos is webpage
    for line in driver.page_source:
        for character in line:
            if amountOfLoading < numberOfCheck:
                text+=character

                if lookUp == TRUE:
                    if character != '\"':
                        grabbedUrl+=character
                    else:
                        lookUp=FALSE
                        if len(grabbedUrl)!=0:
                            amountOfLoading=amountOfLoading+1
                            bylo=FALSE
                            searchfile = io.open('../files_conf/'+"YoutubeCeche.txt", mode="r", encoding="utf-8")
                            for search in searchfile:
                                if search == grabbedUrl+"\n":
                                        bylo=True
                            searchfile.close()
                            if bylo == FALSE:
                                # If this video was alreaty found
                                searchfile = io.open('../files_conf/'+"YoutubeCeche.txt", mode="a", encoding="utf-8")
                                searchfile.write(grabbedUrl+"\n")
                                searchfile.close()

                                # ----------------- AI FEATURE ----------------- 

                                transcript_text = ""
                                try:
                                    transcript = YouTubeTranscriptApi.get_transcript(grabbedUrl, languages=['pl'])
                                    transcript_text = " ".join([entry['text'] for entry in transcript])
                                except Exception as e:
                                    print(f"Transcription error: {e}")

                                if len(transcript_text) > 6000:
                                    transcript_text[:6000]
                                if len(transcript_text) > 100:

                                    ai_api_key=iniLoad.iniLoad('dane.conf','AI','api_key','0')
                                    
                                    response_AI = requests.post(
                                    url="https://openrouter.ai/api/v1/chat/completions",
                                    headers={
                                        "Authorization": f"Bearer {ai_api_key}"
                                    },
                                    data=json.dumps({
                                        "model": "google/gemini-flash-1.5",
                                        "messages": [
                                        {
                                            "role": "user",
                                            "content": "Poniższy tekst to transkrypcja filmu. Twoim zadaniem jest przygotowanie krótkiego streszczenia treści całego filmu. Oto treść filmu: ``` "+transcript_text+"  ```"
                                        }
                                        ],
                                        "max_tokens": 500
                                        
                                    })
                                    )
                                    if response_AI.status_code == 200:
                                        response_content = response_AI.json()
                                        if 'choices' in response_content and len(response_content['choices']) > 0:
                                            summary = response_content['choices'][0]['message']['content']
                                            print(summary)
                                            lista.append(summary + "<:AI:1314942990472712222>")

                                # ----------------- AI FEATURE ----------------- 

                                logging.warning('https://www.youtube.com/watch?v='+grabbedUrl)
                                lista.append('https://www.youtube.com/watch?v='+grabbedUrl)
                            
                            
                if text[-len(textRecognize):] == textRecognize:
                    grabbedUrl=''
                    lookUp=TRUE
    driver.close()

    # Get a discord channel from dane.conf
    youtubeChannelName = iniLoad.iniLoad('dane.conf','YoutubeModule','Channel','User not found')
    channel = discord.utils.get(client.get_all_channels(), name=youtubeChannelName)

    logging.warning('Youtube finished')
    # Send the result SLOWLY
    for wiersz in lista:
        time.sleep(0.5)
        await channel.send(wiersz)




