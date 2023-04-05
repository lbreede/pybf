import logging
import os
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


FileDescriptorOrPath = str | Path


class Brainfuck:
    MAX_ARRAY_LENGTH = 300000
    MAX_VALUE = 256

    def __init__(self):
        self.data_pointer: int = 0
        self.instruction_pointer: int = 0
        self._array: list[int] = [0]
        self.program: str = ""
        self.output: str = ""
        self._input_buffer: list[int] = []
        self._loop_starts: list[int] = []
        self._operations = {
            ">": self._increment_data_pointer,
            "<": self._decrement_data_pointer,
            "+": self._increment_value_at_pointer,
            "-": self._decrement_value_at_pointer,
            ".": self._output_value,
            ",": self._input_value,
            "[": self._start_loop,
            "]": self._end_loop,
        }

    def load(self, file: FileDescriptorOrPath) -> str:
        if os.path.exists(file):
            with open(file, encoding="utf-8") as fp:
                self.program = fp.read()
                return self.program
        raise FileNotFoundError(f"File {file} not found.")

    def reset(self, include_output: bool = False) -> None:
        """Resets all values and optionally also the output"""
        self.data_pointer = 0
        self.instruction_pointer = 0
        self._array = [0]
        self._loop_starts = []
        self._input_buffer = []
        if include_output:
            self.output = ""

    def run(self) -> str:
        """Run the program and return the output."""
        while self.instruction_pointer < len(self.program):
            char = self.program[self.instruction_pointer]

            if char in self._operations:
                self._operations[char]()
            else:
                pass

            self.instruction_pointer += 1
        return self.output

    def _increment_data_pointer(self) -> None:
        """Increment the data pointer (to point to the next cell to the right)."""
        logger.debug(
            "Incrementing data pointer from %s to %s",
            self.data_pointer,
            self.data_pointer + 1,
        )
        self.data_pointer = min(self.data_pointer + 1, self.MAX_ARRAY_LENGTH - 1)
        if self.data_pointer == len(self._array):
            self._array.append(0)

    def _decrement_data_pointer(self) -> None:
        """Decrement the data pointer (to point to the next cell to the left)."""
        logger.debug(
            "Decrementing data pointer from %s to %s",
            self.data_pointer,
            self.data_pointer - 1,
        )
        self.data_pointer = max(self.data_pointer - 1, 0)

    def _increment_value_at_pointer(self) -> None:
        """Increment (increase by one) the byte at the data pointer."""
        logger.debug("Incrementing value at pointer %s", self.data_pointer)
        self._array[self.data_pointer] = min(
            self._array[self.data_pointer] + 1, self.MAX_VALUE - 1
        )

    def _decrement_value_at_pointer(self) -> None:
        """Decrement (decrease by one) the byte at the data pointer."""
        logger.debug("Decrementing value at pointer %s", self.data_pointer)
        self._array[self.data_pointer] = max(self._array[self.data_pointer] - 1, 0)

    def _output_value(self) -> None:
        """Output the value at the data pointer."""
        char = chr(self._array[self.data_pointer])
        logger.debug("Outputting value at pointer %s: %s", self.data_pointer, char)
        self.output += char

    def _input_value(self) -> None:
        """Accept one byte of input, storing its value in the byte at the data pointer."""
        if not self._input_buffer:
            input_str = input()
            self._input_buffer = [ord(c) for c in input_str]
        self._array[self.data_pointer] = self._input_buffer.pop(0)

    def _start_loop(self) -> None:
        """If the start of a loop is reached, append its position to the loop_starts
        list.
        """
        self._loop_starts.append(self.instruction_pointer)

    def _end_loop(self) -> None:
        """Once the end of a loop is reached, check if the value at the data pointer is
        0.
        If it is, pop the last loop start from the loop_starts list and continue with
        the next instruction.
        Else, set the instruction pointer to the last loop start.
        """
        if self._array[self.data_pointer] == 0:
            self._loop_starts.pop()
        else:
            self.instruction_pointer = self._loop_starts[-1]
