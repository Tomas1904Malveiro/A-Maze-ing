NAME = a_maze_ing.py
SRCS = a_maze_ing.py, display.py, output_writer.py, mazegen/__init__.py, mazegen/generator.py


install:
	python3 -m pip install flake8 mypy

all:
	run $(NAME)

debug:
	python3 -m pdb $(NAME)

clean:
	rm -f __pycache__
	rm -f  .mypy_cache