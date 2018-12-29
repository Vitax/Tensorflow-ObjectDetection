""" This script is there to have a global getter for the config file 

"""
import os
import json


def get_config_file():
    """ Method to get the config file in the current application structure """
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "config.txt":
                return os.path.relpath(os.path.join(root, file), ".")


def get_config_file_content(config_file_path):
    """ Gets the content of the current Config file """
    config_file = open(config_file_path)
    try:
        content = json.loads(config_file.read())
        return content
    except:
        return None

