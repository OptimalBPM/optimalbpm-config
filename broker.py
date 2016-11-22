#!/usr/bin/env python3
"""
    This script initiates the Optimal Framework database with a base structure
"""
import os
script_dir = os.path.dirname(__file__)
from of.broker.broker import start_broker

start_broker(_cfg_filename=os.path.join(script_dir, "config.json"))
