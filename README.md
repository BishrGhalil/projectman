# ProjectMan
create projects from templates

### install

#### Linux
```
git clone https://github.com/BishrGhalil/projectman
cd projectman
sudo make install
```

### usage
list templates
```
projectman --list-templates
```

create project from template
```
projectman -n my-project -t python
```
create template from project and ignore all `.yaml` files
```
projectman -n my-project -c --ignore *.yaml
```

### options
```
usage: projectman [-h] [-n NAME] [-t TEMPLATE] [-o OUT] [-c]
                  [--read-hidden-files] [--ignore [IGNORE ...]]
                  [--include-files-content] [--print-template-path]
                  [--list-templates]

options:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  project name
  -t TEMPLATE, --template TEMPLATE
                        template file path of template name
  -o OUT, --out OUT     where to create the project or template

create template:
  -c, --create-template
                        creates template from the current project structure in
                        the current working directory if `--out` is not
                        specified
  --read-hidden-files   read hidden files content
  --ignore [IGNORE ...]
                        files and directories to be ignored when creating template, supports glob format
  --include-files-content
                        include files content in the template file

info:
  --print-template-path
                        prints template storage path
  --list-templates      prints templates

Author Beshr Alghalil

```
