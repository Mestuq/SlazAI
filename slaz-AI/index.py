import os
import sys
import logging
from pickle import FALSE
from datetime import datetime, timedelta
from threading import Timer
from pathlib import Path 
import io
import time
import requests
import pathlib
import aiohttp
import atexit 


#Discord.py libraries
import discord
from discord.ext import commands

# "Clever answears" script
import response
# Special commands script
import advancedcommands
# File load/save script
import iniLoad

# Youtube sync script
import youtube
# Anime new sync script
import anime
# Word splitter
import commandrecognazer

import autoduo.auto

# Bots will wait to stable connection
logging.warning('Waiting for connection')
connectionActive=0

while connectionActive<3:
    try:
        requests.head("http://www.google.com/", timeout=3)
        connectionActive=connectionActive+1
    except requests.ConnectionError:
        logging.warning('Connection Error')
        connectionActive=0
    time.sleep(3)
time.sleep(2)

# Change script relative files dir
os.chdir(os.path.dirname(sys.argv[0]))

# Bot now works
logging.warning('Bot starting now!')

client = discord.Client()
guild = discord.Guild

# 'be silient' feature
send_this_when_free=''
silient_mode=False
def after_silience():
    global silient_mode
    silient_mode=False


VALID_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp'}
message_image_log = []

def clean_log():
    one_hour_ago = datetime.now() - timedelta(hours=1)
    global message_image_log
    message_image_log = [entry for entry in message_image_log if entry[0] >= one_hour_ago]

# On message Event
@client.event
async def on_message(message):
    #try:
    # Is private message
    if isinstance(message.channel, discord.channel.DMChannel):
        await message.author.send("Ze względów bezpieczeństwa, ze ślazatkem można się kontaktować tylko na serwerze Mroczne Zakątki.")
        return
    if True:

        # Cache recent messages for AI context.
        global message_image_log
        clean_log()
        attachment_list = []
        if message.attachments:
            for attachment in message.attachments:
                filename, file_extension = os.path.splitext(attachment.filename)
                file_extension = file_extension.lower() 
                if file_extension in VALID_IMAGE_EXTENSIONS:
                    print(attachment)
                    attachment_list.append(attachment.proxy_url) 
        message_image_log.append((datetime.now(), message.author.name, message.content, attachment_list))
        # -------------------------------------

        global silient_mode
        global send_this_when_free

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        # save all the messagess as the log in file
        f=open("../files_conf/log.txt", "a+")
        f.write(dt_string+" // "+message.author.name+" : \""+message.content+"\"\n")

        # Ceche Users information
        _cecheGroupName=str(message.author.id)
        iniLoad.iniChange("dane.conf",_cecheGroupName,'name',str(message.author.name))
        iniLoad.iniChange("dane.conf",_cecheGroupName,'avatar',str(message.author.avatar_url))
        iniLoad.iniChange("dane.conf",_cecheGroupName,'display_name',str(message.author.display_name))
        iniLoad.iniChange("dane.conf",_cecheGroupName,'discriminator',str(message.author.discriminator))
        iniLoad.iniChange("dane.conf",_cecheGroupName,'hash',str(hash(message.author)))
        
        # Ignore others bots message
        channel = message.channel
        if message.author.bot:
            return
        
        # If bot is in a silient mode
        if send_this_when_free != '':
            await channel.send(send_this_when_free)
            send_this_when_free=''
        
        # Store a message content as table of splitted words. First one, is ignoring letter duplicates and changes BIG LETTER to small.
        tabela=commandrecognazer.word_in_message(message.content,False)                                                           #tabela wyrazów z małej litery i bez powtórzeń
        tabela_pierwotna=commandrecognazer.word_in_message(message.content,True)                                                  #tabela wyrazów pierwotnych
        
        # Check if bot have a clever answear for this message
        resp = response.response_list(tabela,tabela_pierwotna,channel,guild,message,client)                     #standardowe pytania i odpowiedzi
        
        # Then check if this message is a special command
        resp2 = await advancedcommands.response_list(tabela,tabela_pierwotna,channel,guild,message,client,message_image_log)      #zaawansowane polecenia

        # Start/End silient mode
        if resp2 != '':
            resp=resp2
        if resp2 == '&start_silient':
            resp=''
            await channel.send('Dobra, będę cicho')
            silient_mode=True
            Timer(5*60, after_silience, args=None, kwargs=None).start()
        if resp2 == '&end_silient':
            resp=''
            after_silience()
            await channel.send('Ok')
        
        # Block user with inappropriate name
        tabela_usera=commandrecognazer.word_in_message(message.author.name,False)           
        if response.blacklist_usernames(tabela_usera)=='ban':
            resp='Pan ślazatek bezpieczenstwa pilnuje, '+message.author.name+' bana na serwera otrzymuje :)'
            await message.author.ban(reason = "System ślazatkowych zabezpieczeń wykrył zakazany nick")
            
        # If the response for message exist, then send a result
        if resp != '' and silient_mode==False:
            await channel.send(resp)
            
        f.close()

        # Do this once a day
        daily=""
            #create file if not exist
        fle = Path('../files_conf/daily.txt')
        fle.touch(exist_ok=True)
        filee = io.open('../files_conf/'+"daily.txt", mode="r", encoding="utf-8")
        for datee in filee:
            daily=datee
        filee.close()
        daily_do=dt_string = now.strftime("%d/%m/%Y")
        if daily_do!=daily:
            f2=io.open('../files_conf/'+"daily.txt", "w", encoding="utf-8")
            f2.write(daily_do)
            f2.close()
            ##co dzieje się codziennie:
            await anime.animenews(client)
            await youtube.youtubeUpdate(client,50)
            print("Daily commands done")


    #except aiohttp.ClientConnectorError:
    #    logging.warning('Connection error! Restart... ')
    #    os.execv(sys.executable, ['python3']+ [sys.argv[0]] )

@atexit.register 
def goodbye(): 
    logging.warning('Connection error! Restart... ')
    os.execv(sys.executable, ['python3']+ [sys.argv[0]] )

# Load bot token
# you can get one from here https://discord.com/developers/
got_id=iniLoad.iniLoad('dane.conf','Client','id','0')
if got_id == '0':
    # Input discord token 
    print('Enter discord bot token:')
    got_id = input()
    iniLoad.iniChange('dane.conf','Client','id',got_id)
    # Input username with special privilages
    print('Enter your discord username:')
    specialUser = input()
    iniLoad.iniChange('dane.conf','Client','admin',specialUser)
    print('Thanks, bot will start in a second')
client.run(got_id)
