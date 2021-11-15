#!/usr/bin/python3
import datetime
import itertools
import netifaces
import logging
import socket
import struct
import time
from typing import Tuple, Optional, Dict, Any

#Get the IP address of the RoboRIO
def read_addr() -> Optional[str]:
    try:
        ifaddresses = netifaces.ifaddresses('usb0')  # type: Dict[int, Any]
    except:
        return None
    addresses = ifaddresses.get(netifaces.AF_INET)
    if addresses is None:
        return None
    else:
        return "172.22.11.2"

#Try to connecy to the RoboRIO
def try_conn(addr: Tuple[str, int]) -> bool:
    try:
        sock = socket.create_connection(addr, timeout=1)
        sock.close()
        return True
    except OSError:
        return False

#Counter function
def counter():
    yield from range(1, 2 ** 16)
    yield from itertools.cycle(range(0, 2 ** 16))

#Main loop
def main():
    #While loop to keep everything running
    while True:
        address = read_addr()
        if address is None:
            #Log if there is a problem
            print('USB Not found. Waiting 15 seconds to try again...')
            time.sleep(15)
            continue
        tcp_addr = (address, 22)
        if not try_conn(tcp_addr):
            continue
        #Log if connected
        print('Connected to: %s', tcp_addr)
        #Setup the message
        header = bytearray((0x00, 0x00, 0x01, 0x00, 0x10, 0x03))
        addr = (address, 1110)
        sock = socket.socket(type=socket.SOCK_DGRAM)
        current_time = 0
        current_dtime = datetime.datetime.utcnow()
        msg = struct.pack('>i' + 'B' * 8, current_time,
                          current_dtime.second, current_dtime.minute, current_dtime.hour,
                          current_dtime.day, current_dtime.month, current_dtime.year - 1900, 0x10, 0x10)
        #Full sends only
        sock.sendto(header + b'\x0F' + msg, addr)

        #For loop to stay connected and send the enable packet
        for i in counter():
            if i % 10 == 0 and not try_conn(tcp_addr):
                print("Disconnected from", tcp_addr)
                break
            header[0:2] = struct.pack('>H', i)
            if i > 20:
                header[3] = 0x04;
            sock.sendto(header, addr)
            time.sleep(0.02)

#Thunderbirds are go! FAB.
if __name__ == "__main__":
    main()

