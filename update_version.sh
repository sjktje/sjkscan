#!/bin/sh

git flow release start v$1
sed -i -e "s/__version__ = '.*'/__version__ = '$1'/g" sjkscan/__init__.py
git flow release finish v$1
