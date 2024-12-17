import ast
# from document import FILE_OBJECT
import os
import json


def index_start():
    functions = {}
    # current_path = os.path.join(os.getcwd(),"document.py")
    current_path = os.getcwd()

    FILE_OBJECT = {}
    with open(os.path.join(current_path,"document.py"),"r") as read_current_file:
        value = read_current_file.read()
        print("value is ", value)
        # print(read_current_file.read())
        # print(type(read_current_file.read()))
        # breakpoint()
        FILE_OBJECT = json.loads(value)

    print(FILE_OBJECT)


    for record in FILE_OBJECT["structure"]:
        for files in FILE_OBJECT["structure"][record]:
            file_name = f"{record}/{files["name"]}"
            with open(f"{current_path}/{file_name}", "r") as file:
                source_code = file.read()
                tree = ast.parse(source_code)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):  # Check if it's a function
                    function_name = node.name
                    docstring = ast.get_docstring(node)  # Extract the docstring

                    if files["name"] not in functions:
                        functions[files["name"]] = {
                            "code": repr(source_code),
                            "display_name": files["display_name"],
                            "result": []
                        }

                    functions[files["name"]]["result"].append(
                        {
                            "file_path":file_name,
                            "function_name": function_name, 
                            "doc_string": docstring
                        }
                    )

        print("The index ends here....")
    print("kkjdjkd ", os.path.dirname(__file__))
    with open(f"{os.path.dirname(__file__)}/functions_value.py", "w") as wb:
        wb.write("project_dict = " + repr(functions) + "\n")

if __name__ == "__main__":
    index_start()