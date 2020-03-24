import logging

from fastapi import FastAPI, Request


logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/base_url")
def base_url(request: Request):
    return request.base_url


@app.get("/async")
async def async_endpoint():
    return {"Hello": "World"}

@app.get("/sync")
def sync_endpoin():
    return {"Hello": "World"}

@app.get("/logs")
def show_logs():
    logger.debug("DEBUG message")
    logger.info("INFO message")
    logger.warning("WARNING message")
    logger.error("ERROR message")
    return {"msg": "Hello from logger"}

@app.get("/request_info")
def request_info(request: Request):
    return {
        "url": request.url,
        "headers": request.headers,
        "base_url": request.base_url,
        "query_params": request.query_params,
        "path_params": request.path_params,
        "client": request.client,
        "cookies": request.cookies,
        "state": request.state,
    }

