
import os
from typing import Callable

from rich.color import Color
from rich.console import Console, ConsoleOptions
from rich.segment import Segment
from rich.style import Style


class Computed:

    def __init__(self, state: list[bool], function: Callable[[dict[bool]], bool], rang: int):
        self.computer_buffer: list[bool] = [False] * self.Config.height*self.Config.width
        center_index=self.Config.width//2
        self.computer_buffer[center_index-len(state)//2:center_index+len(state)//2] = state
        def value_by_index(index: int, value: int, row: int) -> bool:
            if index + value >= self.Config.width or index+value < 0:
                return False
            return self.computer_buffer[(row-1)*self.Config.width+index+value]
        for i in range(1, self.Config.height):
            for j in range(self.Config.width):
                neighbors = dict()
                for k in range(rang*2+1):
                    neighbors[k - rang] = (value_by_index(j, k-rang, i))
                result = function(neighbors)
                self.computer_buffer[i * self.Config.width + j] = result
    class Config:
        width, height = os.get_terminal_size()

    def get_str(self):
        display_buffer = ''
        for i in range(0, self.Config.height):
            for j in range(self.Config.width):
                if self.computer_buffer[i * self.Config.width + j]:
                    display_buffer += '#'
                else: display_buffer += ' '

        return display_buffer
    
    def __rich_console__(self, console: Console, options: ConsoleOptions):
        color_active = Color.from_rgb(255, 255, 255)
        color_enactive = Color.from_rgb(0, 0, 0)
        def get_color(i):
            return color_active if i else color_enactive
        for i in range(1, self.Config.height, 2):
            for j in range(self.Config.width):
                index_1 = self.computer_buffer[i * self.Config.width + j]
                index_2 = self.computer_buffer[(i-1) * self.Config.width + j]
                yield Segment("▄", Style(color=get_color(index_1), bgcolor=get_color(index_2)))
            yield Segment.line()


