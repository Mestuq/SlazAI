# Ślazatek AI
## Discord Bot was created using discord.py (https://github.com/Rapptz/discord.py)

Ślazatek is a fictional character from Flying Islands universum. 
We came up with the idea to bring his humor to our discord server as well. You can meet him on our server "Mroczne Zakątki", or host him for yours servers. 
<br />

## Features:
### **AI features:**

Automatically finds user questions and answers them. Images and attachments are supported. It tracks 3-hour history of context for all users. I'm using the OpenRouter API.
The bot has been enhanced to handle more complex queries by extracting content from web pages and YouTube videos. When a user sends a message containing a URL, the bot will:
- **For YouTube URLs:** Fetch the video transcript and append it to the message context, allowing the AI to provide more informed responses based on the video content.
- **For Other URLs:** Scrape the text content from the webpage and append it to the message context, enabling the AI to respond with information derived from the linked content.
Moreover, it summarizes YouTube videos using transcriptions and generates summaries for anime announcements (see below).

### **Predefined answers:**

Ślazatek checks every single word of your message, not just those with a specific prefix. It collects words and matches the answers based on predefined answers with the necessary words.

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
### **Reddit integration:**
Automatically sends a message to a designated channel when a new post is made in a specified subreddit.

(For educational and private purpose only)
<br /><br /><br />

### **GameDev News Integration:**
The bot now includes a GameDev news feature that fetches the latest posts from https://gamefromscratch.com/. Credits and links to the original post and author are included. Additionally, the posts are translated into Polish to make the content accessible to a wider audience.


### THIS BOT ONLY HANDLE ONE SERVER AT ONCE FOR ONE CLIENT!
If you want to use this bot for multiple servers you need to make multiple discord api's in 
https://discord.com/developers/

## Required python packages to run this bot:
```bash
pip install discord.py
pip install netifaces
pip install urllib3
pip install configparser
pip install selenium
pip install beautifulsoup4
pip install requests
pip install youtube-transcript-api
```

## Installation:
### For Docker users:
Run container in interactive mode or change config file files_conf/dane.conf to configure your bot.
Warning! Dockerfile was not carefully checked against errors.
```bash
docker run -it slaz-AI
```
### Installation without docker
You have to have Firefox installed!<br />
Unzip master file. <br />
Install Geckodriver from here: https://github.com/mozilla/geckodriver/releases<br />
Create new firefox profile. To do this, run "firefox -p", and create new profile with directory "files_conf/profile".<br />
In the browser, log into your youtube channel. This bot will follow all the channels you are subscribing.<br />
If you want, to run this bot in autostart move file "extra/slazai.desktop" to "/computer_name/.config/autostart".<br />
Run "python slaz-AI/index.py" <br />
Answer several questions in command line.<br />

## List of commands:
**Normal commands:**

"stwórz mi kanał [name_of_chanel_without_space]" - create a message channel in current category.

"zamknij [word] [number of minutes]" - Make bot silent for given number of minutes.

"dobra mów" albo "&end_silient" - koniec wyciszenia bota

"pokaż ranking przekleństw" - Show swear ranking (who swears the most)

"Widzisz mnie?" - Check if bot works (in early state, for debug purposes)

"animeupdate" - Check for new anime (doing automatically every day)

"youtubeupdate [number]" - Check for new youtube videos (doing automatically every day). Optional argument is to stipulate how old videos will be considered.

"redditupdate" - Check for new Reddit posts (doing automatically every day)

"exitbotme" - Quit the discord server.

"say [name_of_channel] [content]" - bot will send a message (content) into given channel name. Replace spaces with '_' in content argument. 

"&add [topic]" - Add new GameJam topic

"&remove [ID]" - Remove GameJam topic with ID

"&show" - Show all GameJam topics

"&random" - Random one GameJam topic.

"zapomnij historie" - Clears the entire AI history context instantly.

"gamedevupdate" - Triggers a GameDev news update.

"youtubeshow" - Displays the list of subscribed YouTube channels in packets of 10.

"youtuberanking" - Displays the ranking of top subscribed YouTube channels based on subscriber count.

"youtubesubscribe" - Subscribes to YouTube channels based on URLs provided in the message.

"youtubeunsubscribe" - Unsubscribes from YouTube channels based on URLs provided in the message.

"dailyupdate" - Triggers the daily updates for anime, YouTube, Reddit, and GameDev news.

**Commands for superusers:**

"AnimeSetChannel" - sets the channel on which anime news will appear

"YoutubeSetChannel" - sets the channel on which youtube news will appear

"RedditSetChannel" - sets the channel on which Reddit news will appear

"GameDevSetChannel" - sets the channel on which GameDev updates will appear

"localip [direction]" - give of server local ip.

"&debug-p [command]" - debug of given message

"&debug [command]" - debug of sent message

"version" - check version of bot

**Work in progress (currently not works):**

"aktualizuj" - automatic download updates from github. (This option stopped working some time ago and I need to fix it)

"vlc [url]" - music on voice channel