#!/bin/sh
echo $(pwd)
python pack/pyinstaller/pyinstaller.py pack/cli_pkg.spec --clean -y


