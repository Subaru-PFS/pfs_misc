#! /bin/sh

git filter-branch --prune-empty --tree-filter '
git lfs track "*.fits"
git lfs track "*.pck"
git lfs track "*.imgstk"
git lfs track "*.dat"
git lfs track "*.gz"
git add .gitattributes .gitconfig

for file in $(git ls-files | xargs git check-attr filter | grep "filter: lfs" | sed -r "s/(.*): filter: lfs/\1/"); do
  echo "Processing ${file}"

  git rm -f --cached ${file}
  echo "Adding $file lfs style"
  git add ${file}
done' --tag-name-filter cat -- --all

