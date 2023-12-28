import ast
import os
from back.dljason import last_updated, patch_num, dl_champ_json

current_directory = os.path.dirname(os.path.abspath(__file__))


# Function to trigger the download of jsons if the patch changed
def new_patch_new_json():
    if last_updated != patch_num:
        with open(os.path.join(current_directory, 'dljason.py'), 'r') as file:
            data = file.read()
            tree = ast.parse(data)
            # Find and replace the value of last_updated
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == 'last_updated':
                            node.value = ast.NameConstant(value=patch_num)
            updated_code = ast.unparse(tree)
            file.close()
        with open(os.path.join(current_directory, 'dljason.py'), 'w') as file:
            file.write(updated_code)
            file.close()
        dl_champ_json()
    else:
        print("No new patch, no new jasons")
    pass
