import os
import shutil
import pytest
from easy_tree_maker.core import TreeMaker

@pytest.fixture
def sample_structure():
    """
    Sample structure to define the tree hierarchy for testing.
    """
    return [
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

@pytest.fixture
def temp_directory():
    """
    Create a temporary directory for testing, and clean it up afterward.
    """
    temp_dir = "temp_test_dir"
    os.makedirs(temp_dir, exist_ok=True)
    yield temp_dir  # Provide the temporary directory path to the test
    shutil.rmtree(temp_dir)  # Cleanup after the test

def test_create_tree(sample_structure, temp_directory):
    """
    Test the creation of a file and directory tree.
    """
    # Initialize TreeMaker with the sample structure
    tree_maker = TreeMaker(sample_structure)
    tree_maker.create_tree(root_path=temp_directory)

    # Validate the structure creation
    project_path = os.path.join(temp_directory, "TestProject")
    src_path = os.path.join(project_path, "src")
    app_path = os.path.join(src_path, "app.py")

    assert os.path.exists(project_path), "Root directory 'TestProject' was not created."
    assert os.path.exists(os.path.join(project_path, "README.md")), "File 'README.md' was not created."
    assert os.path.exists(app_path), "File 'app.py' was not created inside 'src' directory."
