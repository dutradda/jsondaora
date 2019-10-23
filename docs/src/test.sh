#!/bin/bash

test_path=$(dirname ${BASH_SOURCE[0]})
tests_regex="s%${test_path}/index/(.*)\.py%\1%g"
test_files="$(find ${test_path}/index/*.py | sed -r -e ${tests_regex})"

for filename in ${test_files}; do
    output_file=${test_path}/index/${filename}.output
    output_file2=${test_path}/index/${filename}.output2
    output_tmpfile=/tmp/${filename}.output
    checksum_file=/tmp/${filename}.checksum
    checksum_file2=/tmp/${filename}.checksum2

    coverage run -p ${test_path}/index/${filename}.py > ${output_tmpfile}
    md5sum ${output_file} ${output_tmpfile} > /tmp/${filename}.checksum
    md5sum ${output_file2} ${output_tmpfile} > /tmp/${filename}.checksum2

    output=$(sed -r -e 's/(.*) .*/\1/g' ${checksum_file} | uniq | wc -l)
    output2=$(sed -r -e 's/(.*) .*/\1/g' ${checksum_file2} | uniq | wc -l)

    if [[ (${output} -ne 1) && (${output2} -ne 1) ]]; then
        echo -e '\n\n\e[91mDocumentation assertion error!\e[0m\n\n'
        diff -u ${output_file} ${output_tmpfile}
        echo
        exit 1
    fi
done

echo -e '\n---------------------------------------'
echo 'Docs examples outputs assertion passed!'
echo '---------------------------------------'
