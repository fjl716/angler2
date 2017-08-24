from time import sleep

from angler import Angler
import sys
import logging
import os

logging.basicConfig(level=logging.INFO)


def main(argv):
    angler_id = os.environ.get('ANGLER_ID')
    zookeeper_hosts = os.environ.get('ZOOKEEPER_HOSTS')

    angler = Angler(angler_id, zookeeper_hosts)
    angler.start()
    while True:
        sleep(1)


if __name__ == "__main__":
    main(sys.argv)
