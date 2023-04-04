import unittest

from pybf import Brainfuck


class TestPyBf(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bf = Brainfuck()

    # def test_files(self) ->None:
    #     pass

    def test_program(self) -> None:
        self.bf.program = "++++++++++."
        self.bf.run()
        print(self.output)

    def tearDown(self) -> None:
        self.bf.reset()
