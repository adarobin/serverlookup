# serverlookup

Parse a CSV containing hostname, serial, ip, netmask, and gateway and output JSON
or a message to STDERR.

```console
adam@wintendo:~/serverlookup$ ./serverlookup.py -h
usage: serverlookup.py [-h] [-f FILE] serial

positional arguments:
  serial                serial number to look up

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  path to csv file (set to ./newservers.csv if unspecified)

adam@wintendo:~/serverlookup$ ./serverlookup.py -f /home/adam/test.csv asdf3
{"hostname": "vcenter", "serial": "asdf3", "ip": "10.255.2.9", "netmask": "255.255.255.0", "gateway": "10.255.2.1"}

adam@wintendo:~/serverlookup$ ./serverlookup.py -f /home/adam/test.csv asdf2 | jq
{
  "hostname": "brawndo",
  "serial": "asdf2",
  "ip": "10.255.2.10",
  "netmask": "255.255.255.0",
  "gateway": "10.255.2.1"
}

adam@wintendo:~/serverlookup$ ./serverlookup.py -f /home/adam/test.csv asdf0 | jq
Netmask for oops2 is invalid: 255.266.255.0

adam@wintendo:~/serverlookup$ ./serverlookup.py -f /home/adam/test.csv asdf1 | jq
IP 10.255.0.10 and Gateway 10.255.2.1 with Netmask 255.255.255.0 for oops are not in the same network
```