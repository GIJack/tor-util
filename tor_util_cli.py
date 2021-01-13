#!/usr/bin/env python
prog_meta = {
    'name' : "tor_util",
    'version' : "0.0.0"
}
tor_util_desc='''
Utility for controling TOR via the API. Command line version.

Does Two Things:
1. Send commands to the API over the network
2. Generates hashed passwords for use in the torrc file

TOR API Commands:
	new_ip		Sends the NEWNYM command which gets a new IP. This
generates new tunnels, and with it, a new exit node that has a new IP.

Local Utilities(Commands):
	gen_passwd_hash		Generates a password hash for use in torrc.

	gen_config		Generates blank settings file
'''
tor_util_desc = tor_util_desc.strip()

from tor_util_lib import *

import argparse

def main():
    parser = argparse.ArgumentParser(description=tor_util_desc,add_help=False,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs=1, help="See above for description of commands")
    parser.add_argument("-?", "--help"           , help="Show This Help Message", action="help")

    parser.add_argument("-t","--password-prompt" , help="Prompt for password. overrides settings",action="store_true")
    parser.add_argument("-w","--password"        , help="Password. overrides settings",type=str,nargs=1)
    parser.add_argument("-V","--version"         , help="Print Version and Exit")
    
    parser_network = parser.add_argument_group("Network","Network Settings for send commands")
    parser_network.add_argument("-h","--host"    , help="Address/hostname of TOR daemon")
    parser_network.add_argument("-p","--port"    , help="Port of TOR daemon")
    parser_network.add_argument
    args = parser.parse_args()
    print(args) #DEBUG
    #TODO: write program


if __name__ == "__main__":
    main()
