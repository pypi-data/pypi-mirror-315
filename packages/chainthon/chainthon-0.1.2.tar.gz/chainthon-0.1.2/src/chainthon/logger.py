"""
@description: logger module for chainthon
@author: rontom
@license: Apache License, Version 2.0
"""

import logging
import sys
from typing import Optional

def setup_logger(name: str = "chainthon", level: Optional[int] = None) -> logging.Logger:
    """Set up and return a logger instance."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        )
        logger.addHandler(handler)
    
    if level is not None:
        logger.setLevel(level)
    elif not logger.level:
        logger.setLevel(logging.INFO)

    for module in ["socketio", "engineio", "numexpr"]:
        logging.getLogger(module).setLevel(logging.ERROR)
    
    return logger

logger = setup_logger()
