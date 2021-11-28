#  ***IPv4 TCP/UDP Port Scanner*** 🕵️💉
[![Version](https://img.shields.io/badge/GeorgiosPortScannerv1.0.0-brightgreen.svg?maxAge=259200)]()
[![Stage](https://img.shields.io/badge/Release-Stable-brightgreen.svg)]()
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)]()
[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
# ***Author*** : Georgios Zervakis

# ***Description***: 

This repository hosts a basic IPv4 port scanner written in Python 3.9. It was created as part of an exercise and general programming practise. You can use it to either improve your Python/programming skills or to configure it in a target machine where other 3rd party scanning tools are not available e.g. nmap.

## ✔️ ***Features***:

- __Information Modules__ :

- [x] IPv4 Port Scanner for both TCP/UDP network protocols

## ✔️ ***Installation Linux/Windows*** :
$ git clone git@github.com:ZervakisGeorgios/UntilmatePortScanner.git

Usage
-----

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
        
    
    *  The file to be loaded into the script should be a txt file with the extension .txt
    ** An output.txt file will be generated at the end of the execution to store all open ports for all target IPv4
       addresses. It will flag with a bool variable ports that should be investigated. The list of risk ports is different for 
       TCP/UDP protocols. A thorough research took place to define these lists.
 
Example 1 - Single IPv4 address
-------


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
    
Example 2 - Scanning Multiple IP addresses
-------
    $ python port_stanner_v1.py ip_addresses.txt -t -b
    -- banner omitted --
    *** File ip_addresses.txt was loaded successfully ***
    Validating IP addresses
    All IP addresses were scanned and validated
    Scanning TCP ports
    Port 53 is open!
    Port 80 is open!
    Scanning Completed for 192.168.0.1 :  0:00:03.768897
    Scanning TCP ports
    Port 80 is open!
    Port 135 is open!
    Port 139 is open!
    Port 445 is open!
    Scanning Completed for 192.168.0.23 :  0:00:02.233892
    
Contents of output.txt

    {
    "findings": [
        {
            "ip_address": "192.168.0.1",
            "open_port": "53",
            "risk_port": true
        },
        {
            "ip_address": "192.168.0.1",
            "open_port": "80",
            "risk_port": true
        },
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
    
Contents of ip_addresses.txt

    192.168.0.1
    192.168.0.23
    

## ✔️ ***About*** :

$ Twitter : https://twitter.com/@Georgios_zm

$ LinkedIn: https://www.linkedin.com/in/georgios-zervakis/

$ Tested On : Windows / Ubuntu / Kali Linux /


## ✔️ ***Appendix*** :
References for the research that took place to define TCP/UDP risk ports
https://www.dummies.com/programming/networking/commonly-hacked-ports/
https://nmap.org/book/port-scanning.html
https://specopssoft.com/blog/open-ports-and-their-vulnerabilities/

Why we used socket.connect_ex instead of socket.connect
https://stackoverflow.com/questions/48318266/python-socket-connect-vs-connect-ex

Caveats on the UDP scanning
https://null-byte.wonderhowto.com/how-to/sploit-make-python-port-scanner-0161074/

Source that was used to build the write_to_json function
https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file

Future works: Add functionality to scan IPv6 addresses. Add functionality to scan common risk high ports
