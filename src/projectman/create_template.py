import fnmatch
import json
import os

import yaml

from projectman.prints import error


def create_template_from_project(
    path: str | os.PathLike,
    read_hidden_files=False,
    include_files_content=True,
    ignore=(),
) -> dict:
    project = {"name": os.path.basename(path), "type": "directory", "children": []}
    for ent in os.scandir(path):
        if ignore and any(fnmatch.fnmatch(ent.name, pattern) for pattern in ignore):
            continue
        if ent.is_dir():
            if ent.name.startswith("."):
                continue
            print(ent.path)
            project["children"].append(create_template_from_project(ent.path))
        elif ent.is_file():
            if not read_hidden_files and ent.name.startswith("."):
                continue
            file = {"name": ent.name, "type": "file"}
            with open(ent.path, "r", encoding="utf8") as f:
                try:
                    content = f.read()
                except Exception as e:
                    error(ent.path, "faild\n\t", str(e))
                    continue

                print(ent.path)
                if content:
                    file["content"] = content
                    if not include_files_content:
                        continue
            project["children"].append(file)

    if len(project["children"]) == 0:
        project.pop("children")

    return project


def save_template(template: dict, name: str, dest: str | os.PathLike, type_="yaml"):
    if not os.path.splitext(name)[1]:
        name += f".{type_}"
    dest = os.path.join(dest, name)
    with open(dest, "w") as f:
        if type_ == "yaml":
            yaml.safe_dump(template, f, default_flow_style=False)
        elif type_ == "json":
            json.dump(template, f, indent=2)
