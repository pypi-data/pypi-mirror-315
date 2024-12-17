# Tree Maker

A simple Python package that creates a directory and file structure from a given JSON or Python object.

## Installation 

You can install the package using pip:

```bash
pip install easy-tree-maker
```

## Usage

You can use the `TreeMaker` class to create directories and files based on a JSON or Python structure.

### Example with Python object:
```python
from easy_tree_maker.core import TreeMaker

tree_structure = [
    {
        "type": "directory",
        "name": "TestProject",
        "contents": [
            {"type": "file", "name": "README.md"},
            {"type": "directory", "name": "src", "contents": [
                {"type": "file", "name": "app.py"}
            ]}
        ]
    }
]

tree_maker = TreeMaker(tree_structure, is_json=False)
tree_maker.create_tree(root_path="./TestDirectory")
```

### Example with JSON string:
```python
import json
from tree_maker.core import TreeMaker

tree_structure_json = json.dumps([
    {
        "type": "directory",
        "name": "TestProject",
        "contents": [
            {"type": "file", "name": "README.md"},
            {"type": "directory", "name": "src", "contents": [
                {"type": "file", "name": "app.py"}
            ]}
        ]
    }
])

tree_maker = TreeMaker(tree_structure_json, is_json=True)
tree_maker.create_tree(root_path="./TestDirectory")
```
