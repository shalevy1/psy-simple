#!/bin/bash
set -e

WORK=`pwd`

echo "Cloning $TRAVIS_BRANCH from $REPO"
git clone -b $TRAVIS_BRANCH $REPO deploy
cd deploy

sed -i "s#https://#git://#" .gitmodules

echo "Initializing submodule $REFDIR"
git submodule update --init $REFDIR

sed -i "s#git://#https://#" .gitmodules

echo "Pull from origin"
cd $REFDIR
git checkout $REFBRANCH
git pull

echo "deploying ..."
cd $WORK
bash ci/deploy.sh deploy $TRAVIS_BRANCH "$REFDIR" .gitmodules

rm -rf deploy