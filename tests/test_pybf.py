import os
import unittest

from pybf import Brainfuck


class TestPyBf(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bf = Brainfuck()
        cls.bf_files = os.path.join(os.path.dirname(__file__), "..", "bf_files")

    def tearDown(self) -> None:
        self.bf.reset()

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
