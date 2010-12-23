#!/bin/bash

set -e

WDIR=$PWD
cd build/html
mv _sources sources
mv _static static
grep -r _static * | cut -f 1 -d : | xargs sed -i "bk" "s/_static/static/g"
grep -r _sources * | cut -f 1 -d : | xargs sed -i "bk" "s/_sources/sources/g"
rm *bk */*bk
cd $WDIR
