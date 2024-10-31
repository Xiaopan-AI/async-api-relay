import uuid
import json
import asyncio
import aiohttp
from loguru import logger
from fastapi import FastAPI, Request, Path

app = FastAPI()

async def post_async(
    task_id: str,
    url: str,
    headers: dict,
    params: dict,
    data: dict
):
    if headers:
        # Just clean up and use only the "User-Agent" and "Content-Type" headers
        headers = {
            "User-Agent": headers.get("user-agent", "Apifox/1.0.0 (https://apifox.com)"),
            "Content-Type": headers.get("content-type", "application/json")
        }
    if not url.startswith("http"):
        attempts = [f"https://{url}", f"http://{url}"]
    for try_url in attempts:
        try:
            logger.debug(f"[{task_id}] Sending request to {try_url} with headers: {headers}, params: {params}, data: {data}")
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(try_url, headers=headers, params=params, json=data) as response:
                    if response.status != 200:
                        logger.error(f"[{task_id}] Request failed with status code {response.status} and reason: {response.reason}")
                        return
                    response_json = await response.json()
                    logger.info(f"[{task_id}] Request successful with response: {response_json}")
                    return
        except:
            continue
        
@app.get("/")
async def root():
    return {"status": 200, "message": "Welcome to the Async API Relay!"}

@app.post("/{url:path}")
async def post(
    request: Request,
    url: str = Path(..., description="URL to send the request"),
):
    headers = dict(request.headers)
    params = dict(request.query_params)
    data = await request.json()

    # Post an async task in the background
    task_id = str(uuid.uuid4())
    asyncio.create_task(post_async(task_id, url, headers, params, data))
    logger.info(f"[{task_id}] Request sent in the background")
    return {"status": 200, "message": f"Request sent in the background (Task ID: {task_id})"}
