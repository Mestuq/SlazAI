from io import StringIO
from pickle import TRUE
import discord
import time
import os
import sys
import subprocess
import netifaces

import codecs

import base64
from datetime import datetime
import iniLoad
import anime
import youtube

# Gamejam topics
import gamejam

import requests
import json

import autoduo.auto

poczekaj=0

def url_to_base64(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        base64_image = base64.b64encode(response.content).decode('utf-8')
        return base64_image
    except requests.RequestException as e:
        print(f"Error fetching the image: {e}")
        return None

def check_mime_type(url):
    try:
        response = requests.head(url)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type')
        if content_type:
            print(f"MIME Type of {url}: {content_type}")
            return content_type
        else:
            print(f"No Content-Type header found for {url}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def unprecised_command(mess,requir):
    for req in requir:
        fulfills=False
        for mes in mess:
            if req == mes:
                fulfills=True
        if fulfills == False:
            return False
    return True

def get_formatted_messages(message_log, include_images=True):
    messages = []
    for log_entry in message_log:
        timestamp, author, content, attachment_list = log_entry
        role = "user" if author != "Ślazatek" else "assistant"
        
        content_list = []
        
        # Add the text content
        if content:
            content_list.append({
                "type": "text",
                "text": author + " : " + content + " "
            })
        
        # Add the image attachments if include_images is True
        if include_images:
            for attachment_url in attachment_list:
                base64_image = url_to_base64(attachment_url)
                mime_type = check_mime_type(attachment_url)
                content_list.append({
                    "type": "image_url",
                    "image_url": {
                        "url":  f"data:{mime_type};base64,{base64_image}"
                    }
                })
        
        messages.append({
            "role": role,
            "content": content_list if content_list else content
        })
    
    return messages

# Class/Struct matching username with their swears count
class v2:
    def __init__(self,ids,howmanys):
        self.ids=ids
        self.howmanys=howmanys
    def __repr__(self):
        return repr((self.ids,self.howmanys)) 

async def response_list(tabela,tabela_pierwotna,channel,guild,message,client,message_image_log):
    # pierszy element to '#'
    global poczekaj

    # Simple fix for table overflow
    for i in range(1,10):
        tabela.append('') 
        tabela_pierwotna.append('')

    # Create a new channel command 
    if tabela[0] == 'stwórz':
        if tabela[1] == 'mi':
            if tabela[2] == 'kanał':
                # Cool down if user do it too fast
                if poczekaj != datetime.now().minute  :
                    ilekanalow=0
                    nazwykanalow = message.guild.channels
                    # Check if the channel count limit is not reached
                    for kanaly in nazwykanalow:
                        ilekanalow+=1
                    if ilekanalow < 100:
                        nazwakanalu = tabela_pierwotna[3]
                        ds = await message.guild.create_text_channel(nazwakanalu)
                        cat = message.channel.category
                        await ds.edit(category=cat, overwrite=True)
                        await ds.edit(sync_permissions=True)
                        await ds.send('Kanał użytkownika: '+message.author.name)
                        poczekaj = datetime.now().minute
                        return 'Zrobione!'
                    else:
                        return 'Sorki ale jest na tym serwerze już '+str(ilekanalow)+", poczekaj na admina by powiększyć ten limit. Jeszcze raz przepraszam ale to jest pewna forma zabezpieczenia przed raidami."
                else:
                    return 'Poczekaj minutkę, nie chcę robić spamu'

    # Optional feature for github integration. More info in "extra/run_update.sh"
    if tabela[0] == 'aktualizuj':
        await channel.send('Poczekaj!')
        time.sleep(2.0)
        os.system('/home/pi/files/run_update.sh')
        sys.exit(0)
        return ''
    
    if unprecised_command(tabela,["co", "jest"]) \
        or unprecised_command(tabela,["który"]) \
        or unprecised_command(tabela,["kim"]) \
        or unprecised_command(tabela,["kto"]) \
        or unprecised_command(tabela,["ktury"]) \
        or unprecised_command(tabela,["skąd"]) \
        or unprecised_command(tabela,["z kąd"]) \
        or unprecised_command(tabela,["jak"]) \
        or unprecised_command(tabela,["gdzie"]) \
        or unprecised_command(tabela,["?"]) \
        or unprecised_command(tabela,["kiedy"]):
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")

        sarcastic_prompt = "Jesteś teraz na chat-cie discord na serwerze Mroczne Zakątki i piszesz tam pod pseudonimem Ślazatek. Piszesz teraz razem z innymi użytkownikami na serwerze. \
            Jest dzisiaj "+current_date+". \
            Pomagaj użytkownikom w razie potrzeby. \
            Odpowiadaj krótko, najlepiej w dwóch-trzech zdaniach."
        
        # Jeżeli ktoś przypadkiem popełni błąd ortograficzny w wiadomości to mu go złośliwie wypomnij. \

        print(get_formatted_messages(message_image_log))

        messages = [ 
            {
                "role": "system", 
                "content": [{
                    'type': 'text', 
                    'text': sarcastic_prompt
                }]
            } ] + get_formatted_messages(message_image_log)

        if len(message.content) > 10:

            ai_api_key=iniLoad.iniLoad('dane.conf','AI','api_key','0')
            
            response_AI = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {ai_api_key}"
            },
            data=json.dumps({
                "model": "google/gemini-flash-1.5",
                "messages": messages,
                "max_tokens": 200
                
            })
            )
            
            if response_AI.status_code == 200:
                response_content = response_AI.json()
                if 'choices' in response_content and len(response_content['choices']) > 0:
                    ai_answear = response_content['choices'][0]['message']['content']

                    if ai_answear.startswith("ŚlazGPT :"):
                        ai_answear = ai_answear[len("ŚlazGPT :"):].strip()
                    if ai_answear.startswith("ŚlazGPT:"):
                        ai_answear = ai_answear[len("ŚlazGPT:"):].strip()
                    if ai_answear.startswith("Ślazatek :"):
                        ai_answear = ai_answear[len("Ślazatek :"):].strip()
                    if ai_answear.startswith("Ślazatek:"):
                        ai_answear = ai_answear[len("Ślazatek:"):].strip()

                    ai_answear = ai_answear.replace("@Mestuq", "<@352808188338241536>").replace("@mestuq", "<@352808188338241536>")
                    ai_answear = ai_answear.replace("@Kasztan", "<@368814924144705549>").replace("@kasztan", "<@368814924144705549>")
                    ai_answear = ai_answear.replace("@Aztoja", "<@332452079908028418>").replace("@aztoja", "<@332452079908028418>")
                    ai_answear = ai_answear.replace("@Szklanka", "<@391237384899133441>").replace("@szklanka", "<@391237384899133441>")

                    # Delete AI emoji
                    for i in range(len("<:AI:1314942990472712222>"), 0, -1):
                        #print(f"<:AI:{'1314942990472712222>'[:i]}")
                        ai_answear = ai_answear.replace(f"<:AI:{'1314942990472712222>'[:i]}", "")
                    ai_answear = ai_answear.replace("<:AI:", "") 
                    ai_answear = ai_answear.replace("<:AI", "") 
                    ai_answear = ai_answear.replace("<:A", "")  # Final case

                    return ai_answear + "<:AI:1314942990472712222>"
            else:
                print(response_AI)





    # Show the ranking of swears
    if tabela[0] == 'pokaż':
        if tabela[1] == 'ranking':
            if tabela[2] == 'przekleństw':
                #plik = open('../files_conf/licznik.conf', "r")
                plik = codecs.open('../files_conf/licznik.conf',encoding="utf-16")
                resp="Ranking przekleństw: \n"

                # decompose file. "x" is one line of file
                _members=[]               
                for x in plik:
                    _type=False
                    _no=False
                    _id=''
                    _howmany=''
                    for y in x:
                        if y=='[':
                            _no=True
                        if y!='=':
                            if _type==False:
                                _id=_id+y
                            else :
                                _howmany=_howmany+y
                        if y=='=':
                            _type=True
                    _id=_id.strip()
                    _howmany=_howmany.strip()
                    if _no==False:
                        if _id != '':
                            _members.append(v2(int(_id),int(_howmany)))
                # sort from the highest value
                _members=sorted(_members,key=lambda v2: v2.howmanys)
                _members.reverse()
                # Use a ceche file of users information
                # return response for this command
                for x in _members:
                    resp=resp+'\n'+iniLoad.iniLoad('dane.conf',str(x.ids),'display_name','User not found')+' # '+str(x.howmanys)
                return resp
    
    # Open a vlc in host. In the future, it will be used for voice channel streaming
    if tabela_pierwotna[0] == 'vlc':
        if message.author.name == iniLoad.iniLoad('dane.conf','Client','admin',''):
            subprocess.call('vlc '+tabela_pierwotna[1], shell=True)
            return 'Trwa uruchamianie...'

    # Set this channel as a channel for anime notifications
    if tabela_pierwotna[0] == 'AnimeSetChannel':
        # Only admin can do this
        if message.author.name == iniLoad.iniLoad('dane.conf','Client','admin',''):
            iniLoad.iniChange("dane.conf",'AnimeModule','Channel',message.channel.name)
            return 'Ok'

    # Set this channel as a channel for youtube notifications 
    if tabela_pierwotna[0] == 'YoutubeSetChannel':
        if message.author.name == iniLoad.iniLoad('dane.conf','Client','admin',''):
            iniLoad.iniChange("dane.conf",'YoutubeModule','Channel',message.channel.name)
            return 'Ok'

    # Alternative command for &start_silient
    if tabela[0] == 'zamknij':
        if tabela[1] == 'ryj' or tabela[1] == 'morde':
            return '&start_silient'
    
     # Alternative command for &end_silient
    if tabela[0] == 'dobra':
        if tabela[1] == 'mów':
            return '&end_silient'
   
    # Get your local ip adress. Its really usefull for configuration if your ip adress is not static
    if tabela_pierwotna[0] == 'localip':
        if tabela_pierwotna[1] == '-':
            # Only admin can see it
            if message.author.name == iniLoad.iniLoad('dane.conf','Client','admin',''):
                iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
                return netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
    
    # Manual update of anime news
    if tabela_pierwotna[0] == 'animeupdate':
        await message.delete()
        await anime.animenews(client)

    # Manual update of youtube videos
    if tabela_pierwotna[0] == 'youtubeupdate':
        await message.delete()
        num=50
        
        try:
            num=int(tabela_pierwotna[1])
        except ValueError:
            num=50

        await youtube.youtubeUpdate(client,num)
    
    # Freeze your bot. This command not is not closing bot!
    if tabela_pierwotna[0] == 'exitbotme':
        while TRUE:
            time.sleep(60)
    
    # Repeat after me command 
    if tabela_pierwotna[0] == 'say':
        findChannel = discord.utils.get(client.get_all_channels(), name=tabela_pierwotna[1])
        await findChannel.send(tabela_pierwotna[2].replace('_', ' '))
    
    if tabela[0] == 'autoduo':
        await autoduo.auto.try_solve(client)


    # GAMEJAM MODULE
    if tabela_pierwotna[0] == '&add':
        await gamejam.add_topic(channel,tabela_pierwotna[1].replace('_', ' '))
    if tabela_pierwotna[0] == '&remove':
        await gamejam.remove_topic(channel,(int(tabela_pierwotna[1])-1))
    if tabela_pierwotna[0] == '&show':
        await gamejam.show_topics(channel)
    if tabela_pierwotna[0] == '&random':
        await gamejam.random_topic(channel)
    
    # If no command was found, then return ''
    return ''
