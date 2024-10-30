import uuid
import asyncio
import aiohttp
from loguru import logger
from fastapi import FastAPI, Request, Path, Header, Body

app = FastAPI()

async def post_async(
    task_id: str,
    url: str,
    headers: dict,
    query_params: dict,
    data: dict
):
    logger.debug(f"[{task_id}] Sending request to {url} with headers: {headers}, query_params: {query_params}, body_params: {data}")
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, params=query_params, json=data, timeout=15) as response:
            if response.status != 200:
                logger.error(f"[{task_id}] Request failed with status code {response.status} and reason: {response.reason}")
                return
            response_json = await response.json()
            logger.info(f"[{task_id}] Request successful with response: {response_json}")
            return
        
@app.get("/")
async def root():
    return {"status": 200, "message": "Welcome to the Async API Relay!"}

@app.post("/{url:path}")
async def post(
    request: Request,
    url: str = Path(..., description="URL to send the request"),
    # header_params: dict = Header(None, description="[Optional] Header parameters to send in the request"),
    # body_params: dict = Body(None, description="[Optional] Body parameters to send in the request"),
):
    # Split raw url to base_url and query parameters
    logger.debug(f"URL: {url}")
    if '?' in url:
        base_url, query_params = url.split('?')
        query_params = query_params.split('&')
        query_params = {param.split('=')[0]: param.split('=')[1] for param in query_params}
    else:
        base_url = url
        query_params = {}
    
    # Join manual query params with the request one
    query_params.update(dict(request.query_params))

    headers = dict(request.headers)
    data = await request.json()

    # Post an async task in the background
    task_id = str(uuid.uuid4())
    asyncio.create_task(post_async(task_id, base_url, headers, query_params, data))
    logger.info(f"[{task_id}] Request sent in the background")
    return {"status": 200, "message": f"Request sent in the background (Task ID: {task_id})"}