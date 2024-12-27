import time
import os
import sys
import subprocess
import netifaces
import codecs
from datetime import datetime
import iniload
import anime
import youtube
import gamejam
import airesponses
import reddit

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

    if is_command_match(command_words, ["<@405439246548205569>"]) or any(word in original_words for word in ["ślazatku", "ślazatek", "ślazatkowi", "ślaz", "ślazowi", "ślazu"]):
        """Generates a sarcastic AI response based on the current date and context."""
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        sarcastic_prompt = f"Jesteś teraz na chat-cie discord na serwerze Mroczne Zakątki i piszesz tam pod pseudonimem Ślazatek. Piszesz teraz razem z innymi użytkownikami na serwerze. Jest dzisiaj {current_date}. Pomagaj użytkownikom w razie potrzeby. Odpowiadaj krótko, najlepiej w dwóch-trzech zdaniach."

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
            for member in members:
                response_text += f"\n{iniload.ini_load('dane.conf', str(member.user_id), 'display_name', 'User not found')} # {member.count}"
            return response_text

    if command_words[0] == 'vlc' and message.author.name == iniload.ini_load('dane.conf', 'Client', 'admin', ''):
        """Launches VLC media player with the specified file."""
        subprocess.call(f'vlc {command_words[1]}', shell=True)
        return 'Trwa uruchamianie...'

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

    if command_words[0] == 'zamknij' and command_words[1] in ['ryj', 'morde']:
        """Stops the bot from responding temporarily."""
        return '&start_silient'

    if command_words[0] == 'dobra' and command_words[1] == 'mów':
        """Resumes the bot's responses."""
        return '&end_silient'

    if command_words[0] == 'localip' and command_words[1] == '-' and message.author.name == iniload.ini_load('dane.conf', 'Client', 'admin', ''):
        """Retrieves the local IP address of the default network interface."""
        iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
        return netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']

    if command_words[0] == 'animeupdate':
        """Triggers an anime news update."""
        await message.delete()
        await anime.animenews(client)
    
    if command_words[0] == 'redditupdate':
        """Triggers an Reddit subreddit update."""
        await message.delete()
        await reddit.reddit_posts(client)

    if command_words[0] == 'youtubeupdate':
        """Triggers a YouTube update with a specified number of videos."""
        await message.delete()
        num = int(command_words[1]) if command_words[1].isdigit() else 50
        await youtube.youtube_update(client, num)

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
        await gamejam.add_topic(channel, command_words[1].replace('_', ' '))
    if command_words[0] == '&remove':
        """Removes a topic from the game jam list by index."""
        await gamejam.remove_topic(channel, int(command_words[1]) - 1)
    if command_words[0] == '&show':
        """Displays all topics in the game jam list."""
        await gamejam.show_topics(channel)
    if command_words[0] == '&random':
        """Selects and displays a random topic from the game jam list."""
        await gamejam.random_topic(channel)

    return ''