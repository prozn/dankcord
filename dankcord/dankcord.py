
__version__ = "0.1.0"

import sys
import logging
import logging.handlers

def main():
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.WARNING) #DEBUG)
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    if sys.argv[1] == "startbot":
        from .dankbot import startbot
        print('Starting bot...')
        startbot()
    elif sys.argv[1] == "esiupdate":
        from .esiupdate import start
        print('Starting esi update service')
        start()
    else:
        print('You need to specify startbot or esiupdate function as the first argument')

    print('Bot has ended....')

if __name__ == '__main__':
    main()