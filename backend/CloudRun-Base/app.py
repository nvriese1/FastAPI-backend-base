#!/usr/bin/env python
# coding: utf-8

# Base modules / libraries
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

# Start logging
logging.basicConfig(level=logging.INFO, force=True) 

# Custom modules / libraries
from utils.default import *

# Load environment
load_dotenv(override=True)

# Deployment configuration
LOCAL_DEPLOYMENT = os.getenv('LOCAL_DEPLOYMENT', 'false').lower() == 'true'  
PORT = os.environ.get('PORT')    
logging.info(f'PORT: {PORT}')

# Placeholder for some startup process (loading models, etc.)
async def startup_process() -> None:
    # [Startup process code]
    return

# Placeholder for some shutdown process (clearing memory, etc.)
async def shutdown_process() -> None:
    # [Shutdown process code]
    return

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # Startup logic
    await startup_process()
    yield
    # Shutdown logic
    await shutdown_process()

app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def example_auth_middleware(request: Request, call_next: Callable):
    
    authorization: str = request.headers.get("Authorization", None)
    token = ""
    
    if authorization is not None:
        scheme, token = authorization.split()
    
    request.state.token = token
    response = await call_next(request)
    return response


@app.get('/')
async def health_check():
    return {"message": "No issues to report."}

   
@app.post('/example_endpoint')
async def example_endpoint(raw_request: Request):
    
    try:
        request = await raw_request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    logging.info(f"Request recieved: {request}") 
    
    # [Endpoint process code]
    
    response = {"response": "Hello world!"}
    return response


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=PORT)