import logging
import time
import discord

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from youtube_transcript_api import YouTubeTranscriptApi
import iniload
import re
import airesponses

async def youtube_update(client, number_of_check):
    """This function is responsible for checking the latest videos from YouTube subscriptions, 
    extracting their transcripts, summarizing the content if applicable, and then posting 
    the summaries and video links to a specified Discord channel."""

    logging.warning('Launching YouTube')
    video_list = []

    # Configure Chrome options
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument(r"--user-data-dir=/home/pi/.config/chromium")
    options.add_argument(r'--profile-directory=Default')

    # Initialize WebDriver
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
    driver.get("https://www.youtube.com/feed/subscriptions")

    logging.warning('Waiting...')
    time.sleep(15)
    logging.warning('Waiting ended')

    # Extract video IDs from page source
    page_source = driver.page_source
    video_ids = re.findall(r'videoId":"([^"]+)"', page_source)[:number_of_check]

    # Process each video ID
    for video_id in video_ids:
        with open('../files_conf/YoutubeCeche.txt', 'r+', encoding='utf-8') as cache_file:
            if video_id + "\n" not in cache_file:
                cache_file.write(video_id + "\n")

                # Fetch transcript
                transcript_text = ""
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pl'])
                    transcript_text = (" ".join(entry['text'] for entry in transcript))[:100000]
                except Exception as e:
                    logging.error(f"Transcription error: {e}")

                # Summarize transcript if it's long enough
                if len(transcript_text) > 100:
                    youtube_prompt = airesponses.load_prompt("youtube_prompt").format(transcript_text=transcript_text)
                    summary = airesponses.get_ai_response_generic("google/gemini-flash-1.5",500, youtube_prompt, None, False )
                    if summary:
                        video_list.append(summary + "<:AI:1314942990472712222>")

                logging.warning(f'https://www.youtube.com/watch?v={video_id}')
                video_list.append(f'https://www.youtube.com/watch?v={video_id}')

    driver.close()

    # Send messages to Discord channel
    youtube_channel_name = iniload.ini_load('dane.conf', 'YoutubeModule', 'Channel', 'User not found')
    channel = discord.utils.get(client.get_all_channels(), name=youtube_channel_name)

    logging.warning('YouTube finished')
    for video in video_list:
        time.sleep(0.5)
        await channel.send(video)

async def show_subscribed_channels(channel):
    """This function scans the YouTube subscriptions page and displays the channel names and IDs in packets of 10."""
    
    logging.warning('Fetching subscribed channels')
    
    # Configure Chrome options
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument(r"--user-data-dir=/home/pi/.config/chromium")
    options.add_argument(r'--profile-directory=Default')

    # Initialize WebDriver
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
    driver.get("https://www.youtube.com/feed/channels")

    logging.warning('Waiting...')
    time.sleep(15)
    logging.warning('Waiting ended')

    # Extract channel IDs and names from page source
    page_source = driver.page_source
    channel_data = re.findall(r'{"channelId":"([^"]+)","title":{"simpleText":"([^"]+)"}', page_source)

    driver.close()

    # Sort channel_data alphabetically by channel name
    channel_data.sort(key=lambda x: x[1].lower())

    message = "## Subscribed Channels:\n"
    for i, (channel_id, channel_name) in enumerate(channel_data, 1):
        message += f"{i}. {channel_name} - <https://www.youtube.com/channel/{channel_id}>\n"
        if i % 15 == 0:
            await channel.send(message)
            message = ""
            time.sleep(0.5)

    if message.strip():
        await channel.send(message)

async def show_top_subscribed_channels(channel):
    """This function scans the YouTube subscriptions page and displays the top subscribed channels."""
    
    logging.warning('Fetching top subscribed channels')
    
    # Configure Chrome options
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument(r"--user-data-dir=/home/pi/.config/chromium")
    options.add_argument(r'--profile-directory=Default')

    # Initialize WebDriver
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
    driver.get("https://www.youtube.com/feed/channels")

    logging.warning('Waiting...')
    time.sleep(15)
    logging.warning('Waiting ended')

    # Extract channel IDs, names, and subscriber counts from page source
    page_source = driver.page_source
    channel_data = re.findall(r'{"channelId":"([^"]+)","title":{"simpleText":"([^"]+)"}.*?"videoCountText":{"accessibility":{"accessibilityData":{"label":"([^"]+)"}}', page_source)

    driver.close()

    # Convert subscriber counts to integers for sorting
    def parse_subscribers(subscriber_text):
        # Remove non-breaking spaces and other unwanted characters
        subscriber_text = subscriber_text.replace('\xa0', ' ').strip()
        
        # Handle Polish text variations
        subscriber_text = subscriber_text.replace(' subskrybentów', '')
        subscriber_text = subscriber_text.replace(' tysiąca', ' tys.')
        subscriber_text = subscriber_text.replace(' tysiące', ' tys.')
        subscriber_text = subscriber_text.replace(' tysięcy', ' tys.')
        subscriber_text = subscriber_text.replace(' miliona', ' mln')
        subscriber_text = subscriber_text.replace(' milion', ' mln')
        subscriber_text = subscriber_text.replace(' milionów', ' mln')
        subscriber_text = subscriber_text.replace(' tys.', ' tys.')
        subscriber_text = subscriber_text.replace(' subskrybent', '')

        
        if 'mln' in subscriber_text:
            # Handle millions (e.g., "1,12 mln")
            return int(float(subscriber_text.replace(' mln', '').replace(',', '.')) * 1000000)
        elif 'tys.' in subscriber_text:
            # Handle thousands (e.g., "1,1 tys.")
            return int(float(subscriber_text.replace(' tys.', '').replace(',', '.')) * 1000)
        else:
            # Handle plain numbers (e.g., "556 subskrybentów")
            # Remove any remaining non-numeric characters
            subscriber_text = ''.join(filter(str.isdigit, subscriber_text))
            return int(subscriber_text) if subscriber_text else 0

    # Sort channel_data by subscriber count in descending order
    channel_data.sort(key=lambda x: parse_subscribers(x[2]), reverse=True)

    message = "## Top Subscribed Channels:\n"
    for i, (channel_id, channel_name, subscriber_count) in enumerate(channel_data, 1):
        message += f"{i}. {channel_name} - {subscriber_count} - <https://www.youtube.com/channel/{channel_id}>\n"
        if i % 15 == 0:
            await channel.send(message)
            message = ""
            time.sleep(0.5)

    if message.strip():
        await channel.send(message)



async def subscribe_to_channels(message):
    """This function subscribes to YouTube channels by parsing the message for YouTube URLs,
    opening each URL with Selenium, and clicking the 'Subskrybuj' button."""

    logging.warning('Starting subscription process')
    
    try:
        # Extract YouTube URLs from the message
        youtube_urls = re.findall(r'(https?://(?:www\.)?youtube\.com/(?:channel/|user/|c/|@)[^\s,]+)', message.content)
        youtube_urls = [url.rstrip(',') for url in youtube_urls]
        youtube_urls = list(set(youtube_urls))
        
        if not youtube_urls:
            await message.channel.send("No valid YouTube URLs found in the message.")
            return
        
        # Configure Chrome options
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument(r"--user-data-dir=/home/pi/.config/chromium")
        options.add_argument(r'--profile-directory=Default')
        
        # Initialize WebDriver
        driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
        
        for url in youtube_urls:
            try:
                logging.warning(f'Opening URL: {url}')
                driver.get(url)
                
                WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'yt-spec-button-shape-next__button-text-content') and text()='Subskrybuj']"))
                )
                
                subscribe_button = driver.find_element(By.XPATH, "//div[contains(@class, 'yt-spec-button-shape-next__button-text-content') and text()='Subskrybuj']")
                driver.execute_script("arguments[0].scrollIntoView(true);", subscribe_button)
                driver.execute_script("arguments[0].click();", subscribe_button)
                
                logging.warning(f'Subscribed to channel: {url}')
                time.sleep(5) 
                
                await message.channel.send(f"Subscribed to channel: {url}")
            
            except Exception as e:
                logging.error(f"Failed to subscribe to channel {url}: {e}")
                await message.channel.send(f"Failed to subscribe to channel: {url}.")
        
        driver.close()
        logging.warning('Subscription process finished')
    
    except Exception as e:
        logging.error(f"An error occurred during the subscription process: {e}")
        await message.channel.send(f"An error occurred during the subscription process.")

async def unsubscribe_from_channels(message):
    """This function unsubscribes from YouTube channels by parsing the message for YouTube URLs,
    opening each URL with Selenium, and clicking the 'Rezygnuję z subskrypcji' button."""

    logging.warning('Starting unsubscription process')
    
    try:
        youtube_urls = re.findall(r'(https?://(?:www\.)?youtube\.com/(?:channel/|user/|c/|@)[^\s,]+)', message.content)
        youtube_urls = [url.rstrip(',') for url in youtube_urls]
        youtube_urls = list(set(youtube_urls))
        
        if not youtube_urls:
            await message.channel.send("No valid YouTube URLs found in the message.")
            return
        print("YOUTUBE URLS:")
        print(youtube_urls)
        
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument(r"--user-data-dir=/home/pi/.config/chromium")
        options.add_argument(r'--profile-directory=Default')
        
        driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
        
        for url in youtube_urls:
            try:
                logging.warning(f'Opening URL: {url}')
                driver.get(url)
                
                time.sleep(2) 

                WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'yt-spec-button-shape-next__button-text-content') and text()='Subskrybujesz']"))
                )
                subscribed_button = driver.find_element(By.XPATH, "//div[contains(@class, 'yt-spec-button-shape-next__button-text-content') and text()='Subskrybujesz']")
                driver.execute_script("arguments[0].scrollIntoView(true);", subscribed_button)
                driver.execute_script("arguments[0].click();", subscribed_button)
                
                time.sleep(2) 

                WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'yt-core-attributed-string') and contains(text(), 'Rezygnuję z subskrypcji')]"))
                )
                unsubscribe_button_list = driver.find_element(By.XPATH, "//span[contains(@class, 'yt-core-attributed-string') and contains(text(), 'Rezygnuję z subskrypcji')]")
                driver.execute_script("arguments[0].scrollIntoView(true);", unsubscribe_button_list)
                driver.execute_script("arguments[0].click();", unsubscribe_button_list)

                time.sleep(2) 

                WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'yt-spec-button-shape-next') and @aria-label='Rezygnuję z subskrypcji']"))
                )
                unsubscribe_button = driver.find_element(By.XPATH, "//button[contains(@class, 'yt-spec-button-shape-next') and @aria-label='Rezygnuję z subskrypcji']")
                driver.execute_script("arguments[0].scrollIntoView(true);", unsubscribe_button)
                driver.execute_script("arguments[0].click();", unsubscribe_button)

                time.sleep(5) 

                logging.warning(f'Unsubscribed from channel: {url}')
                await message.channel.send(f"Unsubscribed from channel: {url}")
            
            except Exception as e:
                logging.error(f"Error unsubscribing from {url}: {e}")
                await message.channel.send(f"Failed to unsubscribe from channel: {url}.")
        
        driver.close()
        logging.warning('Unsubscription process finished')
    
    except Exception as e:
        logging.error(f"An error occurred during the unsubscription process: {e}")
        await message.channel.send(f"An error occurred during the unsubscription process.")