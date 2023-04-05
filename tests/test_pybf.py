import os
import unittest

from pybf import Brainfuck


class TestPyBf(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bf = Brainfuck()
        cls.bf_files = os.path.join(os.path.dirname(__file__), "..", "bf_files")

    def test_files(self) -> None:
        path = os.path.join(self.bf_files, "hello_world.bf")
        self.bf.load(path)
        output = self.bf.run()
        self.assertEqual(output, "Hello World!\n")
        self.assertEqual(self.bf.output, "Hello World!\n")

    def test_program(self) -> None:
        self.bf.program = ">++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<++.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-]<+."
        output = self.bf.run()
        self.assertEqual(output, "Hello, World!")
        self.assertEqual(self.bf.output, "Hello, World!")

    def test_two_programs(self) -> None:
        self.bf.program = (
            "++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>++.>+.+++++++..+++."
        )
        output = self.bf.run()
        self.assertEqual(output, "Hello")
        self.assertEqual(self.bf.output, "Hello")

        self.bf.reset()

        self.bf.program = "++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>++++++++++++++.------------.>>-------------.++++++++++++++++++++++++.+++.------.--------.<<+."
        output = self.bf.run()
        self.assertEqual(output, "Hello, World!")
        self.assertEqual(self.bf.output, "Hello, World!")

    def test_partial_program(self) -> None:
        program = ">++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<++.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-]<+."
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
        self.bf.program = ">++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<++.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-]<+."
        self.bf.run()
        self.bf.reset()

        self.assertEqual(self.bf.data_pointer, 0)
        self.assertEqual(self.bf.instruction_pointer, 0)
        self.assertNotEqual(self.bf.output, "")

        self.bf.reset(include_output=True)

        self.assertEqual(self.bf.output, "")

    def tearDown(self) -> None:
        self.bf.reset(include_output=True)
