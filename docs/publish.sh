#!/bin/bash
set -e
# set -x
if [ -z "$1" ]
  then
    echo "No version supplied"
    exit 1
fi
if [ -z "$2" ]
  then
    commit_message="Update docs to version ${version}"
fi
version=${1}
commit_message=${2}
echo "Regenerate documentation for ${version}"
make clean
make dirhtml
echo "Check out gh-pages as a working tree"
git worktree add published gh-pages
echo "Clear out all old files"
rm -rf published/*
echo "Copy new files to published"
cp -r _build/dirhtml/* published/
# mkdir -p published/en/v/${version}
# cp -r _build/dirhtml/* published/en/v/${version}
cd published
echo "Add all files to published pages"
git add -A
git commit -m "${commit_message}"
git push
# git worktree prune
echo "Removing working tree"
git worktree remove published/
echo "Done!"
