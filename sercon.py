#!/usr/bin/env python
# This is a background server which implements a websocket interface to be
# consumed by xterm.js frontend code, running in the browser. Think of it as a
# microservice. It must be running on the device connected to the 8-bit host
# systems.
import asyncio
from websockets.asyncio.server import serve

from lib.com import Com

con0 = Com()


def reader():
    return con0.read()


def writer(msg):
    con0.write(msg)


async def readWrapper(websocket):
    loop = asyncio.get_running_loop()
    for line in await loop.run_in_executor(None, reader):
        await websocket.send(bytes(line.encode()))


async def writeWrapper(websocket):
    loop = asyncio.get_running_loop()
    async for msg in websocket:
        await loop.run_in_executor(None, writer, msg)


async def serIo(websocket):
    await asyncio.gather(readWrapper(websocket), writeWrapper(websocket))


async def main():
    async with serve(serIo, "localhost", 8079) as server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
