#!/usr/bin/env python
# coding: utf-8
import os
import uvicorn
import json 
import numpy as np
import logging
import asyncio
import itertools
import warnings
import time
from natsort import natsorted
from datetime import datetime, timezone
from dotenv import load_dotenv
from typing import *

from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, Request, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse

logger = logging.getLogger('default')

ENV = load_dotenv()
if ENV:    
    # Deployment configuration
    LOCAL_DEPLOYMENT = os.getenv('LOCAL_DEPLOYMENT', 'false').lower() == 'true' 
    PORT = os.environ.get('PORT')

async def fastmap(iterable: Iterable, operation: Callable, max_workers=100) -> list:
    """
    Maps an operation over an iterable with 'max_workers' workers.
    
    Parameters:
    - iterable: An Iterable of any type.
    - operation: A Callable that takes an item from iterable and performs an operation.
    - max_workers: The maximum number of worker threads to use.
    
    Returns:
    - A list containing None for successful operations or an exception if an error occurred.
    
    Example:
    >> item_list: Iterable = ['this is an item', 'this is another item']
    >> result = fastmap(
            iterable=item_list, 
            operation=print_function
        )
    >> 'this is an item'\n'this is another item'
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(operation, iterable, timeout=None))
