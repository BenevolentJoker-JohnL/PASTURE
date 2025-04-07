#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pasture/tests/__init__.py

Marks the tests directory as a Python package.
Contains shared testing utilities.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to enable imports of the pasture package
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
