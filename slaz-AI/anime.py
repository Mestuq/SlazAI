import discord
import iniload
import io
import time
import logging
import requests
import airesponses
from bs4 import BeautifulSoup

async def animenews(client):
    """Fetches upcoming anime news from Anime News Network and posts it to a specified Discord channel."""
    animeChannelName = iniload.ini_load('dane.conf', 'AnimeModule', 'Channel', 'User not found')
    logging.warning('animeChannelName')
    channel = discord.utils.get(client.get_all_channels(), name=animeChannelName)

    urls = [
        "https://www.animenewsnetwork.com/encyclopedia/anime/upcoming/tv",
        "https://www.animenewsnetwork.com/encyclopedia/anime/upcoming/movie"
    ]

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                img_tag = row.find('img')
                name_tag = row.find('a', class_='ENCYC')
                date_tag = row.find_all('td')[-1] if row.find_all('td') else None

                if name_tag:

                    image_url = "https://www.animenewsnetwork.com/images/encyc/" + img_tag['src'].split('/')[-1] if img_tag \
                        else "https://cdn.discordapp.com/attachments/801861475395698740/1025787436988645506/unknown.png"
                    
                    name = name_tag.text.strip()
                    date = date_tag.text.strip() if date_tag else "nieznany"

                    already_presented = False
                    with io.open('../files_conf/anime_saved.txt', mode="r", encoding="utf-8") as searchfile:
                        for search in searchfile:
                            if search.strip() == name:
                                already_presented = True
                                break

                    if not already_presented:
                        with io.open('../files_conf/anime_saved.txt', mode="a", encoding="utf-8") as searchfile:
                            searchfile.write(name + "\n")

                        ai_description = ""
                        if len(name) > 10:
                            anime_prompt = f"Wyjaśnij krótko na czym polega historia nadchodzącego anime \"{name}\". Nie wchodź w szczegóły. Pisz w języku polskim."
                            summary = airesponses.get_ai_response_generic("perplexity/llama-3.1-sonar-large-128k-online",500,anime_prompt,None,False)
                            if summary:
                                ai_description = summary + " (AI)"

                        embed = discord.Embed(
                            title=name,
                            description=ai_description,
                            colour=discord.Colour.blue(),
                            url=f"https://www.animenewsnetwork.com{name_tag['href']}"
                        )
                        embed.set_footer(text=f"Premiera planowana jest na: {date}")
                        embed.set_image(url=image_url)

                        await channel.send(embed=embed)
                        time.sleep(0.5)
