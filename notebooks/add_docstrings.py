import os
import ast


SRC_FOLDER = "src"


def add_docstring_to_function(source, node):

    lines = source.splitlines()

    insert_line = node.body[0].lineno - 1

    indent = " " * (node.col_offset + 4)

    lines.insert(
        insert_line,
        f'{indent}"""Function: {node.name}"""'
    )

    return "\n".join(lines)


def process_file(path):

    with open(path, "r", encoding="utf-8") as f:
        source = f.read()


    tree = ast.parse(source)

    functions = []


    for node in ast.walk(tree):

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

            if node.name.startswith("_"):
                continue

            if ast.get_docstring(node) is None:
                functions.append(node)


    # Insert from bottom to top
    for node in sorted(
        functions,
        key=lambda x: x.lineno,
        reverse=True
    ):

        source = add_docstring_to_function(
            source,
            node
        )


    if functions:

        with open(path, "w", encoding="utf-8") as f:
            f.write(source)


        print(
            "Updated:",
            path,
            "| Functions:",
            len(functions)
        )



for root, dirs, files in os.walk(SRC_FOLDER):

    for file in files:

        if file.endswith(".py"):

            process_file(
                os.path.join(root,file)
            )


print("Done")