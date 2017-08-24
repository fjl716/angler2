import service
import sys
import os

if __name__ == "__main__":
    os.environ['ANGLER_ID'] = '58f9a41a7d078e0cae4626ef'
    os.environ['ZOOKEEPER_HOSTS'] = '127.0.0.1:2181'
    service.main(sys.argv)
