#!/usr/bin/env python
'''
This is a utility for controling TOR via the API

Common Library
'''

import os
import json

conf_file      = os.getenv("HOME") + "/.config/tor_util/config"
default_config = {
    'tor_host' : "127.0.0.1",
    'tor_port' : "9051",
    'password' : ""
}

def read_config(file_name):
    '''Loads JSON config returns dict{} with keys'''
    
    file_obj = open(file_name,"r")
    contents = file_obj.read()
    file_obj.close()
    
    contents = json.loads(contents)
    return contents

def write_config(file_name,config_obj):
    '''write config to JSON file'''
    
    contents = json.dumps(config_obj,indent=4)
    contents += "\n"
    
    file_obj = open(file_name, "w")
    file_obj.write(contents)
    file_obj.close()

def proc_config_start():
    '''checks for config, writes defaults if not present, returns dict with keys''' 
    conf_dir = os.path.dirname(conf_file)
    
    # check if config directory exists. If not make it, and then return defaults:
    if os.path.isdir(conf_dir) == False and os.path.exists(conf_dir) == True:
        raise "BadConfDir"
    elif os.path.exists(conf_dir) == False:
        os.mkdir(conf_dir)
        write_config(conf_file,default_config)
        return default_config
        
    # check if config file exists, if not make it then return defaults:
    if os.path.isfile(conf_file) == False and os.path.exists(conf_file) == True:
        raise "BadConfFile"
    elif os.path.exists(conf_file) == False:
        write_config(conf_file,default_config)
        return default_config
        
    # load config
    loaded_config = read_config(conf_file)
    # check to make sure all items are present. If not, load them
    for item in default_config.keys():
        if item not in loaded_config.keys():
            loaded_config[item] = default_config['item']

    return loaded_config
