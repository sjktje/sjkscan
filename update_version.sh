#!/bin/sh

git flow release start v$1
sed -e "s/__version__ = '.*'/__version__ = '$1'/g" -i sjkscan/__init__.py
echo "Now run tests etc, and then:"
echo "git flow release finish v$1"
