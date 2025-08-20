#!/usr/bin/env python
# This is a background server which implements a websocket interface to be
# consumed by xterm.js frontend code, running in the browser. Think of it as a
# microservice. It must be running on the device connected to the 8-bit host
# systems.
import asyncio
from websockets.asyncio.server import serve

from lib.com import Com

con0 = Com()

async def serIo(websocket):
    async for message in websocket:
        con0.write(message, False)
        sout = con0.read()
        for line in sout:
            await websocket.send(line)


async def main():
    async with serve(serIo, "localhost", 8079) as server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
