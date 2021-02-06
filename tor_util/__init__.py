#!/usr/bin/env python
'''
This is a utility for controling TOR via the API

Common Library
'''

import os
import sys
import json
import stem
import stem.connection

class common:
    conf_file = os.getenv("HOME") + "/.config/tor_util/config"
    if "win" in sys.platform:
        conf_file = os.getenv("APPDATA") + "/tor_util/config"
    prog_meta = {
        'name'    : "TOR API Utility",
        'version' : "0.1.0"
    }
    default_config = {
        'tor_host' : "127.0.0.1",
        'tor_port' : 9051,
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
    
        contents  = json.dumps(config_obj,indent=4)
        contents += "\n"
    
        file_obj = open(file_name, "w")
        file_obj.write(contents)
        file_obj.close()

    def proc_config_start():
        '''checks for config, writes defaults if not present, returns dict with keys''' 
        conf_dir = os.path.dirname(common.conf_file)
    
        # check if config directory exists. If not make it, and then return defaults:
        if os.path.isdir(conf_dir)    == False and os.path.exists(conf_dir) == True:
            raise "BadConfDir"
        elif os.path.exists(conf_dir) == False:
            os.mkdir(conf_dir)
            common.write_config(common.conf_file,common.default_config)
            os.chmod(common.conf_file, 0o600)
            return common.default_config
        
        # check if config file exists, if not make it then return defaults:
        if os.path.isfile(common.conf_file)   == False and os.path.exists(common.conf_file) == True:
            raise "BadConfFile"
        elif os.path.exists(common.conf_file) == False:
            common.write_config(common.conf_file,common.default_config)
            os.chmod(common.conf_file, 0o600)
            return common.default_config
        
        # load config
        loaded_config = common.read_config(common.conf_file)
        # check to make sure all items are present. If not, load them
        for item in common.default_config.keys():
            if item not in loaded_config.keys():
                loaded_config[item] = common.default_config[item]

        return loaded_config

    def check_port(port):
        '''Check if port is a valid TCP Port number. Takes one parameter, the port, returns bool(True/False)'''
        # ports are intergers
        if type(port) != int:
            return False
        #between 1 and 65535, or 2^16 - 1
        if 1 <= port <= 65535:
            return True
        else:
            return False
    
    def send_tor_command(command,host,port,password=""):
        '''Send a command tor TOR daremon. Needs command, host, port, and optionally password. returns tupple with error code and message'''
        '''error code: 0 is success, everything else is fail. Message is for updating status'''
        # build the command.
        auth_string = "AUTHENTICATE " + '\"' + password + '\"' + "\n"
        output = ""

        # Set up the control object
        control_obj = stem.socket.ControlPort(address=host, port=port, connect=False)
        try:
            control_obj.connect()
        except stem.SocketError:
            output = [("1", "Could Not Connect!")]
            return output
        try:
            stem.connection.authenticate(control_obj,password)
        except stem.connection.IncorrectPassword:
            output = [("1", "Incorrect Password")]
            return output
        
        try:
            control_obj.send(command)
        except:
            output = [("1","Could not send command?")]
            return output
        
        message_obj = control_obj.recv()
        output      = message_obj.content()
    
        control_obj.close()
    
        return output
        
    def tor_daemon_status(host,port,password=""):
        '''Run several commands to determine status of router. returns list object'''
        # build the command.
        auth_string = "AUTHENTICATE " + '\"' + password + '\"' + "\n"
        output = ""

        # Set up the control object
        control_obj = stem.socket.ControlPort(address=host, port=port, connect=False)
        try:
            control_obj.connect()
        except stem.SocketError:
            output = [("1", "Could Not Connect!")]
            return output
        try:
            stem.connection.authenticate(control_obj,password)
        except stem.connection.IncorrectPassword:
            output = [("1", "Incorrect Password")]
            return output
        
        command_list = { "Version":"GETINFO version", "Circut Status:":"GETINFO status/circuit-established", "Directory Status:":"GETINFO status/enough-dir-info", "Descriptor Status:":"GETINFO status/good-server-descriptor", "Bootstrap:":"GETINFO status/bootstrap-phase" }

        # Commands
        output = []
        for item in command_list:
            command = command_list[item]
        
            try:
                control_obj.send(command)
            except:
                output.append( ("1","Could not send " + command + " command") )
                continue
            
            message_obj = control_obj.recv()
            raw_output = message_obj.content()
            if raw_output[-1][0] == "250" and raw_output[-1][-1] == "OK":
                del(raw_output[-1])
            for line in raw_output:
                output.append(line)
    
        control_obj.close()
        return output
