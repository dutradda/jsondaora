#!/bin/bash

test_path=$(dirname ${BASH_SOURCE[0]})
tests_regex="s%${test_path}/index/(.*)\.py%\1%g"
test_files="$(find ${test_path}/index/*.py | sed -r -e ${tests_regex})"

for filename in ${test_files}; do
    output_file=${test_path}/index/${filename}.output 
    output_tmpfile=/tmp/${filename}.output

    python3.7 ${test_path}/index/${filename}.py > ${output_tmpfile}
    md5sum ${output_file} ${output_tmpfile} > /tmp/${filename}.checksum

    output=$(sed -r -e 's/(.*) .*/\1/g' /tmp/${filename}.checksum | uniq | wc -l)

    if ! [ ${output} -eq 1 ]; then
        echo -e '\n\n\e[91mOutput assertion error!\e[0m\n\n'
        diff -u ${output_file} ${output_tmpfile}
        echo
        exit 1
    fi
done

echo -e '\n---------------------------------------'
echo 'Docs examples outputs assertion passed!'
echo '---------------------------------------'
