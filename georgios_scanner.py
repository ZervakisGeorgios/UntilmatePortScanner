import ipaddress
import sys
import json
import time
import socket
import threading
from queue import Queue

# Queue module implements multi-producer/consumer queues useful in threaded https://docs.python.org/3/library/queue.html
queue = Queue()
port_list = range(1, 1024 + 1)  # The standard ports to be scanned
open_ports = {'findings': []}  # Initialises the dictionary that will store open ports


def usage():
    """
    The method usage prints out the banner of the script as well as examples of the usage and information about The Creator
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
    for port in port_list_to_fill:
        queue.put(port)


def portscan(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))  # it should change to sys.argv[1] or a dynamic variable
        return True
    except:
        return False


def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):  # it will differe to UDP
            print("Port {} is open!".format(port))
            open_ports.append(port)


if __name__ == '__main__':
    usage()  # The banner is called
    # If the number of arguments passed is not equal to 4 or the arguments are not correct, the script terminates
    if (len(sys.argv) != 4) or (sys.argv[2] not in ("-t", "-u")) or (sys.argv[3] not in ("-b", "i")):
        wrong_arguments()   # It informs the user that the wrong arguments were passed
        usage()             # It will show the banner with the examples to the user again
        sys.exit()          # The script terminates
    elif sys.argv[1] in ("help", "-h", "h", "?", "--h", "--help", "/?"):  # Banner to be displayed if user wants help
        usage()
        sys.exit()
    elif validate_ip_address(sys.argv[1]):  # Execution block for a single IP address
        print("valid ip")
    elif ".txt" in sys.argv[1]:             # Execution block for txt file with multiple IPs
        list_of_ips = open_file(sys.argv[1])
        print(list_of_ips)
    else:                                   # Execution block for wrong IP/file argument
        wrong_arguments()
