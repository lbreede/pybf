# PyBf - A Python Interpreter for Brainfuck

PyBf is a Python interpreter for the esoteric programming language Brainfuck. Brainfuck is a minimalistic language with only eight commands that manipulate an array of memory cells. The simplicity of the language and the difficulty of programming in it have made it a popular language for programming puzzles and challenges.

PyBf is a lightweight and easy-to-use interpreter for Brainfuck programs. It supports running programs from strings or files, as well as partial programs and resetting the interpreter. PyBf is also tested with a suite of unit tests to ensure its reliability.

## Installation

PyBf can be installed using pip:

```bash
pip install pybf
```

## Usage

Using PyBf is simple. First, create an instance of the `Brainfuck` class:

```python
from pybf import Brainfuck
bf = Brainfuck()
```

Next, load a Brainfuck program either from a file or a string:

```python
bf.load("hello_world.bf")
```

Or:

```python
bf.program = ">+++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<++.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-]<+."
```

Finally, run the program:

```python
output = bf.run()
```

The output of the program will be returned by the `run()` method, and can also be accessed through the `output` attribute of the `Brainfuck` instance.

## Contributing

Contributions to PyBf are welcome! To contribute, please fork the repository and submit a pull request with your changes. Please ensure that your code is well-documented and passes the existing unit tests.

## License

PyBf is licensed under the MIT License. See the LICENSE file for details.