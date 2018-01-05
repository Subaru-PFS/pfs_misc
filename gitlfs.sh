#! /bin/sh

git filter-branch --prune-empty --tree-filter '
  git lfs track "*.png"
  git lfs track "*.PNG"
  git lfs track "*.jpg"
  git lfs track "*.JPG"
  git lfs track "*.jpeg"
  git lfs track "*.JPEG"
  git lfs track "*.vsd"
  git lfs track "*.pdf"
  git lfs track "*.ods"
  git lfs track "*.doc"
  git lfs track "*.docx"
  git lfs track "*.eps"
  git lfs track "*.ppt"
  git lfs track "*.pptx"
  git lfs track "*.mpp"
  git add .gitattributes 

  for file in $(git ls-files | xargs -i git check-attr filter "{}" | grep "filter: lfs" | sed -r "s/^(.*): filter: lfs/\1/" | sed -e "s/ /\%/g"); do
    echo "OPT: ${file}"
    file=`echo ${file} | sed -e "s/\%/ /g"`
    echo "Processing ${file}"
    git rm -f --cached "${file}"
    echo "Adding $file lfs style"
    git add "${file}"
  done' --tag-name-filter cat -- --all


