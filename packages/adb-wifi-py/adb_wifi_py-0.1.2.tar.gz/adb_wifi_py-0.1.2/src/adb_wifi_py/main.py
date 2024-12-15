#!/usr/bin/env python3

"""
Android 11+
Pair and connect devices for wireless debug on terminal

python-zeroconf: A pure python implementation of multicast DNS service discovery
https://github.com/jstasiak/python-zeroconf
"""

import logging
import subprocess
from sys import argv, exit

from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
from qrcode import QRCode

# Constants
TYPE = "_adb-tls-pairing._tcp.local."
NAME = "debug"
PASSWORD = "123456"
FORMAT_QR = "WIFI:T:ADB;S:{name};P:{password};;"
CMD_SHOW = "qrencode -t UTF8 '{data}'"
CMD_PAIR = "adb pair {ip}:{port} {code}"
SUCCESS_MSG = "Successfully paired"


class ADBListener(ServiceListener):
    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        logging.debug(f"Service {name} removed.")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        logging.debug(f"Service {name} added.")
        logging.debug(f"Service info: {info}")
        self.pair(info)

    def pair(self, info) -> None:
        cmd = CMD_PAIR.format(ip=info.server, port=info.port, code=PASSWORD)
        logging.debug(f"Executing command: {cmd}")
        process = subprocess.run(cmd, shell=True, capture_output=True)
        stdout = process.stdout.decode()
        logging.debug(f"{stdout=}\n{process.stderr=}")

        if process.returncode != 0:
            print("Pairing failed.")
            exit(1)

        if stdout.startswith(SUCCESS_MSG):
            print(SUCCESS_MSG + "!")
            exit(0)

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        pass


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG if len(argv) > 1 else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    qr = QRCode()
    qr.add_data(FORMAT_QR.format(name=NAME, password=PASSWORD))
    qr.make(fit=True)
    qr.print_ascii(invert=True)

    print("Scan QR code to pair new device.")
    print(
        "[System]->[Developer options]->[Wireless debugging]->[Pair device with QR code]"
    )

    zeroconf = Zeroconf()
    listener = ADBListener()
    browser = ServiceBrowser(zeroconf, TYPE, listener)

    browser.join()  # Waiting until thread ends

    zeroconf.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\rClosing...")
