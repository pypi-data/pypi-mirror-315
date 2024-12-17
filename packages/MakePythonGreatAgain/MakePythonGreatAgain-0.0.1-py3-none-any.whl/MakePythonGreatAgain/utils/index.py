import os


def parseDictKeys(dict):
    return list(dict.keys())

def parseDictValues(dict):
    return list(dict.values())

def clearScreen(OS=os.name):
    if OS == 'nt':
        os.system('cls')
    else: # Some other shitty OS I haven't heard of
        os.system('clear')


# Function name: pingTestWin
# Description: This function returns the hostname of the Windows machine
# Parameters: None
# Returns string
def pingTestWin(destinations=["129.21.3.17", "8.8.8.8"]):
    status_dict = {}
    for destination in destinations:
        response = os.system("ping -n 1 " + destination + " >nul 2>&1")
        status_dict[destination] = 1 if response == 0 else 0
    return status_dict

# Function name: pingTestLinux
# Description: This function returns the hostname of the Windows machine
# Parameters: destinations(OPT): array(str)
# Returns dictionary
def pingTestLinux(destinations=["129.21.3.17", "8.8.8.8"]):
    status_dict = {}
    for destination in destinations:
        response = os.system("ping -c 1 " + destination + " >/dev/null 2>&1")
        status_dict[destination] = 1 if response == 0 else 0
    return status_dict
