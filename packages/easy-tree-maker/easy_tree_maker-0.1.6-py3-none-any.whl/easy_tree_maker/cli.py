import argparse
import os
import json
from easy_tree_maker.core import TreeMaker

def main():
    parser = argparse.ArgumentParser(
        description="Recreate directory structures from JSON or tree-like data."
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to the JSON file containing the tree structure or a raw JSON string.",
    )
    parser.add_argument(
        "--root",
        type=str,
        default=".",
        help="Root directory where the tree should be created (default is current directory).",
    )
    args = parser.parse_args()

    # Check if input is a file path or raw JSON string
    if os.path.exists(args.input):
        with open(args.input, "r") as file:
            input_data = file.read()
    else:
        input_data = args.input

    # Create the tree
    try:
        maker = TreeMaker(input_data)
        maker.create_tree(root_path=args.root)
        print(f"Tree successfully created at: {os.path.abspath(args.root)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
