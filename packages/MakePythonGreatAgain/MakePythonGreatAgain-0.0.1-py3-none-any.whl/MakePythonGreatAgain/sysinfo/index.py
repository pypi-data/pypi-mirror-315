import os
import platform
import re
import subprocess
from operator import contains

from MakePythonGreatAgain.MPGAResponse import MPGAResponse


# Function name: getHostname
# Description: This function returns the hostname of the machine
# Parameters: None
# Returns MPGAResponse
def getHostname():
    return MPGAResponse(200, platform.node())

# Function name: getDefaultGatewayLinux
# Description:
# Parameters: None
# Returns MPGAResponse
def getDefaultGatewayLinux():
    return subprocess.check_output("ip route show | awk '/default/ {print $3}'", shell=True).decode().strip()


# Function name: getDefaultGatewayLinux
# Description:
# Parameters: None
# Returns MPGAResponse
def getDefaultGatewayLinuxBackup():
    p = subprocess.Popen(["ip r"], stdout=subprocess.PIPE, shell=True)
    out = p.stdout.read().decode('utf-8').split()[2]
    return out

# Function name: setHostnameLinux
# Description: Sets the hostname of the machine
# Parameters: hostname: str
# Returns MPGAResponse
def setHostnameLinux(hostname):
    # Check if name starts with invalid chars
    if re.match(r'^[a-zA-Z0-9]', hostname):
        result = os.system("sudo hostnamectl set-hostname " + hostname)
        return MPGAResponse(200, result, "Hostname change success.")
    else:
        return MPGAResponse(400, 1, "Please make sure the hostname is typed correctly.")


# Function name: getIPAddressesLinux
# Description: Gets the IP addresses of the machine, excluding IPV6 and localhost
# Parameters: None
# Returns MPGAResponse
def getIPAddressesLinux():
    results = subprocess.check_output("ip a | awk '/inet/ {print $2}'", shell=True).decode().strip()

    # Split up each IP
    results = results.split("\n")

    # Remove 127.0.0.1
    # results = an array of (var ip) for ip in results if ip contains any form of 127.0.0.1
    results = [ip for ip in results if not contains(ip, "127.0.0.1")]

    # Remove IPV6 Addresses and any wildcards (anything with a :)
    results = [ip for ip in results if not contains(ip, ":")]

    # Remove the subnet mask
    results = [ip.split("/")[0] for ip in results]


    return MPGAResponse(200, results)


# Function name: getOSInfoLinux
# Description: Gets information about the OS, version, and kernel
# Parameters: None
# Returns MPGAResponse
def getOSInfoLinux():
    os = platform.system()
    version = platform.version()
    kernel = platform.release() if platform.release() else "N/A"
    return MPGAResponse(200, [os, version, kernel])

def getStorageInfoLinux():
    return MPGAResponse(200, subprocess.check_output("df -h", shell=True).decode().strip())