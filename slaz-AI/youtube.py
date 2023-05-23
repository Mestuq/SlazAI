from pickle import FALSE, TRUE
from selenium import webdriver

import logging
import io

import discord
import iniLoad
import os, sys
import iniLoad
import time


async def youtubeUpdate(client,numberOfCheck):
    logging.warning('Loanching YouTube')
    lista=[]

    # Open Firefox
    profile_path = '../files_conf/profile/'
    fp = webdriver.FirefoxProfile(profile_path)
    driver = webdriver.Firefox(fp)

    # Open your subscriptions
    driver.get("https://www.youtube.com/feed/subscriptions")

    # Wait page to load
    logging.warning('Waiting...')
    time.sleep(20)
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




