#  ***IPv4 TCP/UDP Port Scanner*** 🕵️💉
[![Version](https://img.shields.io/badge/GeorgiosPortScannerv1.0.0-brightgreen.svg?maxAge=259200)]()
[![Stage](https://img.shields.io/badge/Release-Stable-brightgreen.svg)]()
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)]()
[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
# ***Author*** : Georgios Zervakis

# ***Description***: 

This repository hosts a basic IPv4 port scanner written in Python 3.9. It was created as part of an exercise and general programming practise. You can use it to either improve your Python/programming skills or to configure it in a target machine where other 3rd party scanning tools are not available e.g. nmap.

## ✔️ ***Features***:

- __Infromation Modules__ :

- [x] IPv4 Port Scanner for both TCP/UDP network protocols

## ✔️ ***Installation Linux/Windows*** :
$ git clone git@github.com:ZervakisGeorgios/UntilmatePortScanner.git

Usage
-----

::

    Usage:
        python georgios_scanner.py [<arguments>] [options]

    Arguments:
        <IP>                A single IPv4 address
        <file-path>         The path to the file containing multiple IPv4 addresses. The form of the addresses should be either one 
                            IPv4 address in each line of the file OR a subnet in the first line of the file. The subnet will be analysed to get 
                            the IP addresses from within it. The script cannot analyse subnets where the host bits are set.
    Options:
        -t                  Scan TCP ports
        -u                  Scan UDP ports
        -b                  Perform a basic scan. This involved scanning ports 1-1024.
 
Example
-------

::

    $ python3 georgios_scanner.py 192.168.0.23 -t -b
    -- banner omitted --
    Target ip: 192.168.0.23
    Scanning TCP ports
    Port 80 is open!
    Port 135 is open!
    Port 139 is open!
    Port 445 is open!
    Scanning Completed in:  0:00:02.231671
  
Contents of output.txt

::
    {
    "findings": [
        
        {
            "ip_address": "192.168.0.23",
            "open_port": "80",
            "risk_port": true
        },
        
        {
            "ip_address": "192.168.0.23",
            "open_port": "135",
            "risk_port": true
        },
        
        {
            "ip_address": "192.168.0.23",
            "open_port": "139",
            "risk_port": true
        },
        {
            "ip_address": "192.168.0.23",
            "open_port": "445",
            "risk_port": true
        }
    ]
    }
    

## ✔️ ***About*** :

$ Twitter : https://twitter.com/@Georgios_zm

$ Linkedin: https://www.linkedin.com/in/georgios-zervakis/

$ Tested On : Windows / Ubuntu / Kali Linux /
