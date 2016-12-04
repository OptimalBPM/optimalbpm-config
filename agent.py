#!/usr/bin/env python3

"""
    This script starts the Optimal BPM agent
"""

import os
script_dir = os.path.dirname(os.path.abspath(__file__))

from plugins.optimalbpm.agent.agent import start_agent

start_agent(_cfg_filename=os.path.join(script_dir, "config.json"))
