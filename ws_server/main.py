import asyncio

import websockets


async def ping_pong(websocket):
    while True:
        msg_in = await websocket.recv()
        if msg_in == "ping":
            print("received PING, answering PONG")
            await websocket.send("pong")
        elif msg_in == "pong":
            print("received PONG, answering PING")
            await websocket.send("ping")
        else:
            print(msg_in)
            await websocket.send("unknown")


async def main():
    async with websockets.serve(ping_pong, "localhost", 1500):
        print("start waiting for ping")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
