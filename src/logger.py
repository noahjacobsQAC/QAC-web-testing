# -*- coding: utf-8 -*-
# https://docs.python.org/3/library/logging.html

import logging.config
logger = logging.config.fileConfig(fname=r'./config/log.conf')
