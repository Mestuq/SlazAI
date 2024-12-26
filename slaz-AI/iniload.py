import configparser
import codecs

def ini_load(file, group, item, default):
    """
    Loads a specific item from a specified group in an INI file.
    If the group or item does not exist, it returns the default value.
    """
    config = configparser.ConfigParser()
    config.read(f'../files_conf/{file}', encoding="utf-16")
    if not config.has_section(group):
        config.add_section(group)
        return default
    return config.get(group, item) if config.has_option(group, item) else default

def ini_change(file, group, item, value):
    """
    Changes or sets a specific item in a specified group in an INI file.
    If the group does not exist, it creates the group before setting the item.
    """
    config = configparser.ConfigParser()
    with codecs.open(f'../files_conf/{file}', "r", "utf16") as config_file:
        config.read_file(config_file)
    if not config.has_section(group):
        config.add_section(group)
    config.set(group, item, value)
    with open(f'../files_conf/{file}', 'w', encoding="utf-16") as config_file:
        config.write(config_file)