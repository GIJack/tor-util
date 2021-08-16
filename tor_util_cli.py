#!/usr/bin/env python
# Exit codes 0: success, 1: program failure, 2: user failure, 4: help/info
tor_util_desc='''
Utility for controling TOR via the API. Command line version.

Does Two Things:
1. Send commands to the API over the network
2. Generates hashed passwords for use in the torrc file

API  Host,  Port,  and Password as specified as a JSON file in 
~/.config/tor_util/config, or can be overridden with switches

TOR API Commands:
	new_ip		Sends the NEWNYM command which gets a new IP. This
generates new tunnels, and with it, a new exit node that has a new IP.

	flush_dns		Flushes DNS cache on TOR daemon.

	dormant_mode \__	Turns Dormant Mode on/off. Newish feature to TOR
	active_mode  /
    
    daemon_status		Checks operational status of the TOR Daemon.

Local Utilities(Commands):
	gen_passwd_hash		Generates a password hash for use in torrc.
    
	touch_config		Quit after generating config. useful for first
run
'''
tor_util_desc = tor_util_desc.strip()

from tor_util import common as lib

import argparse
import sys
from getpass import getpass

class colors:
    '''pretty terminal colors'''
    reset='\033[0m'
    bold='\033[01m'
    red='\033[31m'
    cyan='\033[36m'
    yellow='\033[93m'

def message(message):
    print("tor_util_cli: " + message)

def softerr(message):
    '''combination of submsg and error'''
    print(colors.red + colors.bold + "¡ERROR!: " + colors.reset + message, file=sys.stderr)
    return

def exit_with_error(exit,message):
    print("tor_util_cli:" + colors.red + colors.bold + " ¡ERROR!: " + colors.reset + message, file=sys.stderr)
    sys.exit(exit)

def warn(message):
    print("tor_util_cli:" + colors.yellow + colors.bold + "¡WARN!: " + colors.reset + message, file=sys.stderr)
    return
    
def print_password_hash(in_password):
    '''returns a hashed password string for torrc. takes one parameter, plaintext password'''
    in_password = str(in_password)
    hashed_pass = lib.generate_tor_hash(in_password)
    output_message = '''# Paste the following line in your torrc file
# Delete any previous HashedControlPassword lines
'''
    output_message += "HashedControlPassword " + hashed_pass
    print(output_message)
    sys.exit()

def main():
    parser = argparse.ArgumentParser(description=tor_util_desc,epilog="\n\n",add_help=False,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs="?"     , help="See above for description of commands")
    parser.add_argument("-?", "--help"           , help="Show This Help Message", action="help")

    parser.add_argument("-t","--password-prompt" , help="Prompt for password. overrides settings",action="store_true")
    parser.add_argument("-w","--password"        , help="Password. overrides settings",type=str)
    parser.add_argument("-V","--version"         , help="Print Version and Exit", action="store_true")
    
    parser_network = parser.add_argument_group("Network","Network Settings for send commands")
    parser_network.add_argument("-h","--host"    , help="Address/hostname of TOR daemon")
    parser_network.add_argument("-p","--port"    , help="Port of TOR daemon",type=int)
    parser_network.add_argument
    args = parser.parse_args()
    
    # Check version. Don't touch anything, just exit when done
    if args.version == True:
        message("VERSION: " + lib.prog_meta["name"] + "\t" + lib.prog_meta["version"])
        sys.exit(4)
    
    # Load Config
    try:
        config = lib.proc_config_start()
    except:
        warn("Could not load config, using defaults...")
        config = lib.default_config
    # If we are just generating the config, leave it along
    if args.command == "touch_config":
       sys.exit(0)

    ## proc options:
    #Check password
    if args.password_prompt == True:
       config['password'] = getpass()
    elif args.password != None:
       config['password'] = args.password
    #host and port
    if args.host != None:
        config['tor_host'] = args.host
    if args.port != None:
        config['tor_port'] = args.port

    ## Sanity checking
    #check to make sure port is valid:
    if lib.check_port(config['tor_port']) != True:
        exit_with_error(2,"Invalid port: " + str(config['tor_port']))

    # commands
    command = ""
    if args.command == None:
        exit_with_error(2,"No Command Specified, see --help")   
    elif args.command == "new_ip":
        message("Sending New IP Request...")
        command = "SIGNAL NEWNYM"
    elif args.command == "flush_dns":
        message("Clearing DNS Cache...")
        command = "SIGNAL CLEARDNSCACHE"
    elif args.command == "dormant_mode":
        message("Putting TOR Daemon in Dormant Mode...")
        command = "SIGNAL DORMANT"
    elif args.command == "active_mode":
        message("Restoring TOR Daemon to Active Mode...")
        command = "SIGNAL ACTIVE"
    elif args.command == "daemon_status":
        message("Checking Daemon Status...")
    elif args.command == "gen_passwd_hash":
        if args.password_prompt == None and args.password == None:
            hash_pass  = getpass()
        elif args.password_prompt != None:
            hash_pass  = args.password_prompt
        elif args.password != None:
            hash_pass = args.password
        else:
            exit_with_error(2,"Something has gone terribly wrong. unknown password type for hashing. Should never get here. DEBUG!")

        print_password_hash(hash_pass)

    else:
        exit_with_error(2,"Command " + args.command + " is not supported.")

    if args.command == "daemon_status":
        result = lib.tor_daemon_status(config['tor_host'],config['tor_port'],config['password'])
    else:
        result = lib.send_tor_command(command,config['tor_host'],config['tor_port'],config['password'])

    errors_count = 0
    # characters of left column for output, output data
    col = 35
    for line in result:
        error_code = int(line[0])
        line = line[-1]
        if error_code != 250:
            errors_count += 1
            softerr(line + "\n")
        else:
            if "=" in line:
                split_line = line.split(" ")
                for line_item in split_line:
                    line_item = line_item.split("=")
                    if len(line_item) == 1:
                        continue
                    lin_len = len(line_item[0])
                    print( line_item[0] + ":\t".expandtabs(col - lin_len) + line_item[1])
            else:
                print(line)

    if errors_count == 0:
        sys.exit(0)
    else:
        sys.exit(1)
    
if __name__ == "__main__":
    main()
