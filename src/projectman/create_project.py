import os
import yaml
from projectman.const import CONFIG_PATH


class TemplateParseError(Exception):
    pass


def create_project_from_template(
    dest: str | os.PathLike, project_name: str, template: str | os.PathLike | dict
) -> None:
    if isinstance(template, (str, os.PathLike)):
        if not os.path.lexists(template):
            templates = os.listdir(CONFIG_PATH)
            if template + ".yaml" in templates:
                template = CONFIG_PATH / f"{template}.yaml"

        with open(template, "r") as f:
            try:
                template = yaml.safe_load(f)
            except yaml.parser.ParserError as e:
                raise TemplateParseError(str(e))

    def get_or_raise_parse_error(gettable, key, default=None, err_msg=""):
        value = gettable.get(key, default)
        if value is None:
            raise TemplateParseError(err_msg)
        else:
            return value

    def create_directory(directory, parent_path):
        directory_path = os.path.join(parent_path, directory["name"]).replace(
            "$project_name", project_name
        )
        os.makedirs(directory_path, exist_ok=True)
        create_children(directory.get("children", []), directory_path)

    def create_file(file, parent_path):
        file_path = os.path.join(parent_path, file["name"])
        if file.get("content"):
            with open(file_path, "w") as f:
                f.write(file["content"].strip().replace("$project_name", project_name))

    def create_children(children, parent_path):
        for child in children:
            name = get_or_raise_parse_error(
                child, "name", err_msg="child should have a `name` field"
            )
            _type = get_or_raise_parse_error(
                child, "type", err_msg=f"child `{name}` should have a `type` field"
            )
            if _type == "directory":
                create_directory(child, parent_path)
            elif _type == "file":
                create_file(child, parent_path)
            else:
                raise TemplateParseError(f"unkown child type for child `{name}`")

    dest = os.path.join(dest, project_name)
    os.makedirs(dest, exist_ok=True)
    create_directory(template, dest)
