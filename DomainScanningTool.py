#!/usr/bin/env python

import binascii
import socket
import random
import os

DEFAULT_SERVER = '1.1.1.1'
DEFAULT_PORT = 53
AUTHOR = 'dynos01'
EMAIL = 'i@dyn.im'
VERSION = '1.0'

def send(message, server, port):
    """
    Sends UDP packet to server and waits for response.

    Args:
        message: Encoded data, which will be sent.
        server: DNS server address. both IPv4 and IPv6 are supported.
        port: DNS server port.

    Returns:
        A string containing raw response.
    """
    message = message.strip()
    addr = (server, port)

    if '.' in server:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    try:
        s.sendto(binascii.unhexlify(message), addr)
        data, address = s.recvfrom(4096)
    finally:
        s.close()

    return binascii.hexlify(data).decode()

def buildMessage(domain):
    """
    Creates a DNS request according to RFC2929. Attributes other than domain name are hard-coded.

    Args:
        domain: The domain name to be checked.

    Returns:
        A string containing raw DNS request.
    """
    message = '{:04x}'.format(random.randint(0, 65535)) #Generate an random request ID
    message += '01000001000000000000'

    #Encode parts of the given domain name into our request
    addr = domain.split('.')
    for i in addr:
        length = '{:02x}'.format(len(i))
        addr = binascii.hexlify(i.encode())
        message += length
        message += addr.decode()

    message += '0000060001'

    return message

def validateServer(ip, port):
    """
    Checks if the given IP-port combination is valid.

    Args:
        ip: IPv4 or IPv6 address.
        port: Port number.

    Returns:
        A bool value. True for valid and False for invalid.
    """
    if port <= 0 or port > 65535:
        return False

    try:
        if '.' in ip:
            socket.inet_pton(socket.AF_INET, ip)
        else:
            socket.inet_pton(socket.AF_INET6, ip)
    except:
        return False

    return True

def check(domain, server, port):
    """
    Sends the request, reads the raw response and checks the ANCOUNT attribute according to RFC2929.

    Args:
        domain: Domain name to be checked.
        server: DNS server to check against.
        port: DNS server port.

    Returns:
        A bool value representing if the domain exists.

    """
    message = buildMessage(domain)
    response = send(message, server, port)
    rcode = '{:b}'.format(int(response[4:8], 16)).zfill(16)[12:16]
    return False if rcode == '0011' else True

def main():
    print('Domain scanning tool version %s' % VERSION)
    print('Author: %s <%s>' % (AUTHOR, EMAIL))

    server = []
    port = []
    dns = input('Please input a list of DNS servers (IPv4 or IPv6), which will be used to check against: ')
    if len(dns) == 0:
        server.append(DEFAULT_SERVER)
        port.append(DEFAULT_PORT)
    else:
        dns = dns.split(',')
        for i, item in enumerate(dns):
            item = item.strip()
            if '[' in item:
                s = item.split(']')[0][1:]
                p = item.split(']')[1][1:]
            else:
                s = item.split(':')[0]
                p = item.split(':')[1]
            p = int(p)
            if not validateServer(s, p):
                print('Invalid DNS server.')
                return
            server.append(s)
            port.append(p)

    tld = input('Please input the suffixes to be scanned. If you want to scan multiple suffixes at once, please use commas to separate the list. \n')
    tld = tld.split(',')
    for i, item in enumerate(tld):
        tld[i] = item.strip()

    dictFile = input('Please input the path for dictionary file. \n')
    if not os.access(dictFile, os.R_OK):
        print('Unable to read dictionary file. ')
        return

    resultFile = input('If you want to save the results to a file, input its path. Otherwise, press ENTER. \n')
    if len(resultFile) > 0:
        result = open(resultFile, 'a')

    input('All data collected. Press ENTER to start scanning. ')

    for line in open(dictFile):
        for suffix in tld:
            domain = line.strip() + '.' + suffix
            i = random.choice(range(len(server)))
            if not check(domain, server[i], port[i]):
                print(domain + ' is available. ')
                if len(resultFile) > 0:
                    result.write(domain + ' is available. \n')

    print('Scanning finished. ')
    if len(resultFile) > 0:
        print('Results have been saved to ' + resultFile + '.')

if __name__ == '__main__':
    main()
