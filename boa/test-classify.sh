#!/bin/sh

changed="0"

if [ ! -f dataset/py/3/7/379733022.json ] ; then
    mkdir -p dataset/py/3/7
    /bin/echo -n "[" > dataset/py/3/7/379733022.json
    wget -qO - "https://api.github.com/repos/psybers/py-classify-tests" >> dataset/py/3/7/379733022.json
    echo "]" >> dataset/py/3/7/379733022.json
fi

if [ ! -d repo/3/7/379733022/.git ] ; then
    mkdir -p repo/3/7
    git clone --bare https://github.com/psybers/py-classify-tests.git repo/3/7/379733022
    changed="1"
else
    pushd .
    cd repo/3/7/379733022/.git
    oldref=`cat refs/heads/main`
    git fetch
    newref=`cat refs/heads/main`
    popd
    if [[ "$newref" != "$oldref" ]] ; then
        changed="1"
    fi
fi

if [[ "$changed" == "1" ]] ; then
    rm -Rf dataset/test
    ./boa.sh -g -inputJson dataset/py -output dataset/test -inputRepo repo/ -debug
fi

rm -Rf output
./boa.sh -e -d dataset/test/ -i py-classify.boa -o output

./failingtests.py
./failingtests.py | wc -l