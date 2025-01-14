import logging
from datetime import datetime, timedelta
from pathlib import Path
import io
import discord
import youtube
import iniload
import anime
import reddit
import gamedevnews

VALID_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp'}
CONFIG_FILE = 'dane.conf'
LOG_FILE = "../files_conf/log.txt"
DAILY_FILE = "../files_conf/daily.txt"
SILENT_MODE_DURATION = 5 * 60  # 5 minutes

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

connection_active = 0
send_this_when_free = ''
silent_mode = False
message_image_log = []

def clean_log():
    """Clean the message image log by removing entries older than one hour."""
    one_hour_ago = datetime.now() - timedelta(hours=1)
    global message_image_log
    message_image_log = [entry for entry in message_image_log if entry[0] >= one_hour_ago]

def silence_state(is_silient: bool):
    """Disable silent mode after a specified duration."""
    global silent_mode
    silent_mode = is_silient
    
def get_silence_state():
    global silent_mode
    return silent_mode


def log_message(message: discord.Message):
    """Log the message to a file."""
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    with open(LOG_FILE, "a+", encoding="utf-8") as log_file:
        log_file.write(f"{dt_string} // {message.author.name} : \"{message.content}\"\n")

def word_in_message(message, fixing=False):
    """Processes a given message to clean and split it into individual words or tokens."""
    if fixing:
        message = message.lower() 
        message = ''.join([char for i, char in enumerate(message) if i == 0 or char != message[i - 1]])
        message = message.replace(",", " , ").replace("#", " # ").replace("?", " ? ").replace("!", " ! ").replace(".", " . ").replace("\"", " \" ").replace("/", " / ").replace("\\", " \\ ")
    return message.split()

def update_user_data(message: discord.Message):
    """Update user data in the configuration file."""
    user_id = str(message.author.id)
    iniload.ini_change(CONFIG_FILE, user_id, 'name', message.author.name)
    iniload.ini_change(CONFIG_FILE, user_id, 'avatar', str(message.author.avatar_url))
    iniload.ini_change(CONFIG_FILE, user_id, 'display_name', message.author.display_name)
    iniload.ini_change(CONFIG_FILE, user_id, 'discriminator', message.author.discriminator)
    iniload.ini_change(CONFIG_FILE, user_id, 'hash', str(hash(message.author)))

async def handle_daily_tasks(client: discord.Client):
    """Handle daily tasks like anime news and YouTube updates."""
    daily_file = Path(DAILY_FILE)
    daily_file.touch(exist_ok=True)
    with io.open(daily_file, mode="r", encoding="utf-8") as file:
        daily = file.read().strip()

    current_date = datetime.now().strftime("%d/%m/%Y")
    if current_date != daily:
        with io.open(daily_file, "w", encoding="utf-8") as file:
            file.write(current_date)
        await anime.animenews(client)
        await youtube.youtube_update(client, 50)
        await reddit.reddit_posts(client)
        await gamedevnews.gamedevnews_update(client)
        logger.info("Daily commands done")

async def send_large_message(channel, message, silent_mode=False):
    """Split the message into chunks of 1500 characters and send it in chunks."""
    if message and not silent_mode:
        chunk_size = 1500
        chunks = [message[i:i + chunk_size] for i in range(0, len(message), chunk_size)]
        for chunk in chunks:
            await channel.send(chunk)
