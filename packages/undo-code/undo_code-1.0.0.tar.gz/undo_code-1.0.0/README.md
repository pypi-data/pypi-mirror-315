# undo-code

[![PyPI version](https://badge.fury.io/py/undo-code.svg)](https://badge.fury.io/py/undo-code)

`undo-code` is a Python package that allows developers to easily integrate undo/redo functionality into their projects. This package simplifies the process of managing changes and restoring previous states in applications, making it especially useful for text editors, graphic design tools, and other software requiring history tracking.

## Features

- **Simple API**: Easy-to-use methods for adding, undoing, and redoing actions.
- **Flexible Integration**: Works seamlessly with various data structures and custom objects.
- **Lightweight**: Minimal dependencies and efficient performance.

## Installation

Install `undo-code` using pip:

```bash
pip install undo-code
```

## Usage

Here's a basic example to get started:

```python
from undo_code import UndoManager

# Create an UndoManager instance
undo_manager = UndoManager()

# Define actions
def add_action():
    print("Action added!")

def remove_action():
    print("Action undone!")

# Add an action to the undo stack
undo_manager.add_action(add_action, remove_action)

# Undo the last action
undo_manager.undo()

# Redo the undone action
undo_manager.redo()
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or feedback, feel free to reach out to [Your Email or GitHub Profile].
