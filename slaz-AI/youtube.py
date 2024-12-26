import logging
import time
import discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
                    transcript_text = " ".join(entry['text'] for entry in transcript)
                except Exception as e:
                    logging.error(f"Transcription error: {e}")

                # Summarize transcript if it's long enough
                if len(transcript_text) > 100:
                    youtube_prompt = f"Poniższy tekst to transkrypcja filmu. Twoim zadaniem jest przygotowanie krótkiego streszczenia treści całego filmu. Oto treść filmu: ``` {transcript_text[:6000]}  ```"
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