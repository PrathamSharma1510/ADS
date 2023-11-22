
# set the python interpreter
PYTHON = python3

# set the default input file
DEFAULT_INPUT_FILE = input.txt

# compile the source code
run:
	$(PYTHON) main.py $(input_file)

# remove the output file
clean:
	rm output_file.txt