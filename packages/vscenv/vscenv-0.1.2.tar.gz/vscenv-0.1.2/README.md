# vscenv - Management of isolated vscode environments

vscenv is a command-line script that makes it easy to maintain and manage isolated vscode environments written in Python.

This script allows users to manage isolated vscode environments, enabling the creation, deletion, and execution of separate environments with their own user data and extensions.

---

## Installation
- Option 1 : Install from pypi
    ```
    pip install vscenv
    ```
- Option 2 : Install from soruce
    ```
    git clone https://github.com/jugangdae/vscenv
    cd vscenv
    pyhton -m build
    pip install dist/vscenv-0.0.1-py3-none-any.whl
    ```
> For global installations, the `--break-system-package` option is required.

---
## Commands

1. `create` : Create a new vscenv environment.
    ```
    vscenv create [vscenv_env]
    vscenv c [vscenv_env]
    ```
2. `list` : Show list of vscenv environments. 
    ```
    vscenv list
    vscenv l
    ```
3. `run` : Run vscode using the vscenv environment
    ```
    vscenv run [vscenv_env] [work_path]
    vscenv r [vscenv_env] [work_path]
    ```
4. `Delete` : Delete the vscenv environment.
    ```
    vscenv delete [vscenv_env]
    vscenv d [vscenv_env]
    ```
5. `help` and `version`
    ```
    vscenv [-h | --help]
    vscenv [-v | --version]
    ```
---
## Config (~/.vscenvconf)
```
[setting]
vscenv_cmd = ["code" or "code-insider"]
vscenv_dir = [path of vscenv environments directory]
```
