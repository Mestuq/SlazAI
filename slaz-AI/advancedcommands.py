import time
import os
import sys
import subprocess
import netifaces
import codecs
from datetime import datetime
from threading import Timer
import iniload
import discord
import anime
import youtube
import gamejam
import airesponses
import reddit
import gamedevnews
import messagehandlers

wait_time = 0

def is_command_match(message_words, required_words):
    """Checks if all required words are present in the message words."""
    return all(req in message_words for req in required_words)

class UserSwearCount:
    """Class to store user ID and their swear count."""
    def __init__(self, user_id, count):
        self.user_id = user_id
        self.count = count

    def __repr__(self):
        return repr((self.user_id, self.count))

async def handle_response(command_words, original_words, channel, guild, message, client):
    """Handles various commands and responses based on the input message."""
    global wait_time

    for i in range(1, 10):
        command_words.append('')
        original_words.append('')

    if command_words[0] == 'stwórz' and command_words[1] == 'mi' and command_words[2] == 'kanał':
        """Creates a new text channel if the limit is not exceeded."""
        if wait_time != datetime.now().minute:
            channel_count = len(message.guild.channels)
            if channel_count < 100:
                channel_name = command_words[3]
                new_channel = await message.guild.create_text_channel(channel_name)
                await new_channel.edit(category=message.channel.category, sync_permissions=True)
                await new_channel.send(f'Kanał użytkownika: {message.author.name}')
                wait_time = datetime.now().minute
                return 'Zrobione!'
            else:
                return f'Sorki, ale na tym serwerze jest już {channel_count} kanałów. Poczekaj na admina, aby zwiększyć ten limit.'
        else:
            return 'Poczekaj minutę, nie chcę robić spamu.'

    if command_words[0] == 'aktualizuj':
        """Updates the bot by running an update script and exiting."""
        await channel.send('Poczekaj!')
        time.sleep(2.0)
        os.system('/home/pi/files/run_update.sh')
        sys.exit(0)
        return ''

    if is_command_match(command_words, ["<ślazatku>"]):
        """Generates a non sarcastic AI response based on the current date and context."""
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        non_sarcastic_prompt = airesponses.load_prompt("non_sarcastic_prompt").format(current_date=current_date)

        if len(message.content) > 10:
            return airesponses.get_ai_response_generic("google/gemini-flash-1.5",500,None,non_sarcastic_prompt,True) + "<:AI:1314942990472712222>"

    if is_command_match(command_words, ["<@405439246548205569>"]) or any(word in original_words for word in ["ślazatku", "ślazatek", "ślazatkowi", "ślaz", "ślazowi", "ślazu"]):
        """Generates a sarcastic AI response based on the current date and context."""
        
        # Check if the user is asking for help or doesn't remember a specific command
        command_prompt = airesponses.load_prompt("command_prompt")

        # Get the AI response with the command prompt
        ai_response = airesponses.get_ai_response_generic("google/gemini-flash-1.5", 500, message.content, command_prompt, True)

        # If the AI suggests a command, execute it on behalf of the user
        if ai_response and "none" not in ai_response.lower():
            
            unwanted_chars = "`*\"'"
            ai_response = ai_response.strip(unwanted_chars)

            message.content = ai_response
            await message.channel.send(f"Wykonuję komendę: {ai_response}")
            command_words = messagehandlers.word_in_message(message.content, False)
            original_words = messagehandlers.word_in_message(message.content, True)
            return await handle_response(command_words, original_words, channel, guild, message, client) 
        
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        sarcastic_prompt = airesponses.load_prompt("sarcastic_prompt").format(current_date=current_date)

        if len(message.content) > 10:
            return airesponses.get_ai_response_generic("google/gemini-flash-1.5",500,None,sarcastic_prompt,True) + "<:AI:1314942990472712222>"

    if command_words[0] == 'pokaż' and command_words[1] == 'ranking' and command_words[2] == 'przekleństw':
        """Displays a ranking of users based on their swear count."""
        with codecs.open('../files_conf/licznik.conf', encoding="utf-16") as file:
            response_text = "Ranking przekleństw: \n"
            members = []
            for line in file:
                if '=' in line:
                    user_id, count = line.strip().split('=')
                    members.append(UserSwearCount(int(user_id), int(count)))
            members.sort(key=lambda x: x.count, reverse=True)
            
            for index, member in enumerate(members, start=1):
                display_name = iniload.ini_load('dane.conf', str(member.user_id), 'display_name', 'User not found')
                name = iniload.ini_load('dane.conf', str(member.user_id), 'name', 'User not found')
                count_str = str(member.count)
                
                # Format the line with tabulations for spacing
                response_text += f"{index}.\t{display_name}\t({name})\t#\t{count_str}\n"
            return response_text

    if command_words[0] == 'vlc' and message.author.name == iniload.ini_load('dane.conf', 'Client', 'admin', ''):
        """Launches VLC media player with the specified file."""
        subprocess.call(f'vlc {command_words[1]}', shell=True)
        return 'Trwa uruchamianie...'
    
    if command_words[0] == 'zapomnij' and command_words[1] == 'historie':
        """Clears the entire message_image_log."""
        airesponses.clear_message_log()
        return 'Zapomniałem.'

    if command_words[0] == 'AnimeSetChannel' and message.author.name == iniload.ini_load('dane.conf', 'Client', 'admin', ''):
        """Sets the channel for anime updates."""
        iniload.ini_change("dane.conf", 'AnimeModule', 'Channel', message.channel.name)
        return 'Ok'

    if command_words[0] == 'YoutubeSetChannel' and message.author.name == iniload.ini_load('dane.conf', 'Client', 'admin', ''):
        """Sets the channel for YouTube updates."""
        iniload.ini_change("dane.conf", 'YoutubeModule', 'Channel', message.channel.name)
        return 'Ok'

    if command_words[0] == 'RedditSetChannel' and message.author.name == iniload.ini_load('dane.conf', 'Client', 'admin', ''):
        """Sets the channel for Reddit updates."""
        iniload.ini_change("dane.conf", 'RedditModule', 'Channel', message.channel.name)
        return 'Ok'

    if command_words[0] == 'GameDevSetChannel' and message.author.name == iniload.ini_load('dane.conf', 'Client', 'admin', ''):
        """Sets the channel for GameDev updates."""
        iniload.ini_change("dane.conf", 'GameDevModule', 'Channel', message.channel.name)
        return 'Ok'

    if command_words[0] == 'zamknij' and command_words[1] in ['ryj', 'morde']:
        """Stops the bot from responding temporarily."""
        # Default to 15 minutes if command_words[2] is not a digit
        silent_duration = int(command_words[2]) * 60 if len(command_words) > 2 and command_words[2].isdigit() else 15 * 60
        await channel.send(f'Dobra, będę cicho przez {silent_duration // 60} minut. Aby to odwołać użyj polecenia ``dobra mów``.')
        Timer(silent_duration, messagehandlers.silence_state(True)).start()
        return ''

    if command_words[0] == 'localip' and command_words[1] == '-' and message.author.name == iniload.ini_load('dane.conf', 'Client', 'admin', ''):
        """Retrieves the local IP address of the default network interface."""
        iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
        return netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']

    if command_words[0] == 'animeupdate':
        """Triggers an anime news update."""
        await anime.animenews(client)
        return "Już!"
    
    if command_words[0] == 'redditupdate':
        """Triggers an Reddit subreddit update."""
        await reddit.reddit_posts(client)
        return "Już!"
    
    if command_words[0] == 'gamedevupdate':
        """Triggers an GameDev news update."""
        await gamedevnews.gamedevnews_update(client)
        return "Już!"

    if command_words[0] == 'youtubeupdate':
        """Triggers a YouTube update with a specified number of videos."""
        num = int(command_words[1]) if command_words[1].isdigit() else 50
        await youtube.youtube_update(client, num)
        return "Już!"
    
    # Add this block for showing subscribed YouTube channels
    if command_words[0] == 'youtubeshow':
        """Displays the list of subscribed YouTube channels in packets of 10."""
        await youtube.show_subscribed_channels(message.channel)
    
    if command_words[0] == 'youtuberanking':
        """Displays the ranking of top subscribed YouTube channels based on subscriber count."""
        await youtube.show_top_subscribed_channels(message.channel)

    if command_words[0] == 'youtubesubscribe':
        """Subscribes to YouTube channels based on URLs provided in the message."""
        await youtube.subscribe_to_channels(message)

    if command_words[0] == 'youtubeunsubscribe':
        """Unsubscribes from YouTube channels based on URLs provided in the message."""
        await youtube.unsubscribe_from_channels(message)

    # Add this block inside the handle_response function in advancedcommands.py
    if command_words[0] == 'dailyupdate':
        """Triggers the daily updates for anime, YouTube, Reddit, and GameDev news."""
        await anime.animenews(client)
        await youtube.youtube_update(client, 50)
        await reddit.reddit_posts(client)
        await gamedevnews.gamedevnews_update(client)
        return "Już!"

    if command_words[0] == 'exitbotme':
        """Puts the bot into an infinite sleep loop."""
        while True:
            time.sleep(60)

    if command_words[0] == 'say':
        """Sends a message to a specified channel."""
        target_channel = discord.utils.get(client.get_all_channels(), name=command_words[1])
        await target_channel.send(command_words[2].replace('_', ' '))

    if command_words[0] == '&add':
        """Adds a new topic to the game jam list."""
        topic_name = message.content[len('&add '):].strip()
        await gamejam.add_topic(channel, topic_name)

    if command_words[0] == '&remove':
        """Removes a topic from the game jam list by index."""
        await gamejam.remove_topic(channel, command_words[1])
    if command_words[0] == '&show':
        """Displays all topics in the game jam list."""
        await gamejam.show_topics(channel)
    if command_words[0] == '&random':
        """Selects and displays a random topic from the game jam list."""
        await gamejam.random_topic(channel)

    return ''