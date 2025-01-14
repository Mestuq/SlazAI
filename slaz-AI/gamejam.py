import random
import json

topics = []

def load_topics():
    """Loads topics from a JSON file into the global 'topics' list."""
    global topics
    try:
        with open('../files_conf/topics.json', 'r') as file:
            topics = json.load(file)
    except FileNotFoundError:
        topics = []

def save_topics():
    """Saves the current 'topics' list to a JSON file."""
    with open('../files_conf/topics.json', 'w') as file:
        json.dump(topics, file)

async def add_topic(channel, topic):
    """Adds a new topic to the 'topics' list and saves it to the JSON file. Also sends the ID of the new topic."""
    load_topics()
    
    if topic in topics:
        await channel.send(f'Temat "{topic}" już istnieje.')
        return
    
    topics.append(topic)
    save_topics()
    
    new_topic_id = len(topics)
    await channel.send(f'Temat "{topic}" został dodany. ID: {new_topic_id}')
async def remove_topic(channel, topic_id):
    """Removes a topic from the 'topics' list based on the provided ID or topic name and saves the updated list to the JSON file."""
    load_topics()
    
    if topic_id.isdigit():
        topic_id_int = int(topic_id)
        if 1 <= topic_id_int < len(topics)+1:
            removed_topic = topics.pop(topic_id_int-1)
            save_topics()
            await channel.send(f'Temat "{removed_topic}" został usunięty.')
        else:
            await channel.send('Niewłaściwe ID.')
    else:
        topic_id_lower = topic_id.lower()
        found_index = -1
        for i, topic in enumerate(topics):
            if topic.lower() == topic_id_lower:
                found_index = i
                break
        
        if found_index != -1:
            removed_topic = topics.pop(found_index)
            save_topics()
            await channel.send(f'Temat "{removed_topic}" został usunięty.')
        else:
            await channel.send(f'Temat "{topic_id}" nie został znaleziony.')

async def show_topics(channel):
    """Displays all the topics in the 'topics' list."""
    load_topics()
    if topics:
        topic_list = '\n'.join([f'{i}. {topic}' for i, topic in enumerate(topics, start=1)])
        await channel.send(f'**Tematy:**\n{topic_list}')
    else:
        await channel.send('Brak tematów.')

async def random_topic(channel):
    """Selects and displays a random topic from the 'topics' list."""
    load_topics()
    if topics:
        random_topic = random.choice(topics)
        await channel.send(f'Wylosowany temat: {random_topic}')
    else:
        await channel.send('Brak dostępnych tematów.')