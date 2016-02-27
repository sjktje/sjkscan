#!/bin/sh

git flow release start v$1
perl -pi -e "s/__version__ = '.*'/__version__ = '$1'/" sjkscan/__init__.py
echo "Now run tests etc, commit last changes, and then:"
echo "git flow release finish v$1"
