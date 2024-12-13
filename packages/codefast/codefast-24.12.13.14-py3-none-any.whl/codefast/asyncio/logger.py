#!/usr/bin/env python3
import inspect
import os
from codefast.utils import b64decode
import httpx
import pydantic
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_fixed
import sys

logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<level>{time:YYYY-MM-DD HH:mm:ss} | {message}</level>",
    colorize=True
)

logger.add(
    "/tmp/cf.log",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {message}",
    colorize=True
)

API_ENCODED = 'aHR0cHM6Ly9sb2dzLmN1Zm8uY2MvYXBpL2xvZ3MvYWRkCg=='
API = b64decode(API_ENCODED)


class LogData(pydantic.BaseModel):
    filename: str
    linenum: int
    content: str
    level: str
    project: str = "default"

    def __str__(self):
        return f"[{self.project}] {self.filename}:{self.linenum} {self.level} {self.content}"


class AsyncLogger:
    def __init__(self):
        self.project = "default"

    def config(self, project: str):
        self.project = project
        return self

    async def info(self, content: str):
        await add_log("INFO", content, self.project)

    async def error(self, content: str):
        await add_log("ERROR", content, self.project)

    async def warning(self, content: str):
        await add_log("WARNING", content, self.project)

    async def debug(self, content: str):
        await add_log("DEBUG", content, self.project)

    async def critical(self, content: str):
        await add_log("CRITICAL", content, self.project)


async def add_log(level: str, content: str, project: str = "default"):
    caller_frame = inspect.currentframe().f_back.f_back
    filename = os.path.basename(caller_frame.f_code.co_filename)
    line_number = caller_frame.f_lineno

    log_data = LogData(filename=filename,
                       linenum=line_number,
                       content=content,
                       level=level,
                       project=project)

    if level == "INFO":
        logger.info(log_data)
    elif level == "ERROR":
        logger.error(log_data)
    elif level == "WARNING":
        logger.warning(log_data)
    elif level == "DEBUG":
        logger.debug(log_data)
    elif level == "CRITICAL":
        logger.critical(log_data)
    else:
        logger.info(log_data)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    async def send_log_to_api():
        async with httpx.AsyncClient() as client:
            response = await client.post(API,
                                         json={
                                             "content": str(log_data),
                                             "level": level,
                                         },
                                         timeout=30.0)
            response.raise_for_status()

    try:
        await send_log_to_api()
    except httpx.HTTPStatusError as e:
        error_data = {
            "filename":
            filename,
            "linenum":
            line_number,
            "content":
            f"Failed to send log to API. Status code: {e.response.status_code}"
        }
        logger.error(error_data)
    except httpx.RequestError as e:
        error_data = {
            "filename": filename,
            "linenum": line_number,
            "content":
            f"Network error occurred while sending log to API: {str(e)}"
        }
        logger.error(error_data)
    except Exception as e:
        error_data = {
            "filename":
            filename,
            "linenum":
            line_number,
            "content":
            f"Unexpected error occurred while sending log to API: {str(e)}"
        }
        logger.error(error_data)


alogger = AsyncLogger()
