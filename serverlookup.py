#!/usr/bin/env python3

import csv
import argparse
import json
import sys
import ipaddress

argparser = argparse.ArgumentParser()
argparser.add_argument("serial", help="serial number to look up")
argparser.add_argument("-f","--file", help="path to csv file (set to ./newservers.csv if unspecified)")
args = argparser.parse_args()

def main():
    # Try to open and parse the CSV - error to stderr otherwise
    csvfilename = "./newservers.csv"
    if args.file:
        csvfilename = args.file
    try:    
        with open(csvfilename) as csvfile:
                newservers = csv.DictReader(csvfile)
                serverlist = []
                for row in newservers:
                    serverlist.append(row)
    except FileNotFoundError:
        print(f"File {args.file} not found", file=sys.stderr)
        exit(1)
    finally:
        csvfile.close()
    
    # Try to find the serial number specified - error to stderr otherwise
    try:
        server = next(x for x in serverlist if x["serial"] == args.serial)
    except StopIteration:
        print(f"Serial {args.serial} not found", file=sys.stderr)
        exit(1)

    # Remove extra whitespace around hostname
    server["hostname"] = str.strip(server["hostname"])

    # validate IP address
    try:
        ip = ipaddress.ip_address(server["ip"])
    except ValueError:
        print(f"IP for {server['hostname']} is invalid: {server['ip']}", file=sys.stderr)
        exit(1)

    # validate gateway
    try:
        gateway = ipaddress.ip_address(server["gateway"])
    except ValueError:
        print(f"Gateway for {server['hostname']} is invalid: {server['gateway']}", file=sys.stderr)
        exit(1)
    
    # validate netmask and get network
    try:
        network = ipaddress.ip_network(format(ip)+"/"+server["netmask"], strict=False)
    except ValueError:
        print(f"Netmask for {server['hostname']} is invalid: {server['netmask']}", file=sys.stderr)
        exit(1)

    if gateway not in network:
        print(f"IP {format(ip)} and Gateway {format(gateway)} with Netmask {network.netmask} for {server['hostname']} are not in the same network", file=sys.stderr)
        exit(1)

    print(json.dumps(server))

if __name__ == "__main__":
    main()
