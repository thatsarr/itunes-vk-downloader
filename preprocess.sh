#!/bin/bash
if [ $# -ne 1 ]; then
    echo "usage: $0 <filename>"
    exit 1
fi
iconv -f utf-16le -t utf-8 $1 > $1.tmp
sed -i "s/\r/\n/g" $1.tmp
sed -i "s/\t\+/|/g" $1.tmp
