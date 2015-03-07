#!/bin/sh
echo $(pwd)
python pack/pyinstaller/pyinstaller.py pack/srv_pkg.spec --clean -y


