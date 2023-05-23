import configparser
import logging
import codecs
import sys

# Load ini content
def iniLoad(_file,_group,_item,_default):

    # Warning about loading data
    logging.warning('File Loading '+'../files_conf/'+_file)

    config = configparser.ConfigParser()
    config.sections()
    # UTF-16 for emoji support
    config.read('../files_conf/'+_file, encoding="utf-16")

    # If ini group not exist, create one
    if config.has_section(_group) == False:
        config.add_section(_group)
        return _default

    # If item not exist create one
    if config.has_option(_group, _item) == True:
        _return=config.get(_group, _item)
    else:
        config.set(_group,_item, _default)
    
    # Return result
    return _return

# Change ini content
def iniChange(_file,_group,_item,_value):

    # Warning about saving data
    logging.warning('File Saving '+'../files_conf/'+_file)

    config = configparser.ConfigParser()
    config.sections()
    # UTF-16 for emoji support
    config.readfp(codecs.open('../files_conf/'+_file, "r", "utf16"))

    # If ini group not exist, create one
    if config.has_section(_group) == False:
        config.add_section(_group)
    config.set(_group,_item, _value)

    # Merge the content to a file
    with open('../files_conf/'+_file, 'w',encoding="utf-16") as configfile:
        config.write(configfile)
