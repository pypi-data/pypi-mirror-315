"""
@description: logger module for chainthon
@author: rontom
@license: Apache License, Version 2.0
"""
import logging
import sys

logging.basicConfig(
    level=logging.INFO, 
    stream=sys.stdout, 
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S")

for module in ["socketio", "engineio", "numexpr"]:
    logging.getLogger(module).setLevel(logging.ERROR)

logger = logging.getLogger("chainthon")