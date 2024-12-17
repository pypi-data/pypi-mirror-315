# Tree2File

A command-line tool to create directory structures from tree command output.

## Installation

```bash
pip install tofile
```

## Usage

1. Run the command:
```bash
tofile
```

2. Paste your tree structure. For example:
```bash
my_project/
├── src/
│   └── main.py
├── tests/
│   └── test_main.py
└── README.md
```

3. Press Enter twice to finish input.

The tool will create the directory structure in your current working directory.


## Features

- Creates directories and files from tree command output
- Validates input structure before creation
- Handles nested directories and files
- Simple command-line interface
- Two convenient commands: t2f or tree2file

## License
MIT License