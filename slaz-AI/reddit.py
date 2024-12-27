import discord
import iniload
import io
import time
import logging
import requests
from bs4 import BeautifulSoup

async def reddit_posts(client):
    """Fetches new posts from r/Gamedev_Polska and posts them to a specified Discord channel."""
    redditChannelName = iniload.ini_load('dane.conf', 'RedditModule', 'Channel', 'User not found')
    logging.warning(redditChannelName)
    channel = discord.utils.get(client.get_all_channels(), name=redditChannelName)

    url = "https://www.reddit.com/r/Gamedev_Polska/new/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    print(response.content)
    soup = BeautifulSoup(response.content, 'html.parser')

    posts = soup.find_all('shreddit-post')
    for post in posts:
        post_title = post.get('post-title')
        post_url = "https://www.reddit.com" + post.get('permalink')
        author = post.get('author')

        already_presented = False
        with io.open('../files_conf/reddit_saved.txt', mode="r", encoding="utf-8") as searchfile:
            for search in searchfile:
                if search.strip() == post_title:
                    already_presented = True
                    break

        if not already_presented:
            with io.open('../files_conf/reddit_saved.txt', mode="a", encoding="utf-8") as searchfile:
                searchfile.write(post_title + "\n")

            await channel.send(f'{author} : \"{post_title}\" \n{post_url}')
            time.sleep(0.5)
