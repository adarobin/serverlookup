#!/usr/bin/env python3

import csv

def main():
    with open("./newservers.csv") as csvfile:
        newservers = csv.DictReader(csvfile)
        serverlist = []

        for row in newservers:
            serverlist.append(row)
    
    print(serverlist)

if __name__ == "__main__":
    main()
