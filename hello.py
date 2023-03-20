import time
import json
import asyncio
import itertools
from websockets.legacy import client
from inputs import DeviceManager, get_gamepad

# from pyinput.keyboard import Key, Controller
from pygame import joystick
import pygame


def quad_prop_output(thrust, roll, pitch, yaw):
    yaw = yaw * 0.5
    pitch = pitch * 0.5
    roll = roll * 0.5
    fl = thrust + roll + pitch + yaw
    fr = thrust - roll + pitch - yaw
    bl = thrust + roll - pitch - yaw
    br = thrust - roll - pitch + yaw
    return [min(1, max(-1, x)) for x in [fl, fr, bl, br]]


def handle_button(button, up_down):
    ...


def handle_axis(axis):
    ...


async def run():
    pygame.init()
    js_id = next(i for i in range(10) if "Taranis" in joystick.Joystick(i).get_name())
    js = joystick.Joystick(js_id)
    js.init()
    # assert js.get_name() == "FrSky Taranis Joystick"

    latest_axis = [0 for i in range(js.get_numaxes())]
    async with client.Connect("ws://localhost:8765", ping_timeout=None) as websocket:

        async def send_dict(d):
            await websocket.send(json.dumps(d).encode())

        for t in itertools.count(0, 1 / 100):
            axis_change = False
            for event in list(pygame.event.get())[::-1]:
                if event.type == pygame.JOYAXISMOTION:
                    axis_change = True
                    latest_axis[event.dict["axis"]] = event.dict["value"]

                elif event.type == pygame.JOYBUTTONDOWN:
                    ...

                elif event.type == pygame.JOYBUTTONUP:
                    ...
                else:
                    print(pygame.event.event_name(event.type))
            if axis_change:
                val = (time.time() % 10) / 10.0
                await send_dict({"left_joystick_float": [val, -val]})
            await asyncio.sleep(max(0, t - time.time()))


asyncio.run(run())
