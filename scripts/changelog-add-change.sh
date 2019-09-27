#!/bin/bash

curdir=$(dirname ${BASH_SOURCE[0]})
changelog_file=${curdir}/../docs/changelog.md

if sed -n 3p docs/changelog.md | grep UNRELEASED >/dev/null; then
    first_lines=4
else
    first_lines=2
fi

echo -e "## CHANGELOG\n" > /tmp/changelog.md
echo -e "### UNRELEASED\n" >> /tmp/changelog.md
echo "${1}" | sed -r -e 's/(; ?)/\n/g' | sed -r -e 's/^/ - /g' >> /tmp/changelog.md
tail -n +${first_lines} ${changelog_file} >> /tmp/changelog.md
mv /tmp/changelog.md ${changelog_file}
