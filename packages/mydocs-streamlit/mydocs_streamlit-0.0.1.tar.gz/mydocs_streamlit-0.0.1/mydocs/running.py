import os
import sys
from .index import index_start
import json

FILE_OBJECT = {
    "project_name":"Project Name",
    "structure":{
        "project": [
            {
                "name": "file.py",
                "display_name":"First Document"
            }
        ]
    }
}

def start_command():
    # Define the path to create the new file in a current project directory.
    file_path = os.path.join(os.getcwd(),"document.py")
    file_name = "document.py"
    if os.path.exists(file_name):
        print(f"'{file_name}' already exists.")
    else:
        # Create the new file and write initial content
        with open(file_path, 'w') as wb:
          wb.write(json.dumps(FILE_OBJECT))
          #wb.write(repr(FILE_OBJECT))

        print(f"Created '{file_name}' with default content.")

def run_doc():
    """Run the package index file"""
    file_path = os.path.join(os.getcwd(),"document.py")
    print("file path ", file_path)
    file_name = "document.py"
    if os.path.exists(file_path):
        file_path = "mydocs/index.py"
        print("dddd ")
        index_start()
        # os.system(f"python {file_path}")
    else:
        print(f"'{file_name}' does not exist. Please create it with 'mypackage start'.")


def execute():
    file_path = os.path.join(os.getcwd(),"document.py")
    file_name = "document.py"
    if os.path.exists(file_name):
        # os.path.dirname(__file__)
        # file_path = "mydocs/main.py"
        os.system(f"streamlit run {os.path.dirname(__file__)}/main.py")


def main():
    """Parse and execute commands."""
    if len(sys.argv) < 2:
        print("Usage: mypackage <start|run|execute>")
        sys.exit(1)
    
    command = sys.argv[1]
    if command == "start":
        start_command()
    elif command == "run":
        run_doc()
    elif command == "execute":
        execute()
    else:
        print(f"Unknown command: {command}")
        print("Usage: mypackage <start|run>")
