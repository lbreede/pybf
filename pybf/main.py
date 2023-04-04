import logging
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


FileDescriptorOrPath = str | Path


class Brainfuck:
    MAX_ARRAY_LENGTH = 300000
    MAX_VALUE = 256

    def __init__(self):
        self._data_pointer: int = 0
        self._instruction_pointer: int = 0
        self._array: list[int] = [0]
        self.program: str = ""
        self.output: str = ""
        self._input_buffer: list[int] = []

    def load(self, file: FileDescriptorOrPath) -> str:
        with open(file, encoding="utf-8") as fp:
            self.program = fp.read()
            return self.program

    def reset(self) -> None:
        self._data_pointer = 0
        self._instruction_pointer = 0
        self._array = [0]
        self.output = ""

    def run(self) -> str:
        start: list[int] = []

        while self._instruction_pointer < len(self.program):
            char = self.program[self._instruction_pointer]

            match char:
                case ">":
                    self._increment_data_pointer()
                case "<":
                    self._decrement_data_pointer()
                case "+":
                    self._increment_value()
                case "-":
                    self._decrement_value()
                case ".":
                    self._output_value()
                case ",":
                    if not self._input_buffer:
                        input_str = input()
                        self._input_buffer = [ord(c) for c in input_str]
                    self._array[self._data_pointer] = self._input_buffer.pop(0)
                case "[":
                    start.append(self._instruction_pointer)
                case "]":
                    if self._array[self._data_pointer] == 0:
                        start.pop()
                    else:
                        self._instruction_pointer = start[-1]
                case _:
                    pass

            self._instruction_pointer += 1
        return self.output

    def _increment_data_pointer(self) -> None:
        """Increment the data pointer (to point to the next cell to the right)."""
        self._data_pointer = min(self._data_pointer + 1, self.MAX_ARRAY_LENGTH - 1)
        if self._data_pointer == len(self._array):
            self._array.append(0)

    def _decrement_data_pointer(self) -> None:
        """Decrement the data pointer (to point to the next cell to the left)."""
        self._data_pointer = max(self._data_pointer - 1, 0)

    def _increment_value(self) -> None:
        """Increment the value at the data pointer."""
        self._array[self._data_pointer] = min(
            self._array[self._data_pointer] + 1, self.MAX_VALUE - 1
        )

    def _decrement_value(self) -> None:
        """Decrement the value at the data pointer."""
        self._array[self._data_pointer] = max(self._array[self._data_pointer] - 1, 0)

    def _output_value(self) -> None:
        """Output the value at the data pointer."""
        self.output += chr(self._array[self._data_pointer])


def main() -> None:
    import os

    bf = Brainfuck()
    path = os.path.join(os.path.dirname(__file__), "..", "bf_files", "hello_world.bf")
    bf.load(path)

    bf.run()
    print(bf.output)


if __name__ == "__main__":
    main()
