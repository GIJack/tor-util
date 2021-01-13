#!/usr/bin/env python
'''
This is a utility for controling TOR via the API

Common Library
'''
prog_meta = {
    'name' : "tor_util",
    'version' : "0.0.1"
}
import os
import json
import socket
import stem
import stem.connection
#from stem.control import Controller

conf_file      = os.getenv("HOME") + "/.config/tor_util/config"
default_config = {
    'tor_host' : "127.0.0.1",
    'tor_port' : 9051,
    'password' : ""
}

send_commands = [ "New IP", "Flush DNS" ] # [ "Dormant Mode", "Active Mode" ] #don't work for some reason

def read_config(file_name):
    '''Loads JSON config returns dict{} with keys'''
    
    file_obj = open(file_name,"r")
    contents = file_obj.read()
    file_obj.close()
    
    contents = json.loads(contents)
    return contents

def write_config(file_name,config_obj):
    '''write config to JSON file'''
    
    contents  = json.dumps(config_obj,indent=4)
    contents += "\n"
    
    file_obj = open(file_name, "w")
    file_obj.write(contents)
    file_obj.close()

def proc_config_start():
    '''checks for config, writes defaults if not present, returns dict with keys''' 
    conf_dir = os.path.dirname(conf_file)
    
    # check if config directory exists. If not make it, and then return defaults:
    if os.path.isdir(conf_dir)    == False and os.path.exists(conf_dir) == True:
        raise "BadConfDir"
    elif os.path.exists(conf_dir) == False:
        os.mkdir(conf_dir)
        write_config(conf_file,default_config)
        return default_config
        
    # check if config file exists, if not make it then return defaults:
    if os.path.isfile(conf_file)   == False and os.path.exists(conf_file) == True:
        raise "BadConfFile"
    elif os.path.exists(conf_file) == False:
        write_config(conf_file,default_config)
        return default_config
        
    # load config
    loaded_config = read_config(conf_file)
    # check to make sure all items are present. If not, load them
    for item in default_config.keys():
        if item not in loaded_config.keys():
            loaded_config[item] = default_config[item]

    return loaded_config

def send_tor_new_ip(command,host,port,password=""):
    '''Send a NEWNYM command for a new IP address over TOR. Needs host, port, and optionally password. returns tupple with error code and message'''
    '''error code: 0 is success, everything else is fail. Message is for updating status'''
    # build the command.
    auth_string = "AUTHENTICATE " + '\"' + password + '\"' + "\n"
    output = ""

    # Set up the control object
    control_obj = stem.socket.ControlPort(address=host, port=port, connect=False)
    try:
        control_obj.connect()
    except stem.SocketError:
        output = "1 Could Not Connect to " + host + " on port " + str(port)
        return output
    try:
        stem.connection.authenticate(control_obj,password)
    except stem.connection.IncorrectPassword:
        output = "1 Incorrect Password, host: " + host + "port: " + str(port)
        return output
        
    try:
        control_obj.send(command)
    except:
        output = "1 Could not send command?"
        return output
        
    message_obj    = control_obj.recv()
    #if message_obj.is_ok() == True:
    #    output_code = 0
    #else:
    #    output_code = 2
    output = message_obj.raw_content()
    
    control_obj.close()
    
    return output
