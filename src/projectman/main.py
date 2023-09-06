import argparse
import os
import sys

from projectman.prints import error, info, print, warn, exception, cstr
from projectman.const import CONFIG_PATH
from projectman.create_template import create_template_from_project, save_template
from projectman.create_project import create_project_from_template, TemplateParseError


def init_args():
    parser = argparse.ArgumentParser("projectman", epilog="Author Beshr Alghalil")
    parser.add_argument("-n", "--name", help="project name")
    parser.add_argument(
        "-t", "--template", required=False, help="template file path of template name"
    )

    parser.add_argument(
        "-o",
        "--out",
        help="where to create the project or template",
        default=os.getcwd(),
        required=False,
    )
    create_group = parser.add_argument_group("create template")
    create_group.add_argument(
        "-c",
        "--create-template",
        help="creates template from the current project structure in the current working directory if `--out` is not specified",
        action="store_true",
        required=False,
        default=False,
    )
    create_group.add_argument(
        "--read-hidden-files",
        action="store_true",
        default=False,
        required=False,
        help="read hidden files content",
    )
    create_group.add_argument(
        "--ignore",
        required=False,
        help="files and directories to be ignored when creating template, supports glob format",
        nargs="*",
    )
    create_group.add_argument(
        "--include-files-content",
        required=False,
        help="include files content in the template file",
        action="store_true",
        default=True,
    )

    info_group = parser.add_argument_group("info")
    info_group.add_argument(
        "--print-template-path",
        action="store_true",
        default=False,
        required=False,
        help="prints template storage path",
    )
    info_group.add_argument(
        "--list-templates",
        action="store_true",
        default=False,
        required=False,
        help="prints templates",
    )
    args = parser.parse_args()
    _parser_error_func = parser.error
    parser.error = lambda m: _parser_error_func(cstr(m, color="red", style="bold"))

    info("Templates:")
    if args.list_templates:
        for i in os.listdir(CONFIG_PATH):
            info("  - " + os.path.splitext(i)[0])
        exit(0)
    if args.print_template_path:
        info(CONFIG_PATH)
        exit(0)
    if args.template and not args.name:
        parser.error("The `--name` argument is required when `--template` is provided.")
    if args.name and not (args.template or args.create_template):
        parser.error(
            "one of `--template` or `--create-template` arguments is required when `--name` is provided."
        )
    if args.create_template and not args.name:
        parser.error(
            "The `--name` argument is required when `--create-template` is provided."
        )
    if args.read_hidden_files and not args.create_template:
        parser.error(
            "The `--read-hidden-files` argument is used only when `--template` is provided."
        )
    if args.ignore and not args.create_template:
        parser.error(
            "The `--ignore` argument is used only when `--template` is provided."
        )

    if not args._get_args() and not args._get_kwargs():
        parser.error("please provide the required arguments")

    return args


def main():
    args = init_args()
    try:
        if args.create_template:
            info(f"Creating template `{args.name}` from project")
            dest = os.getcwd()
            template = create_template_from_project(
                dest,
                read_hidden_files=args.read_hidden_files,
                ignore=args.ignore,
                include_files_content=args.include_files_content,
            )
            if "--out" in sys.argv:
                dest = args.out
            else:
                dest = CONFIG_PATH
            save_template(template, args.name, dest)
            print(
                f"Saved template `{args.name}` into `{dest}/{args.name}.yaml`",
                color="green",
            )
        elif args.template:
            info("Creating project from template")
            dest = args.out
            create_project_from_template(
                dest=dest, project_name=args.name, template=args.template
            )
    except TemplateParseError as e:
        error("TemplateParseError: ", e)
    except Exception as e:
        exception(e)

    return 0


if __name__ == "__main__":
    exit(main())
