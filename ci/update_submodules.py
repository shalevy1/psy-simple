#!/usr/bin/env python
import os
import os.path as osp
from utils import repo, get_ref_dir, get_ref_branch
from deploy import deploy
import subprocess as spr
import shutil

ref_dir = get_ref_dir()
ref_branch = get_ref_branch()

if os.getenv('TRAVIS'):
    this_branch = os.getenv('TRAVIS_BRANCH')
elif os.getenv('APPVEYOR'):
    this_branch = os.getenv('APPVEYOR_REPO_BRANCH')

deploy_dir = 'deploy'

work = os.abspath(os.getcwd())

# clone directory
spr.check_call(['git', 'clone', '-b', this_branch, repo, deploy_dir])

os.chdir(deploy_dir)

spr.check_call(['git', 'branch', 'TRAVIS_DEPLOY'])

spr.check_call(['git', 'checkout', 'TRAVIS_DEPLOY'])

spr.check_call(['git', 'submodule', 'update', '--init', ref_dir])

os.chdir(ref_dir)
spr.check_call(['git', 'checkout', ref_branch])
spr.check_call(['git', 'pull'])

os.chdir(work)

deploy(osp.join(deploy_dir, ref_dir), this_branch, ref_dir, '.gitmodules')

shutil.rmtree(deploy_dir)