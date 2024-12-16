#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: the basic settings for ArticleAnalyst
@version: 1.0.0
@file: settings.py
@time: 2023/2/15 9:32
"""
import os

baseDir = os.path.dirname(os.path.abspath(__file__))

# optional settings
maxTry = 5  # The max times to send a request
saveDir = os.path.join(baseDir, "download", "test")  # The dir to save article information downloaded from PubMed
if not os.path.exists(saveDir):
    os.mkdir(saveDir)

