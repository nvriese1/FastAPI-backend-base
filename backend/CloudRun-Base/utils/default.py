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

def batch_operation(
    items: List[Any],
    operation: Callable, 
    **kwargs,
) -> List[Any]:
    """Performs a single operation on a batch of items with optional keyword arguments."""
    results = [operation(item, **kwargs) for item in items]
    return results

async def fastmap(
    iterable: Iterable, 
    operation: Callable, 
    batch_size: int = 5, 
    max_workers: int = 100, 
    **kwargs,
) -> List:
    """
    Maps an operation over an iterable with 'max_workers' workers and optional kwargs, maintaining input order.
    
    Parameters:
    - iterable: An Iterable of any type.
    - operation: A Callable that applies to a batch of items from iterable.
    - batch_size: Number of items in each batch.
    - max_workers: The maximum number of worker threads to use.
    - kwargs: Additional keyword arguments to pass to the operation.
    """
    if not iterable:
        return iterable
    
    batch_size = batch_size if batch_size <= len(iterable) else len(iterable)
    batches = [iterable[i:i + batch_size] for i in range(0, len(iterable), batch_size)]
    optimal_workers = min(len(batches), max_workers)
    loop = asyncio.get_running_loop()
    
    with ThreadPoolExecutor(max_workers=optimal_workers) as executor:
        futures = [loop.run_in_executor(executor, lambda b=batch: batch_operation(b, operation, **kwargs)) for batch in batches]
        results = await asyncio.gather(*futures)
        return [item for sublist in results for item in sublist]
