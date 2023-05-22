from time import time
from datetime import datetime
from aiohttp.web import Request
from aiohttp.multipart import MultipartReader


def get_timestamp() -> float:
    return time()


def strftime(timestamp: float = get_timestamp(), time_format: str = '%m.%d.%Y %H:%M:%S') -> str:
    return datetime.fromtimestamp(timestamp).strftime(time_format)


async def decode_form_data(request: Request) -> dict:
    if request.content_type == 'multipart/form-data':
        form_data: dict = {}
        reader: MultipartReader = await request.multipart()
        async for field in reader:
            if field.filename:
                form_data[field.name] = {'filename': field.filename, 'content': await field.read()}
            else:
                form_data[field.name] = await field.text()
        return form_data
    if request.method == 'GET':
        return dict(request.rel_url.query)
    else:
        return dict(await request.post())
