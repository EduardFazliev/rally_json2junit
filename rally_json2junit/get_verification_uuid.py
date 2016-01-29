#!/usr/bin/python

import sys
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error("File name is missed")
    else:
        with open(sys.argv[1]) as fr:
            with open("verification.uuid", 'w') as fw:
                fw.write(fr.readlines()[-1].split("Verification UUID: ")[1])
