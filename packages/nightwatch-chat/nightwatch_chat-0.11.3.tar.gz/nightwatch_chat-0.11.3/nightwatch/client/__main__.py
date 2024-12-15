# Copyright (c) 2024 iiPython

# Modules
import os
import re
import typing
import requests
from threading import Thread
from argparse import ArgumentParser

import urwid
import websockets
from websockets.sync.client import connect

from nightwatch import __version__, HEX_COLOR_REGEX

from . import config
from .extra.ui import NightwatchUI
from .extra.select import menu
from .extra.wswrap import ORJSONWebSocket

# Initialization
if os.name == "nt":
    urwid.set_encoding("utf-8")

# Connection handler
def connect_loop(host: str, port: int, username: str) -> None:
    protocol, url = "s" if port == 443 else "", f"{host}:{port}"

    # Perform authentication
    resp = requests.post(f"http{protocol}://{url}/api/join", json = {"username": username, "hex": config["client.color"]}).json()
    if resp.get("code") != 200:
        exit(f"\nCould not connect to {url}. Additional details:\n{resp}")

    destination = f"ws{protocol}://{url}/api/ws?authorization={resp['authorization']}"
    try:
        with connect(destination) as ws:
            ws = ORJSONWebSocket(ws)

            # Handle fetching server information
            response = ws.recv()

            # Create UI
            ui = NightwatchUI(ws)
            loop = urwid.MainLoop(ui.frame, [
                ("yellow", "yellow", ""),
                ("gray", "dark gray", "", "", "#555753", ""),
                ("green", "dark green", "")
            ])
            loop.screen.set_terminal_properties(2 ** 24)  # Activate 24-bit color mode

            # Individual components
            loop.screen.register_palette_entry("time", "dark green", "", foreground_high = config["colors.time"] or "#00FF00")
            loop.screen.register_palette_entry("sep", "dark gray", "", foreground_high = config["colors.sep"] or "#555753")

            # Handle messages
            def message_loop(ws: ORJSONWebSocket, ui: NightwatchUI) -> None:
                try:
                    while ws.ws:
                        ui.on_message(ws.recv())

                except websockets.exceptions.ConnectionClosed:
                    pass

            Thread(target = message_loop, args = [ws, ui]).start()

            # Start mainloop
            ui.on_ready(loop, response["data"])
            loop.run()

    except websockets.exceptions.InvalidURI:
        exit(f"\nCould not connect to {destination} due to an HTTP redirect.\nPlease ensure you entered the correct address.")

    except OSError:
        exit(f"\nCould not connect to {destination} due to an OSError.\nThis is more then likely because the server is not running.")

# Entrypoint
def start_client(
    address: typing.Optional[str] = None,
    username: typing.Optional[str] = None
):
    username = username or config["client.username"]

    # Start main UI
    print(f"\033[H\033[2J✨ Nightwatch | v{__version__}\n")
    if username is None:
        print("Hello! It seems that this is your first time using Nightwatch.")
        print("Before you can connect to a server, please set your desired username.\n")

        username = input("Username: ")
        config.set("client.username", username)
        print("\033[4A\033[0J", end = "")  # Reset back up to the Nightwatch label

    # Handle color setup
    color = config["client.color"] or ""
    if not re.match(HEX_COLOR_REGEX, color):
        while True:
            print("For fun, you can select a color for your username.")
            print("Please enter the HEX code (6 long) you would like to have as your color.")
            color = (input("> #") or "ffffff").lstrip("#")

            # Validate their color choice
            if re.match(HEX_COLOR_REGEX, color):
                break

            print("\033[3A\033[0J", end = "")

        print("\033[3A\033[0J", end = "")
        config.set("client.color", color)

    # Handle server address
    if address is None:
        servers = config["client.servers"]
        if servers is None:
            servers = ["nightwatch.iipython.dev"]
            config.set("client.servers", servers)

        print(f"Hello, {username}. Please select a Nightwatch server to connect to:")
        address = menu.show(servers)
        print()

    print(f"Establishing connection to {address} ...")

    # Parse said address
    if ":" not in address:
        host, port = address, 443

    else:
        host, port = address.split(":")

    # Connect to server
    try:
        connect_loop(host, int(port), username)

    except KeyboardInterrupt:
        print("\033[5A\033[0J", end = "")  # Reset back up to the Nightwatch label
        print(f"Goodbye, {username}.")

# Initialization
def main() -> None:
    ap = ArgumentParser(
        prog = "nightwatch",
        description = "The chatting application to end all chatting applications.\nhttps://github.com/iiPythonx/nightwatch",
        epilog = "Copyright (c) 2024 iiPython"
    )
    ap.add_argument("-a", "--address", help = "the nightwatch server to connect to")
    ap.add_argument("-u", "--username", help = "the username to use")
    ap.add_argument("-r", "--reset", action = "store_true", help = "reset the configuration file")

    # Launch client
    args = ap.parse_args()
    if args.reset:
        fetch_config("config").reset()

    start_client(args.address, args.username)
