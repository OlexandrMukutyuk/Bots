import os

from aiohttp import web


async def media(req: web.Request):
    file_name = req.match_info.get('file_name', "Anonymous")
    file_path = f'{os.getcwd()}/tmp/{file_name}'

    if os.path.isfile(file_path):
        return web.FileResponse(file_path)
    else:
        return web.Response(text="File not found", status=404)
