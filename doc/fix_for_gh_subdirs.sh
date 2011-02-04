#!/bin/bash

set -e

WDIR=$PWD
cd build/html
mv _downloads downloads
mv _images images
mv _modules modules_gpf
mv _sources sources
mv _static static
grep -r _downloads * | cut -f 1 -d : | xargs sed -i "bk" "s/_downloads/downloads/g"
grep -r _images * | cut -f 1 -d : | xargs sed -i "bk" "s/_images/images/g"
grep -r _modules * | cut -f 1 -d : | xargs sed -i "bk" "s/_modules/modules_gpf/g"
grep -r _sources * | cut -f 1 -d : | xargs sed -i "bk" "s/_sources/sources/g"
grep -r _static * | cut -f 1 -d : | xargs sed -i "bk" "s/_static/static/g"
rm *bk */*bk
cd $WDIR
