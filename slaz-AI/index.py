import os
import sys
import logging
from threading import Timer
from pathlib import Path
import time
import requests
import atexit
import discord
import response
import advancedcommands
import iniload
import airesponses
import message_handlers

VALID_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp'}
CONFIG_FILE = 'dane.conf'
LOG_FILE = "../files_conf/log.txt"
DAILY_FILE = "../files_conf/daily.txt"
SILENT_MODE_DURATION = 5 * 60  # 5 minutes

client = discord.Client()
guild = discord.Guild

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

connection_active = 0
send_this_when_free = ''
silent_mode = False
message_image_log = []

def check_internet_connection(retries: int = 3, delay: int = 3) -> bool:
    """Check if the bot has an active internet connection."""
    global connection_active
    while connection_active < retries:
        try:
            requests.head("http://www.google.com/", timeout=3)
            connection_active += 1
        except requests.ConnectionError:
            logger.warning('Connection Error')
            connection_active = 0
        time.sleep(delay)
    return connection_active >= retries

@atexit.register
def goodbye():
    """Restart the bot on exit."""
    logger.warning('Connection error! Restarting...')
    os.execv(sys.executable, ['python3'] + [sys.argv[0]])

@client.event
async def on_message(message: discord.Message):
    """Handle incoming messages."""
    if isinstance(message.channel, discord.channel.DMChannel):
        await message.author.send("Ze względów bezpieczeństwa, ze ślazatkiem można się kontaktować tylko na serwerze Mroczne Zakątki.")
        return

    airesponses.log_message(message)
    message_handlers.log_message(message)
    message_handlers.update_user_data(message)

    global silent_mode
    global send_this_when_free

    if message.author.bot:
        return

    if send_this_when_free != '':
        await message.channel.send(send_this_when_free)
        send_this_when_free = ''

    command_words = message_handlers.word_in_message(message.content, False)
    original_words = message_handlers.word_in_message(message.content, True)

    resp = response.response_list(command_words, original_words, message.channel, guild, message, client)
    resp2 = await advancedcommands.handle_response(command_words, original_words, message.channel, guild, message, client)

    if resp2 != '':
        resp = resp2
    if resp2 == '&start_silient':
        resp = ''
        await message.channel.send('Dobra, będę cicho')
        silent_mode = True
        Timer(SILENT_MODE_DURATION, message_handlers.after_silence).start()
    if resp2 == '&end_silient':
        resp = ''
        message_handlers.after_silence()
        await message.channel.send('Ok')

    user_words = message_handlers.word_in_message(message.author.name, False)
    if response.blacklist_usernames(user_words) == 'ban':
        resp = f'Pan ślazatek bezpieczenstwa pilnuje, {message.author.name} bana na serwera otrzymuje :)'
        await message.author.ban(reason="System ślazatkowych zabezpieczeń wykrył zakazany nick")

    if resp != '' and not silent_mode:
        await message.channel.send(resp)

    await message_handlers.handle_daily_tasks(client)

def main():
    """Main function to start the bot."""

    if not check_internet_connection():
        logger.error("Failed to establish internet connection. Exiting...")
        sys.exit(1)

    os.chdir(os.path.dirname(sys.argv[0]))
    logger.info('Bot starting now!')

    got_id = iniload.ini_load(CONFIG_FILE, 'Client', 'id', '0')
    if got_id == '0':
        got_id = input('Enter discord bot token: ')
        iniload.ini_change(CONFIG_FILE, 'Client', 'id', got_id)
        special_user = input('Enter your discord username: ')
        iniload.ini_change(CONFIG_FILE, 'Client', 'admin', special_user)
        logger.info('Thanks, bot will start in a second')

    client.run(got_id)

if __name__ == "__main__":
    main()