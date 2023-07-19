# Ślazatek AI
## Discord Bot was created using discord.py (https://github.com/Rapptz/discord.py)

Ślazatek is a fictional character from Flying Islands universum. 
We came up with the idea to bring his humor to our discord server as well. You can meet him on our server "Mroczne Zakątki", or host him for yours servers. 
<br /><br /><br />

## Features:
### **Clever answers:**

Ślazatek checking every single word of your message, not only that with the prefix. It's collecting words, and matches the answares based of predefinied answers with words that are needed.

### **Security:**

Protection from "raid's". Checking if someone username is similars (not only exact) to others users that were banned from the server before, and if it he bans this user too.

Localy stores a "Log's" from everyone messages on your server.

### **Useful commands:**

Like makeing this bot silence for some time. Check your local ip addres or make new channel avoiding some permissions.

### **Curses words counter:**

Counting every bad word said on the server.
There is a command to show the servers ranking of the most naughty person.

### **Anime announcements:**

Based on information from https://www.animenewsnetwork.com/
(This bot not storageing any copyrighted content, only shows name, date and link for the image from animenewsnetwork and "lern-more" link)

Simply make a channel called "Anime" and you will be reaciving a info about new anime announcements.

(For educational and private purpose only)
### **Youtube integration:**
Selenium grabs youtube.com/feed/subscriptions information, and shows the result on discord channel. </br>
Attention! Firefox and Geckodriver 3.0 is required. </br>
You need to create an youtube account to follow all subscriptions.

(For educational and private purpose only)
<br /><br /><br />

### THIS BOT ONLY HANDLE ONE SERVER AT ONCE FOR ONE CLIENT!
If you want to use this bot for multiple servers you need to make multiple discord api's in 
https://discord.com/developers/

## Required python packages to run this bot:
```
pip install python-discord
pip install netifaces
pip install urllib3
pip install configparser
pip install selenium
```

## Installation:
### For Docker users:
Run container in interactive mode or change config file files_conf/dane.conf to configure your bot.
Warning! Dockerfile was not carefully checked against errors.
docker run -it slaz-AI
### Instalation without docker
You have to have Firefox installed!<br />
Unzip master file. <br />
Install Geckodriver from here: https://github.com/mozilla/geckodriver/releases<br />
Create new firefox profile. To do this, run "firefox -p", and create new profile with directory "files_conf/profile".<br />
In the browser, log into your youtube channel. This bot will follow all the channels you are subscribing.<br />
If you want, to run this bot in autostart move file "extra/slazai.desktop" to "/computer_name/.config/autostart".<br />
Run "python slaz-AI/index.py" <br />
Answear a several questions in command line.<br />

## List of commands:
**Normal commands:**

"stwórz mi kanał [name_of_chanel_without_space]" - create a message channel in current category.

"zamknij [word]" or "&start_silient" - Make bot silient for 15 minutes.

"dobra mów" albo "&end_silient" - koniec wyciszenia bota

"pokaż ranking przekleństw" - Show swear ranking (who swears the most)

"Widzisz mnie?" - Check if bot works (in early state, for debug purposes)

"animeupdate" - Check for new anime (doing automaticly every day)

"youtubeupdate [number]" - Check for new youtube videos (doing automaticly every day). Optional argument is to stipulate how old videos will be considered.

"exitbotme" - Quit the discord server.

"say [name_of_channel] [content]" - bot will send a message (content) into given channel name. Replace spaces with '_' in content argument. 

"&add [topic]" - Add new GameJam topic

"&remove [ID]" - Remove GameJam topic with ID

"&show" - Show all GameJam topics

"&random" - Random one GameJam topic.

**Commands for superusers:**

"AnimeSetChannel" - sets the channel on which anime news will appear

"YoutubeSetChannel" - sets the channel on which youtube news will appear

"localip [direction]" - give of server local ip.

"&debug-p [command]" - debug of given message

"&debug [command]" - debug of sent message

"version" - check version of bot

**Work in progress (curenlty not works):**

"aktualizuj" - automatic download updates from github. (This option stopped working some time ago and I need to fix it)

"vlc [url]" - music on voice channel
