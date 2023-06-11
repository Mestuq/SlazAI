import random
import json

topics = []

def load_topics():
    global topics
    try:
        with open('../files_conf/topics.json', 'r') as file:
            topics = json.load(file)
    except FileNotFoundError:
        topics = []

def save_topics():
    with open('../files_conf/topics.json', 'w') as file:
        json.dump(topics, file)

async def add_topic(channel, topic):
    load_topics()
    topics.append(topic)
    save_topics()
    await channel.send(f'Temat "{topic}" został dodany.')

async def remove_topic(channel, topic_id: int):
    load_topics()
    if 0 <= topic_id < len(topics):
        removed_topic = topics.pop(topic_id)
        save_topics()
        await channel.send(f'Temat "{removed_topic}" został usunięty.')
    else:
        await channel.send('Niewłaściwe ID.')

async def show_topics(channel):
    load_topics()
    if topics:
        topic_list = '\n'.join([f'{i}. {topic}' for i, topic in enumerate(topics)])
        await channel.send(f'**Tematy:**\n{topic_list}')
    else:
        await channel.send('Brak tematów.')

async def random_topic(channel):
    load_topics()
    if topics:
        random_topic = random.choice(topics)
        await channel.send(f'Wylosowany temat: {random_topic}')
    else:
        await channel.send('Brak dostępnych tematów.')

