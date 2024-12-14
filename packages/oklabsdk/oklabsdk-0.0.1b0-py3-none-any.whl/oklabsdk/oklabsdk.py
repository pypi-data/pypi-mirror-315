#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
import os 

load_dotenv()

def main():
    print("Hello, world!")
    print(os.getenv("API_KEY"))