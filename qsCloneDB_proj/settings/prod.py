# PRODUCTION SETTINGS

from __future__ import absolute_import
from .base import *
import json

with open('/etc/config.json') as config_file:
    config = json.load(config_file)

SECRET_KEY = config['SECRET_KEY']

DEBUG = False