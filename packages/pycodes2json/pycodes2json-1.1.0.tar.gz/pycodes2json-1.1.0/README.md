
# py2json

`py2json` is a Python package that scans a directory and its subdirectories for `.py` files, excluding hidden directories (those starting with a `.`), and merges their contents into a single JSON file. It simplifies the process of aggregating Python code into a structured JSON format for further analysis or processing.

## Features

- Automatically scans a specified directory and its subdirectories for `.py` files, skipping hidden directories.
- Outputs the merged contents into a well-formatted JSON file.
- Handles exceptions for missing directories, permissions, and unexpected errors.

## Installation

Install the package using pip:

```bash
pip install py2json
```

## Usage

After installation, use the command-line interface (CLI) tool:

```bash
py2json <directory_path> <output_json_path>
```

### Parameters

- `<directory_path>`: Path to the directory containing `.py` files.
- `<output_json_path>`: Path to save the resulting JSON file.

### Example

Suppose you have a directory named `scripts` containing `.py` files and subdirectories. To merge them into a JSON file named `output.json`, run:

```bash
py2json scripts output.json
```

This will create a JSON file `output.json` with the contents of all `.py` files in the `scripts` directory and its subdirectories, excluding hidden directories.

## Exception Handling

The package gracefully handles the following errors:

- **FileNotFoundError**: If the specified directory does not exist.
- **PermissionError**: If the script lacks permissions to read files or write the output file.
- **Other Errors**: Any unexpected errors are logged for debugging.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests on the [GitHub repository](https://github.com/lechplace/py2json).

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
