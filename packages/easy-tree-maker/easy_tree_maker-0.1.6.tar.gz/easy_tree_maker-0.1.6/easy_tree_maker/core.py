import os
import json

class TreeMaker:
    def __init__(self, input_data, is_json=True):
        """
        Initialize the TreeMaker.
        :param input_data: JSON structure or a Python object (list or dict).
        :param is_json: Whether the input data is in JSON format (default is True).
        """
        self.input_data = input_data
        self.is_json = is_json

    def parse_input(self):
        """
        Parse the input data.
        """
        if self.is_json:
            return json.loads(self.input_data)
        return self.input_data

    def create_tree(self, root_path="."):
        """
        Create the directory and file structure.
        :param root_path: The base path for creating the tree.
        """
        tree_data = self.parse_input()
        self._create_from_structure(tree_data, root_path)

    def _create_from_structure(self, structure, current_path):
        """
        Recursively create directories and files.
        :param structure: Parsed structure data.
        :param current_path: Current directory path.
        """
        if not os.path.exists(current_path):
            os.makedirs(current_path)

        for item in structure:
            item_type = item["type"]
            item_name = item["name"]
            item_path = os.path.join(current_path, item_name)

            if item_type == "directory":
                os.makedirs(item_path, exist_ok=True)
                # Recursively handle directory contents
                if "contents" in item:
                    self._create_from_structure(item["contents"], item_path)
            elif item_type == "file":
                # Create an empty file if it doesn't exist
                if not os.path.exists(item_path):
                    open(item_path, "w").close()
