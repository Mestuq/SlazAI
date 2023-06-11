from io import StringIO
from pickle import TRUE
import discord
import time
import os
import sys
import subprocess
import netifaces

import codecs

from datetime import datetime
import iniLoad
import anime
import youtube

# Gamejam topics
import gamejam

poczekaj=0

# Class/Struct matching username with their swears count
class v2:
    def __init__(self,ids,howmanys):
        self.ids=ids
        self.howmanys=howmanys
    def __repr__(self):
        return repr((self.ids,self.howmanys)) 

async def response_list(tabela,tabela_pierwotna,channel,guild,message,client):
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
        num=10
        
        try:
            num=int(tabela_pierwotna[1])
        except ValueError:
            num=10

        await youtube.youtubeUpdate(client,num)
    
    # Freeze your bot. This command not is not closing bot!
    if tabela_pierwotna[0] == 'exitbotme':
        while TRUE:
            time.sleep(60)
    
    # Repeat after me command 
    if tabela_pierwotna[0] == 'say':
        findChannel = discord.utils.get(client.get_all_channels(), name=tabela_pierwotna[1])
        await findChannel.send(tabela_pierwotna[2].replace('_', ' '))


    # GAMEJAM MODULE
    if tabela_pierwotna[0] == '&add':
        await gamejam.add_topic(channel,tabela_pierwotna[1].replace('_', ' '))
    if tabela_pierwotna[0] == '&remove':
        await gamejam.remove_topic(channel,tabela_pierwotna[1])
    if tabela_pierwotna[0] == '&show':
        await gamejam.show_topics(channel)
    if tabela_pierwotna[0] == '&random':
        await gamejam.random_topic(channel)
    
    # If no command was found, then return ''
    return ''
