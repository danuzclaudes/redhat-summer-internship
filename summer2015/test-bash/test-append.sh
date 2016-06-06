#!/usr/bin/env bash
# This script will test >>

# > is used to write to a file and >> is used to append to a file.
# echo 'this is one > statement' > timing-test
# echo 'this is two >>' >> timing-test
# (time pwd) >> timing-test 2>&1
# (time ll) >> timing-test 2>&1

# note: 
# STDIN->0, STDOUT->1, STDERR->2
# 2>&1 means redirect stderr to stdout
# 2>1 right? but & indicates following a file descriptor, not file name

# >>$1 will take inputs from keyboard and append to $1;
# >>$2 <$1 will take the content of $1 and append to $2.
# Example: ./test-append.sh test-append.sh output
case $# in
 1) cat >>$1 ;;
 2) cat >>$2 <$1 ;;
 *) echo \'usage: append from [foo] to [bar]\' ;;
esac

# Note [ + space + "$1"
# http://www.tldp.org/LDP/abs/html/comparison-ops.html
if [ "$1" != "" ] && [ "$2" != "" ]; then
    echo 'append first param ["'$1'"] to 2nd param ["'$2'"]'
fi


