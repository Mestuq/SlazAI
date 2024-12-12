import discord
import iniLoad
import os, sys
import io
import iniLoad
import time
import logging
import urllib.request

import requests
import json

#Anime update command
async def animenews(client):

    # Get channel from dane.conf
    animeChannelName = iniLoad.iniLoad('dane.conf','AnimeModule','Channel','User not found')
    logging.warning('animeChannelName')
    channel = discord.utils.get(client.get_all_channels(), name=animeChannelName)

    # 0 - series 1 - movies
    for iteration in range(2):
        # Get webpage content (with upcoming animes) and save it to the ceche file.
        if iteration == 0:
            fp = urllib.request.urlopen("https://www.animenewsnetwork.com/encyclopedia/anime/upcoming/tv")
        if iteration == 1:
            fp = urllib.request.urlopen("https://www.animenewsnetwork.com/encyclopedia/anime/upcoming/movie")
        
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()
        with io.open('../files_conf/'+"ceche.txt", "w", encoding="utf-8") as f:
            f.write(mystr)
        
        # local variables usefull for extracting data from webpage
        #lista=[]
        file = io.open('../files_conf/'+"ceche.txt", mode="r", encoding="utf-8")
        act1=""
        waitforquotation=False  #koniec szukania jest w znaku "
        waitforLower=False      #koniec szukania jest w znaku <
        actType=""
        sleepMe=True
        Finish=False
        
        # Received information from webpage
        imageurl=""
        infourl=""
        nameurl=""
        dateurl=""

        for line in file:
            for character in line:
                if sleepMe==False and Finish==False:
                    #print(act1)
                        #INTELIGENTNA ANALIZA
                    if act1=="img src=":
                        print("Szukam Obrazka")
                        waitforquotation=True
                        actType="Image"
                        act1=""
                    elif act1=="a href=":
                        print("Szukam Info")
                        waitforquotation=True
                        actType="Info"
                        act1=""
                    elif act1==" class=ENCYC>":
                        print("Szukam Nazwy")
                        waitforLower=True
                        actType="Name"
                        act1=""
                    elif act1=="td>":
                        print("Szukam Daty")
                        waitforLower=True
                        actType="Date"
                        act1=""
                        
                    elif waitforLower==True:
                        if character=="<":
                            waitforLower=False
                            if actType=="Name":
                                nameurl=act1
                                act1=""
                                print(nameurl)
                            if actType=="Date":
                                dateurl=act1
                                act1=""
                                print(dateurl)
                                #dodawanie anime do PLIKU
                                
                                bylo=False
                                #jeżeli anime nie było wcześniej prezentowane 
                                searchfile = io.open('../files_conf/'+"anime_saved.txt", mode="r", encoding="utf-8")

                                for search in searchfile:
                                    if search == nameurl+"\n":
                                        bylo=True
                                searchfile.close()
                                print(bylo)
                                
                                if bylo==False:
                                    searchfile = io.open('../files_conf/'+"anime_saved.txt", mode="a", encoding="utf-8")
                                    searchfile.write(nameurl+"\n")
                                    searchfile.close()
                                    #lista.append("**         Ogłoszono nowe Anime!**\n**"+nameurl+"** \nPremiera planowana jest na: " +dateurl+"\nWięcej informacji znajdziesz na: \n"+infourl+"\n"+imageurl+"\n")

                                    # ----------------- AI FEATURE ----------------- 
                                    ai_description = ""

                                    if len(nameurl) > 10:

                                        ai_api_key=iniLoad.iniLoad('dane.conf','AI','api_key','0')
                                        
                                        response_AI = requests.post(
                                        url="https://openrouter.ai/api/v1/chat/completions",
                                        headers={
                                            "Authorization": f"Bearer {ai_api_key}"
                                        },
                                        data=json.dumps({
                                            "model": "perplexity/llama-3.1-sonar-large-128k-online",
                                            "messages": [
                                            {
                                                "role": "user",
                                                "content": "Wyjaśnij krótko na czym polega historia nadchodzącego anime \""+nameurl+"\". Nie wchodź w szczegóły."
                                            }
                                            ],
                                            "max_tokens": 500
                                            
                                        })
                                        )
                                        if response_AI.status_code == 200:
                                            response_content = response_AI.json()
                                            if 'choices' in response_content and len(response_content['choices']) > 0:
                                                ai_description = response_content['choices'][0]['message']['content'] + " (AI)"
                                                
                                                for i in range(1, 15): 
                                                    ai_description = ai_description.replace(f"[{i}]", "")

                                                print(ai_description)
                                                
                                                #await channel.send(summary)
                                                #await channel.send("<:AI:1314942990472712222>")

                                    # ----------------- AI FEATURE ----------------- 



                                    fildLargeImage=''
                                    if imageurl == "":
                                        fildLargeImage="https://cdn.discordapp.com/attachments/801861475395698740/1025787436988645506/unknown.png"
                                    else:
                                        for letter in imageurl:
                                            fildLargeImage=fildLargeImage+letter
                                            if letter == '/':
                                                fildLargeImage=''
                                        fildLargeImage='https://www.animenewsnetwork.com/images/encyc/'+fildLargeImage
                                        
                                    embed = discord.Embed(
                                        title = nameurl,
                                        description = ai_description, #"Premiera planowana jest na: " +dateurl,
                                        colour = discord.Colour.blue(),
                                        url=infourl
                                    )
                                    embed.set_footer(text="Premiera planowana jest na: " +dateurl)
                                    embed.set_image(url=fildLargeImage)
                                    #embed.set_author(name='Ogłoszono nowe anime!')

                                    await channel.send(embed=embed)
                                    time.sleep(0.5)

                                nameurl=""
                                dateurl="data jeszcze nie określona"
                                infourl="brak informacji"
                                imageurl=""
                                fildLargeImage=""
                                    
                    elif waitforquotation==True:
                        if character=="\"":
                            waitforquotation=False
                            if actType=="Image":
                                imageurl="https:"+act1+"\n"
                                act1=""
                                print(imageurl)
                            if actType=="Info":
                                infourl="https://www.animenewsnetwork.com"+act1
                                act1=""
                                print(infourl)
                            act1="" #ZEROWANIE ACT1
                            
                    if act1=="/table":
                        print("END")
                        Finish=True
                    #SZUKANIE TYLKO W DANYM OBRĘBIE
                if act1=="table":
                    print("START")
                    sleepMe=False
                    #WYSZUKIWANIE ZNAKÓW
                if character=='<':
                    act1=""
                elif character!='\"':
                    act1+=character
        file.close()
    


    # Send the result SLOWLY
    #for wiersz in lista:
    #    time.sleep(0.5)
    #    await channel.send(wiersz)
    
    
    
