import asyncio
from websockets.legacy.server import Serve
import json
import vgamepad as vg


gamepad_out = vg.VX360Gamepad()


async def echo(websocket):
    print("connected")
    async for message in websocket:
        try:
            data: dict = json.loads(message)
            for key, value in data.items():
                if isinstance(value, list):
                    getattr(gamepad_out, key)(*value)
                else:
                    getattr(gamepad_out, key)(value)
            gamepad_out.update()
        except Exception as e:
            print(e)


async def main():
    async with Serve(echo, "localhost", 8765, ping_timeout=None):
        await asyncio.Future()  # run forever


asyncio.run(main())
