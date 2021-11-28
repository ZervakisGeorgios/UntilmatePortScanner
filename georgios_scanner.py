import ipaddress
import sys
import json
import time
from datetime import datetime
import socket
import threading
from queue import Queue
from pprint import pprint

# Queue module implements multi-producer/consumer queues useful in threaded https://docs.python.org/3/library/queue.html
# queue = Queue()
basic_port_list = range(1, 1025)  # The standard ports to be scanned 1-1024
open_ports = {'findings': []}  # Initialises the dictionary that will store open ports
# set variables to store most common risky ports according to https://nmap.org/book/port-scanning.html
# https://www.dummies.com/programming/networking/commonly-hacked-ports/
# https://specopssoft.com/blog/open-ports-and-their-vulnerabilities/
risk_ports_tcp = {21, 22, 23, 25, 53, 80, 81, 110, 111, 135, 137, 138, 139, 143, 145, 443, 445}
risk_ports_udp = {53, 67, 68, 69, 123, 135, 137, 138, 139, 162, 445, 500, 514, 520, 631}


def usage():
    """
    This function prints out the banner of the script as well as examples of the usage and information about The Creator
    """
    print('''

  ________                          .__                       __________   
 /  _____/  ____  ___________  ____ |__| ____  ______         \____    /   
/   \  ____/ __ \/  _ \_  __ \/ ___\|  |/  _ \/  ___/           /     /    
\    \_\  \  ___(  <_> )  | \/ /_/  >  (  <_> )___ \           /     /_    
 \______  /\___  >____/|__|  \___  /|__|\____/____  >         /_______ \   
        \/     \/           /_____/               \/                  \/   

     _____
    (_____)
    | o o /                                      __  __           \\\            //\\\            //
    \_|_/  ___________             _    _     __ _    _            \\\          //  \\\          //
    |____ | _  _  _  |_    _  _     _    _     _   _   _            \\\        //    \\\        //
    |     |__________|         _     _   _     _ _   _               \\\      //      \\\      //
    |          /\\                         __   __ _                   \\\    //        \\\    //
    /\\        /  \\                                                     \\\  //          \\\  //
   /  \\      /    \\                                                     \\\//            \\\//

    USAGE: python georgiosz_scanner.py IP -t -b
    Example: python georgiosz_dos.py 1.1.1.1 -t -b

    The georgiosz_scanner.py programme was created by Georgios Zervakis and it is the ultimate port scanner
    tool for several network protocols
    Linkedin : https://www.linkedin.com/in/georgios-zervakis/
    Tweeter  : @Georgios_zm
    Website  : georgiosnetworks.com
    TryHackMe: DrG
    ''')


def validate_ip_address(address):
    """
    This function will be used to validate that the IP address the user passed is a valid one
    source: https://codefather.tech/blog/validate-ip-address-python/
    :param address: It will be arg[1] passed directly as a CML option
    :return: Returns True if it is a valid IPv4/v6 or False if it is not a valid IPv4/v6
    """
    try:
        ip = ipaddress.ip_address(address)
        return True
    except ValueError:
        return False
        # print("**************************************************************************************************")
        # print("*************************************** Invalid IP address ***************************************")
        # print("**************************************************************************************************")
        # usage()
        # sys.exit()


def subnet_to_ip(subnet_address):
    """
    This function will produce a list of IP addresses should the user passes a subnet as an input. It will flag and exit
    if the subnet is not valid.

    :param subnet_address: The subnet that the user passed via the txt file
    :return: The function will return a list of the IP addresses based on the given subnet
    """
    list_of_ip_addresses = []
    # A for loop will loop all IP addresses from a given subnet
    try:
        for address in ipaddress.ip_network(subnet_address):
            # Each IP address will be converted to a string and appended into the list
            list_of_ip_addresses.append(str(address))

        return list_of_ip_addresses
    except:
        print("**************************************************************************************************")
        print("************************* Invalid subnet or the subnet has host bits set *************************")
        print("**************************************************************************************************")
        usage()
        sys.exit()


def open_file(file_to_open):
    """
    This fucntion will open a file to read the IP addresses that the user provided
    :param file_to_open: The name or the full path of the file to read IP addresses from
    :return: It returns the list of the provided IP addresses
    """
    list_of_ip_addresses = []
    try:
        with open(file_to_open) as f:
            # contents = f.readlines() #This will provide liens with the \n as suffix: ['1.1.1.1\n', '2.2.2.2']
            list_of_ip_addresses = f.read().splitlines()  # It will store the actual values without the \n
        f.close()
        print(f'File {file_to_open} was loaded successfully')

        return list_of_ip_addresses
    except IOError:
        print("******************************************************************************")
        print(f'*************** COULD NOT OPEN THE FILE {file_to_open} **********************')
        print("******************************************************************************")
        usage()
        sys.exit()


def write_json_file(data_to_write):
    """
    This function writes json data into a file.
    source: https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
    :param data_to_write: The json data to be written in the file
    :return: Returns True if the script managed to write the file
    """
    try:
        with open('output.txt', 'w', encoding='utf-8') as outfile:
            json.dump(data_to_write, outfile, ensure_ascii=False, indent=4)

        return True
    except IOError:
        print("********************************************************************************")
        print("*** Unexpected error while opening the output.txt file to write the contents ***")
        print("********************************************************************************")
        usage()
        sys.exit()


def wrong_arguments():
    """
    This function will be used to flag wrong arguments were passed
    :return: It will not return anything, but it will print a useful message to the user
    """
    print("************************************************************************************")
    print("* You have not provided the correct number of arguments. Or not expected arguments *")
    print("* were received.                                                                   *")
    print("* Check the examples below                                                         *")
    print("************************************************************************************")


def fill_queue(port_list_to_fill):
    """
    This function creates a queue based on the list of ports passed to it
    :param port_list_to_fill: The list of ports to be scanned
    :return: Returns a queue with the ports to be scanned. It will be used from the threading
    """
    queue = Queue()
    for port in port_list_to_fill:
        queue.put(port)
    return queue


def portscan(target, port):
    """
    This function creates the socket to perform port scanning. Based on the following resource, the inbuilt function
    connect_ex is more efficient compared to the connect function
    https://stackoverflow.com/questions/48318266/python-socket-connect-vs-connect-ex
    :param target: The target IP to be scanned
    :param port: The port in which the scan will run
    :return: It returns true if the port is open for the specified IP address
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket_family, socket_type
        code = sock.connect_ex((target, port))
        if code == 0:
            sock.close()
            return True
    except:
        return False
    # try:
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket_family, socket_type
    #     sock.connect((target, port))  # it should change to sys.argv[1] or a dynamic variable
    #     return True
    # except:
    #     return False


def worker(queue_passed, target, risky_ports):
    """
    This function will loop all ports by calling the portscan function. It will append any open port to the dictionary
    :param queue_passed: The queue that holds the ports to be scanned
    :param target: The target IP address
    :param risky_ports: The set of risky ports
    :return:
    """
    while not queue_passed.empty():
        port = queue_passed.get()
        if portscan(target, port):  # it will differ to UDP
            print("Port {} is open!".format(port))  # prints the open ports in the terminal
            if port in risky_ports:  # If the open port is within the risky ports, it is flagged as risky in the output
                # Port is turned from int to str to comply with the instructions
                open_ports['findings'].append({"ip_address": target, "open_port": str(port), "risk_port": True})
            else:
                open_ports['findings'].append({"ip_address": target, "open_port": str(port), "risk_port": False})


def portscan_udp(target, port):
    """
    This function creates the socket to perform port scanning on UDP ports. If a firewall blocked access to the UDP
    ports, this script wrongly will return that a port is open as it will not receive an ICMP reply based on the link:
    https://null-byte.wonderhowto.com/how-to/sploit-make-python-port-scanner-0161074/
    :param target: The target IP to be scanned
    :param port: The port in which the scan will run
    :return: It returns true if the port is open for the specified IP address
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket_family, socket_type
        code = sock.connect_ex((target, port))
        if code == 0:
            sock.close()
            return True
    except:
        return False


def worker_udp(queue_passed, target, risky_ports):
    """
    This function will loop all ports by calling the portscan_udp function. It will append any open port to the
    dictionary
    :param queue_passed: The queue that holds the ports to be scanned
    :param target: The target IP address
    :param risky_ports: The set of risky ports
    :return:
    """
    while not queue_passed.empty():
        port = queue_passed.get()
        if portscan_udp(target, port):  # it will differ to UDP
            print("Port {} is open!".format(port))  # prints the open ports in the terminal
            if port in risky_ports:  # If the open port is within the risky ports, it is flagged as risky in the output
                # Port is turned from int to str to comply with the instructions
                open_ports['findings'].append({"ip_address": target, "open_port": str(port), "risk_port": True})
            else:
                open_ports['findings'].append({"ip_address": target, "open_port": str(port), "risk_port": False})

if __name__ == '__main__':
    usage()  # The banner is called
    # If the number of arguments passed is not equal to 4 or the arguments are not correct, the script terminates
    if (len(sys.argv) != 4) or (sys.argv[2] not in ("-t", "-u")) or (sys.argv[3] not in ("-b", "i")):
        wrong_arguments()  # It informs the user that the wrong arguments were passed
        usage()  # It will show the banner with the examples to the user again
        sys.exit()  # The script terminates
    elif sys.argv[1] in ("help", "-h", "h", "?", "--h", "--help", "/?"):  # Banner to be displayed if user wants help
        usage()
        sys.exit()
    elif validate_ip_address(sys.argv[1]):  # Execution block for a single IP address
        print(f'Target ip: {sys.argv[1]}')
        # scanning a single IP in here
        queue = fill_queue(basic_port_list)  # Initialises the Queue
        thread_list = []  # Initialises the thread list
        if sys.argv[2] == "-t":  # Set risky ports for TCP
            print("Scanning TCP ports")
            risk_ports = risk_ports_tcp
            for t in range(1100):  # specify the number of threads you want to run
                # targets the worker function. It passes the queue, target IP and risky ports (TCP/UDP) as arguments
                thread = threading.Thread(target=worker, args=(queue, sys.argv[1], risk_ports,))
                thread_list.append(thread)  # all threads into a list
        else:
            print("Scanning UDP ports")
            risk_ports = risk_ports_udp
            for t in range(1100):  # specify the number of threads you want to run
                # targets the worker function. It passes the queue, target IP and risky ports (TCP/UDP) as arguments
                thread = threading.Thread(target=worker_udp, args=(queue, sys.argv[1], risk_ports,))
                thread_list.append(thread)  # all threads into a list
        t1 = datetime.now()  # Starts the counter
        for thread in thread_list:
            thread.start()
        # waits until all threads are finished to execute the last print statement
        for thread in thread_list:
            thread.join()

        print(f'Open ports for {sys.argv[1]}: ', open_ports['findings'])
        t2 = datetime.now()
        total = t2 - t1
        print("Scanning Completed in: ", total)

        write_json_file(open_ports)

    elif ".txt" in sys.argv[1]:  # Execution block for txt file with multiple IPs
        list_of_ips = open_file(sys.argv[1])  # Returns the list of entries found inside the file
        print(list_of_ips)  # for testing
        if len(list_of_ips) == 1:  # Execution block if a subnet is passed
            print("One entry was found in the file. "
                  "It will be treated as a subnet and the script will validate it now\n")
            list_of_ips = subnet_to_ip(list_of_ips[0])  # Converts the subnet into IP addresses
            print(f'The subnet was validated. The following list of IP addresses will be scanned: {list_of_ips}')
        else:  # Execution block for multiple IP addresses
            print("Validating the IP addresses")
            for ip in list_of_ips:  # It loops the list of IP addresses to validate that the IPs are ok
                if not validate_ip_address(ip):
                    print("*********************************************************************************")
                    print("* A NOT VALID IP ADDRESS WAS FOUND. PLEASE CORRECT THE IP ADDRESSES IN THE FILE *")
                    print("*********************************************************************************")
                    usage()
                    sys.exit()
            print("All IP addresses were scanned and validated")
        # scanning multiple IPs or subnet IPs in here

    else:  # Execution block for wrong IP/file argument
        wrong_arguments()
        usage()
        sys.exit()
