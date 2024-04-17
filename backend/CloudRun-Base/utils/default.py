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

async def some_utility() -> None:
    return
