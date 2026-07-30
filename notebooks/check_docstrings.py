import os
import ast


SRC_FOLDER = "src"

missing = []


for root, dirs, files in os.walk(SRC_FOLDER):

    for file in files:

        if file.endswith(".py"):

            path = os.path.join(root, file)

            with open(path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read())


            for node in ast.walk(tree):

                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                    # Ignore private functions
                    if node.name.startswith("_"):
                        continue


                    if ast.get_docstring(node) is None:

                        missing.append(
                            {
                                "file": path,
                                "function": node.name
                            }
                        )


print("=" * 50)
print("Missing Docstrings:", len(missing))
print("=" * 50)


for item in missing:

    print(
        item["file"],
        "->",
        item["function"]
    )