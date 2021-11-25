import ipaddress

# A variable to store the IP addresses when converted from a subnet. Used from "subnet_to_ip" function
list_of_ip_addresses = []


def usage():
    '''
    The method usage prints out the banner of the script as well as examples of the usage and information about The Creator
    '''
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

    USAGE: python georgiosz_scanner.py IP etc.
    Example: python georgiosz_dos.py https://www.example.com

    The georgiosz_scanner.py programme was created by Georgios Zervakis and it is the ultimate port scanner
    tool for several network protocols
    Linkedin : https://www.linkedin.com/in/georgios-zervakis/
    Tweeter  : @Georgios_zm
    Website  : georgiosnetworks.com
    TryHackMe: DrG
    ''')

def validate_ip_address(address):
    '''
    This function will be used to validate that the IP address the user passed is a valid one
    :param address: It will be arg[1] passed directly as a CML option
    :return: Returns True if it is a valid IPv4/v6 or False if it is not a valid IPv4/v6
    '''
    try:
        ip = ipaddress.ip_address(address)
        return True
        # print("IP address {} is valid. The object returned is {}".format(address, ip))
    except ValueError:
        return False
        # print("IP address {} is not valid".format(address))


def subnet_to_ip(subnet_address):
    '''
    This function will produce a list of IP addresses should the user passes a subnet as an input
    :param subnet_address: The subnet that the user passed via the txt file
    :return: The function will return a list of the IP addresses based on the given subnet
    '''
    global list_of_ip_addresses
    #A for loop will loop all IP addresses from a given subnet
    for address in ipaddress.ip_network(subnet_address):
        # Each IP address will be converted to a string and appended into the list
        list_of_ip_addresses.append(str(address))

    return list_of_ip_addresses



