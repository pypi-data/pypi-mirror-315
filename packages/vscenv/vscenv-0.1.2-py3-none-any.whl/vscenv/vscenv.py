#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Created By  : Gangdae Ju
# Created Date: Aug 10, 2021
# =============================================================================
import os
import shutil
import argparse
import configparser
import subprocess

version = '0.1.2'

vscenv_cmd = 'code' # 'code' or 'code-insider'
vscenv_dir_path = os.path.join(os.path.expanduser('~'), '.vscenv')
vscenv_conf_path = os.path.join(os.path.expanduser('~'), '.vscenvconf')

def _list(args):
    for i in os.listdir(vscenv_dir_path):
        if not i.startswith('.'):
            print(i)
    return 0

def _create(args):
    codeDir = os.path.join(vscenv_dir_path, args.env)
    userdataDir = os.path.join(codeDir, 'userdata')
    extensionsDir = os.path.join(codeDir, 'extensions')
    
    if os.path.exists(codeDir):
        print(f'ERROR: {args.env} already exists.')
        return -1

    try:
        os.makedirs(userdataDir)
        os.makedirs(extensionsDir)
        print('DONE: Successfully created.')
    except OSError as e:
        print(f'ERROR: Creation failed - {e}')
        return -1
    
    return 0
    
def _delete(args):
    codeDir = os.path.join(vscenv_dir_path, args.env)

    if not os.path.exists(codeDir):
        print(f'ERROR: {args.env} not found.')
        return -1

    try:
        shutil.rmtree(codeDir)
        print('DONE: Successfully deleted.')
    except OSError as e:
        print(f'ERROR: Deletion failed - {e}')
        return -1
    
    return 0

def _run(args):
    codeDir = os.path.join(vscenv_dir_path, args.env)
    userdataDir = os.path.join(codeDir, 'userdata')
    extensionsDir = os.path.join(codeDir, 'extensions')
    
    cmd = [vscenv_cmd]

    if not os.path.exists(codeDir):
        print(f'ERROR: {args.env} not found.')
        return -1

    if os.path.exists(userdataDir):
        cmd.extend(['--user-data-dir', userdataDir])

    if os.path.exists(extensionsDir):
        cmd.extend(['--extensions-dir', extensionsDir])    
    
    cmd.append(args.path)

    try:
        subprocess.run(cmd)
    except subprocess.CalledProcessError as e:
        print(f'ERROR: Failed to run {args.env} - {e}')
        return -1

    return 0

def main():
    global vscenv_cmd, vscenv_dir_path

    if not os.path.exists(vscenv_conf_path):
        config_parser = configparser.ConfigParser()
        config_parser.add_section("setting")
        config_parser.set("setting", "vscenv_cmd", vscenv_cmd)
        config_parser.set("setting", "vscenv_dir", vscenv_dir_path)
        with open(vscenv_conf_path, "w") as fp:
            config_parser.write(fp)
    else:
        config_parser = configparser.ConfigParser()
        config_parser.read(vscenv_conf_path)
        vscenv_cmd = config_parser['setting']['vscenv_run']
        vscenv_dir_path = config_parser['setting']['vscenv_dir']
  
    if not os.path.exists(vscenv_dir_path):
        os.makedirs(vscenv_dir_path)
    
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-v', '--version', action='version', version=f'vscenv v{version}')

    subparsers = arg_parser.add_subparsers()
    cmd_list = subparsers.add_parser('list', aliases=['l'], help='Show list of vscenv environments.')
    cmd_list.set_defaults(func=_list)
    cmd_create = subparsers.add_parser('create', aliases=['c'], help='Create a new vscenv environment.')
    cmd_create.add_argument('env', help='Name of the environment to create')
    cmd_create.set_defaults(func=_create)
    cmd_delete = subparsers.add_parser('delete', aliases=['d'], help='Delete a vscenv environment.')
    cmd_delete.add_argument('env', help='Name of the environment to delete')
    cmd_delete.set_defaults(func=_delete)
    cmd_run = subparsers.add_parser('run', aliases=['r'], help='Run vscode using a vscenv environment.')
    cmd_run.add_argument('env', help='Name of the environment to run')
    cmd_run.add_argument('path', help='Path to the file to open')
    cmd_run.set_defaults(func=_run)
    
    args = arg_parser.parse_args()

    try:
        args.func(args)
    except AttributeError:
        arg_parser.parse_args(['-h'])

if __name__ == '__main__':
    main()
