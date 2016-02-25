#!/bin/sh

git flow release start v$1
sed -i "s/__version__ = '.*'/__version__ = '$1'/g" sjkscan/__init__.py
echo "Now run tests etc, and then:"
echo "git flow release finish v$1"
