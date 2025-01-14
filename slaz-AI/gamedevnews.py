import requests
import discord
from bs4 import BeautifulSoup
import io
import time
import logging
import iniload
import airesponses

logging.basicConfig(level=logging.INFO)

def load_saved_urls(file_path):
    """Loads the list of already presented URLs from a file."""
    try:
        with io.open(file_path, mode="r", encoding="utf-8") as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        return set()

def save_url(file_path, url):
    """Saves a new URL to the file."""
    with io.open(file_path, mode="a", encoding="utf-8") as file:
        file.write(url + "\n")

def get_post_content(url):
    """Gets the content of a post from the given URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the div with the class 'entry-content clear'
    content_div = soup.find('div', class_='entry-content clear')
    if content_div:
        return content_div.get_text(strip=True)
    return None


async def gamedevnews_update(client):
    """Gets new posts from gamefromscratch.com and processes them."""

    redditChannelName = iniload.ini_load('dane.conf', 'GameDevModule', 'Channel', 'User not found')
    channel = discord.utils.get(client.get_all_channels(), name=redditChannelName)

    saved_urls_file = '../files_conf/gamedevnews_saved.txt'
    saved_urls = load_saved_urls(saved_urls_file)
    
    url = "https://gamefromscratch.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all divs with the class 'post-thumb-img-content post-thumb'
    post_thumb_divs = soup.find_all('div', class_='post-thumb-img-content post-thumb')
    for div in post_thumb_divs:
        # Find the <a> tag within the div
        a_tag = div.find('a')
        if a_tag and 'href' in a_tag.attrs:
            post_url = a_tag['href']
            
            if post_url not in saved_urls:
                logging.info(f"New post found: {post_url}")
                
                # Find the <img> tag within the <a> tag
                img_tag = a_tag.find('img')
                lazy_image = None
                if img_tag and 'data-lazy-src' in img_tag.attrs:
                    lazy_image = img_tag['data-lazy-src']
                
                content = get_post_content(post_url)
                if content:
                    if len(content) > 100:
                        gamedev_prompt = airesponses.load_prompt("gamedev_prompt").format(content=content)
                        summary = airesponses.get_ai_response_generic("google/gemini-flash-1.5", 400, gamedev_prompt, None, False )
                        if summary:
                            gamedev_title_prompt = airesponses.load_prompt("gamedev_title_prompt").format(summary=summary)
                            gamedev_article_title = airesponses.get_ai_response_generic("google/gemini-flash-1.5", 20, gamedev_title_prompt, None, False )
                            if gamedev_article_title:
                                # Try to download and send the image as an attachment
                                message_content = f"## {gamedev_article_title} \n {summary} \n Dane zawzięte ze strony: [Link]({post_url}) <:AI:1314942990472712222>"
                                if lazy_image:
                                    try:
                                        image_response = requests.get(lazy_image)
                                        if image_response.status_code == 200:
                                            image_file = discord.File(io.BytesIO(image_response.content), filename="image.png")
                                            await channel.send(message_content, file=image_file)
                                        else:
                                            raise Exception("Failed to download image")
                                    except Exception as e:
                                        logging.warning(f"Failed to download or send image: {e}")
                                        await channel.send(message_content)
                                else:
                                    await channel.send(message_content)
                                time.sleep(0.5)

                    logging.info(f"Content: {content[:200]}...")  # Log first 200 chars of content
                    save_url(saved_urls_file, post_url)
                else:
                    logging.warning(f"Failed to get content from {post_url}")
                
                time.sleep(0.5)  # Sleep t