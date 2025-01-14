import os
import logging
from datetime import datetime, timedelta
import requests
import base64
import iniload
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import yaml

VALID_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp'}
message_image_log = []

def load_prompt(name_of_prompt):
    with open('../files_conf/prompts.yaml', 'r', encoding='utf-8') as file:
        prompts = yaml.safe_load(file)
    return prompts['prompts'].get(name_of_prompt, None)

def clean_log():
    """Cleans the message_image_log by removing entries older than one hour."""
    one_hour_ago = datetime.now() - timedelta(hours=3)
    global message_image_log
    message_image_log = [entry for entry in message_image_log if entry[0] >= one_hour_ago]

def log_message(message):
    """Logs a message along with its attachments (if any) to the message_image_log.
    If the message contains a YouTube URL, it fetches the transcript and appends it.
    For other URLs, it fetches the text content and appends it.
    Ignores URLs from bot messages."""
    global message_image_log
    clean_log()
    attachment_list = []
    
    if message.attachments:
        for attachment in message.attachments:
            filename, file_extension = os.path.splitext(attachment.filename)
            if file_extension.lower() in VALID_IMAGE_EXTENSIONS:
                attachment_list.append(attachment.proxy_url)
    
    # Extract all URLs from the message content
    if not message.author.bot:
        urls = extract_urls(message.content)
        for url in urls:
            if "youtube.com" in url or "youtu.be" in url:
                video_id = extract_youtube_video_id(url)
                try:
                    # First try to fetch the transcript in Polish
                    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pl'])
                except Exception as e:
                    # If Polish transcript is not available, try English
                    try:
                        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                    except Exception as e:
                        message.content += "\n" + load_prompt("unable_to_transcript").format(url=url)
                        print(f"Error fetching YouTube transcript: {e}")
                        continue
                transcript_text = (" ".join(entry['text'] for entry in transcript))[:100000]
                youtube_prompt = load_prompt("transcript_prompt").format(url=url, transcript_text=transcript_text)
                message.content += "\n" + youtube_prompt
            else:
                try:
                    options = Options()
                    options.add_argument("--no-sandbox")
                    options.add_argument(r"--user-data-dir=/home/pi/.config/chromium")
                    options.add_argument(r'--profile-directory=Default')
                    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
                    driver.get(url)
                    time.sleep(5)
                    page_content = driver.page_source
                    driver.close()

                    soup = BeautifulSoup(page_content, 'html.parser')
                    text_content = (soup.get_text())[:100000]
                    
                    url_prompt = load_prompt("website_content_prompt").format(url=url, text_content=text_content)
                    message.content += "\n" + url_prompt
                except Exception as e:
                    message.content += "\n" + load_prompt("website_unable_to_load").format(url=url, e=e)
                    print(f"Error fetching URL content: {e}")
    
    message_image_log.append((datetime.now(), message.author.name, message.content, attachment_list))


def extract_urls(text):
    """Extracts all URLs from the given text."""
    import re
    url_pattern = re.compile(r'https?://\S+')
    return url_pattern.findall(text)

def extract_youtube_video_id(url):
    """Extracts the YouTube video ID from the given URL."""
    import re
    regex = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(regex, url)
    return match.group(1) if match else None

def clear_message_log():
    """Clears the entire message_image_log."""
    global message_image_log
    message_image_log = []

def url_to_base64(image_url):
    """Converts an image URL to a base64 encoded string."""
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        return base64.b64encode(response.content).decode('utf-8')
    except requests.RequestException as e:
        logging.error(f"Error fetching the image: {e}")
        return None

def check_mime_type(url):
    """Checks the MIME type of the content at the given URL."""
    try:
        response = requests.head(url)
        response.raise_for_status()
        return response.headers.get('Content-Type')
    except requests.RequestException as e:
        logging.error(f"An error occurred: {e}")
        return None

def get_formatted_messages(message_log, include_images=True):
    """Formats the message log into a list of dictionaries, optionally including images."""
    messages = []
    for log_entry in message_log:
        timestamp, author, content, attachments = log_entry
        role = "user" if author != "Ślazatek" else "assistant"
        
        content_list = []
        
        if content:
            content_list.append({"type": "text", "text": f"{author} : {content} "})
        
        if include_images:
            for attachment_url in attachments:
                base64_image = url_to_base64(attachment_url)
                mime_type = check_mime_type(attachment_url)
                content_list.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}
                })
        
        messages.append({"role": role, "content": content_list if content_list else content})
    
    return messages

def get_ai_response_generic(model="google/gemini-flash-1.5", max_tokens=500, user_response=None, system_prompt=None, include_user_messages=False):
    """Sends a request to the AI API and returns the response, optionally including user messages."""
    global message_image_log
    ai_api_key = iniload.ini_load('dane.conf', 'AI', 'api_key', '0')

    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if include_user_messages:
        messages += get_formatted_messages(message_image_log)
    if user_response:
        messages.append({"role": "user", "content": user_response})
    
    print("Sended request to AI:")
    print(messages)

    response_ai = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {ai_api_key}"},
        json={
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens
        }
    )
    
    if response_ai.status_code == 200:
        response_content = response_ai.json()
        if 'choices' in response_content and len(response_content['choices']) > 0:
            ai_answer = response_content['choices'][0]['message']['content']
            for prefix in ["ŚlazGPT :", "ŚlazGPT:", "Ślazatek :", "Ślazatek:"]:
                if ai_answer.startswith(prefix):
                    ai_answer = ai_answer[len(prefix):].strip()
            for i in range(1, 15):
                ai_answer = ai_answer.replace(f"[{i}]", "")
            ai_answer = ai_answer.replace("@Mestuq", "<@352808188338241536>").replace("@mestuq", "<@352808188338241536>")
            ai_answer = ai_answer.replace("@Kasztan", "<@368814924144705549>").replace("@kasztan", "<@368814924144705549>")
            ai_answer = ai_answer.replace("@Aztoja", "<@332452079908028418>").replace("@aztoja", "<@332452079908028418>")
            ai_answer = ai_answer.replace("@Szklanka", "<@391237384899133441>").replace("@szklanka", "<@391237384899133441>")
            ai_answer = ai_answer.replace("<:AI:1314942990472712222>", "")
            return ai_answer
    return None