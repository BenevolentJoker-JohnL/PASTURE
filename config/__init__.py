#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pasture/config/__init__.py

Marks the config directory as a Python package.
"""

import os
import json
from pathlib import Path

def get_default_config_path():
    """Return the path to the default configuration file."""
    return Path(__file__).parent / "default_config.json"

def load_default_config():
    """Load and return the default configuration as a dictionary."""
    config_path = get_default_config_path()
    with open(config_path, 'r') as f:
        return json.load(f)
