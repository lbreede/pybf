import os
import unittest

from pybf import Brainfuck

HELLO_WORLD = (
    ">++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<++."
    "------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-]<+."
)
HELLO = "++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>++.>+.+++++++..+++."
WORLD = (
    "++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>++++++++++++++.------------.>>--------"
    "-----.++++++++++++++++++++++++.+++.------.--------.<<+."
)


class TestPyBf(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bf = Brainfuck()
        cls.bf_files = os.path.join(os.path.dirname(__file__), "..", "bf_files")

    def test_files(self) -> None:
        """Test running a program from a file"""
        path = os.path.join(self.bf_files, "hello_world.bf")
        self.bf.load(path)
        output = self.bf.run()
        self.assertEqual(output, "Hello World!\n")
        self.assertEqual(self.bf.output, "Hello World!\n")

    def test_program(self) -> None:
        """Test running a program from a string"""
        self.bf.program = HELLO_WORLD
        output = self.bf.run()
        self.assertEqual(output, "Hello, World!")
        self.assertEqual(self.bf.output, "Hello, World!")

    def test_two_programs(self) -> None:
        """Test running two programs, adding to the same output"""
        self.bf.program = HELLO
        output = self.bf.run()
        self.assertEqual(output, "Hello")
        self.assertEqual(self.bf.output, "Hello")

        # Resets everything except the output to add to it
        self.bf.reset()

        self.bf.program = WORLD
        output = self.bf.run()
        self.assertEqual(output, "Hello, World!")
        self.assertEqual(self.bf.output, "Hello, World!")

    def test_partial_program(self) -> None:
        """Test running a partial program and then running the rest of the program"""
        program = HELLO_WORLD
        program_half_length = len(program) // 2
        program_a = program[:program_half_length]
        program_b = program[program_half_length:]
        self.bf.program = program_a
        self.bf.run()
        self.bf.program = program_b
        self.bf.instruction_pointer = 0
        output = self.bf.run()
        self.assertEqual(output, "Hello, World!")
        self.assertEqual(self.bf.output, "Hello, World!")

    def test_reset(self) -> None:
        """Test reset method with and without including output"""
        self.bf.program = HELLO_WORLD
        self.bf.run()
        self.bf.reset()

        self.assertEqual(self.bf.data_pointer, 0)
        self.assertEqual(self.bf.instruction_pointer, 0)
        self.assertNotEqual(self.bf.output, "")

        self.bf.reset(include_output=True)

        self.assertEqual(self.bf.output, "")

    def test_file_not_found(self) -> None:
        """Test loading a file that doesn't exist"""
        with self.assertRaises(FileNotFoundError):
            self.bf.load("does_not_exist.bf")

    def tearDown(self) -> None:
        """Resets the interpreter completely"""
        self.bf.reset(include_output=True)
