#!/usr/bin/env python3
"""
    This script initiates the Optimal Framework database with a base structure
"""
if __name__ == "__main__":
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    from of.broker.broker import start_broker

    start_broker(_cfg_filename=os.path.join(script_dir, "config.json"))
