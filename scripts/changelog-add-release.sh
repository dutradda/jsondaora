#!/bin/bash

curdir=$(dirname ${BASH_SOURCE[0]})
changelog_file=${curdir}/../docs/changelog.md

read version

sed -i -r -e "s/UNRELEASED/${version} - $(date +%Y-%m-%d)/" ${changelog_file}
