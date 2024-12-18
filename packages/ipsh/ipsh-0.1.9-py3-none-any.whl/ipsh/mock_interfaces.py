# -*- coding: utf-8 -*-

"""mock_interfaces module: mock objects for testing"""

from collections import deque
from typing import Any

from . import const

BEL_NUM = 7
BS_NUM = 8
LF_NUM = 10
CR_NUM = 13


class Screen:
    """Observable screen mock"""

    def __init__(self) -> None:
        """initialize an internal line buffer"""
        self.__lines: list[list[str]] = [[]]
        self.__cursor_pos: int = 0
        self.__buffer: deque[int] = deque()
        self.__alerts: int = 0

    @property
    def current_line(self) -> list[str]:
        """Return the current line"""
        return self.__lines[-1]

    @property
    def lines(self) -> list[str]:
        """Return a list of strings generated from self.__lines"""
        return [const.EMPTY.join(line) for line in self.__lines]

    @property
    def cursor_pos(self) -> int:
        """Return the cursor position"""
        return self.__cursor_pos

    @property
    def alerts(self) -> int:
        """Return the number of alerts"""
        return self.__alerts

    def clear(self) -> None:
        """reset all data"""
        self.__lines.clear()
        self.__lines.append([])
        self.__buffer.clear()
        self.__cursor_pos = 0
        self.__alerts = 0

    def echo(self, *data: str) -> None:
        """mock buffers.echo()"""
        self.print(*data, sep=const.EMPTY, end=const.EMPTY, flush=True)

    def print(
        self,
        *objects: Any,
        sep: str = const.BLANK,
        end: str = const.LF,
        flush: bool = False,
    ) -> None:
        """mock the print() function"""
        printables: list[str] = []
        for item in objects:
            if isinstance(item, bytes):
                printables.append(item.decode())
            else:
                printables.append(str(item))
            #
        #
        data = sep.join(printables) + end
        self.add_to_buffer(data, flush=flush)

    def add_to_buffer(self, data: str, flush: bool = False) -> None:
        """add data to buffer, char by char.
        Flush at every LF or at the end if flush is True
        """
        num_data = [ord(char) for char in data]
        output_data: list[int] = []
        if flush:
            output_data.extend(list(self.__buffer))
            self.__buffer.clear()
            output_data.extend(num_data)
        else:
            self.__buffer.extend(num_data)
            while True:
                try:
                    next_lf = self.__buffer.index(LF_NUM)
                except ValueError:
                    break
                #
                for _ in range(next_lf + 1):
                    output_data.append(self.__buffer.popleft())
                #
            #
        #
        self.output(output_data)

    def output(self, char_data: list[int]) -> None:
        """Append output to the current line, etc"""
        for codepoint in char_data:
            if codepoint == LF_NUM:
                self.__lines.append([])
                self.__cursor_pos = 0
            elif codepoint == BS_NUM and self.__cursor_pos > 0:
                self.__cursor_pos -= 1
            elif codepoint == CR_NUM:
                self.__cursor_pos = 0
            elif codepoint == BEL_NUM:
                self.__alerts += 1
            else:
                char = chr(codepoint)
                if not char.isprintable():
                    continue
                #
                if len(self.current_line) > self.__cursor_pos:
                    self.current_line[self.__cursor_pos] = char
                else:
                    self.current_line.append(char)
                #
                self.__cursor_pos += 1
            #
        #
