# Copyright (c) 2024 iiPython

# Modules
import shlex
from typing import Tuple
from datetime import datetime
from types import FunctionType

import urwid
import emoji

from .commands import commands
from .wswrap import ORJSONWebSocket
from ..vendor.scroll import Scrollable, ScrollBar

from nightwatch.client import config

# Input edit class
class InputEdit(urwid.Edit):
    def __init__(self, send_message: FunctionType) -> None:
        self.send_message = send_message
        super().__init__("> ", wrap = "clip")

    def keypress(self, size: Tuple[int], key: str) -> None:
        if key != "enter":
            return super().keypress(size, key)

        elif not self.edit_text.strip():
            return

        self.send_message(self.edit_text)
        self.edit_text = ""

# Main UI class
class NightwatchUI():
    def __init__(self, websocket: ORJSONWebSocket) -> None:
        self.last_author, self.last_time = None, 0
        self.websocket = websocket

        # Main urwid setup
        self.pile = urwid.Pile([])
        self.scroll = Scrollable(urwid.Filler(self.pile, valign = "top"))
        self.frame = urwid.Frame(ScrollBar(self.scroll), footer = InputEdit(self.send_message), focus_part = "footer")

        # Initialize commands
        self.commands = {}
        for command in commands:
            command = command(self, self.add_message)
            self.commands[command.name] = command

    def length(self, text: str) -> int:
        return int(len(text.encode(encoding = "utf_16_le")) / 2)

    def send_message(self, text: str) -> None:
        if text[0] == "/":
            try:
                splices = shlex.split(text.replace("\\", "\\\\"))
                if splices[0][1:] in self.commands:
                    response = self.commands[splices[0][1:]].on_execute(splices[1:])
                    if response is None:
                        return  # Internal command, do not send in chat lmao

                    text = response

            except ValueError:
                pass

        self.websocket.send({"type": "message", "data": {"message": text}})

    def construct_message(self, author: str, content: str, user_color: str = "gray") -> None:
        visible_author = author if author != self.last_author else " " * self.length(author)
        now, time_string = datetime.now(), ""
        if (author != self.last_author) or ((now - self.last_time).total_seconds() > 300):
            time_string = now.strftime("%I:%M %p" if config["client.time_format"] != "24h" else "%H:%M") + "  "  # Right padding for the scrollbar

        self.pile.contents.append((urwid.Columns([
            (self.length(visible_author), urwid.Text((user_color, visible_author))),
            (3, urwid.Text(("sep", " | "))),
            ("weight", 4, urwid.Text(content)),
            (len(time_string) + 2, urwid.Text(("time", time_string), align = "right"))  # +2 adds left padding
        ]), self.pile.options()))
        self.last_author, self.last_time = author, now

    def add_message(self, author: str, content: str, user_color: str = "gray") -> None:
        self.construct_message(author, emoji.emojize(content), user_color)

        # Scroll to the end (if we haven't manually moved)
        if len(self.pile.contents) > 50:
            self.pile.contents = self.pile.contents[1:]

        self.scroll.to_end()
        self.loop.screen.clear()
        self.loop.draw_screen()

    def on_message(self, data: dict) -> None:
        if not hasattr(self, "loop"):
            return  # We aren't even initialized yet

        match data:
            case {"type": "response", "data": {"callback": callback}}:
                callbackfn = self.websocket.callbacks[callback]
                del self.websocket.callbacks[callback]
                return callbackfn(data)

            case {"type": "message", "data": {"user": user, "message": message}}:
                color_code = f"user-{user['name']}"
                self.loop.screen.register_palette_entry(color_code, "yellow", "", foreground_high = f"#{user['hex']}")

                # Push message to screen
                self.add_message(user["name"], message, color_code)

            case _:
                exit(f"Nightwatch Exception\n{'=' * 50}\n\n{data['data']['message']}")

    def on_ready(self, loop: urwid.MainLoop, payload: dict) -> None:
        self.loop = loop
        self.construct_message("Nightwatch", f"You have connected to {payload['name']}.")
