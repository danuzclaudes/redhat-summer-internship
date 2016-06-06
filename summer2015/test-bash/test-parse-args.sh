#!/usr/bin/env bash
if [ ! $# == 1 ]; then
   echo "usage ./test-parse-args <args>"
fi

echo $1
export MYVAR=$1
echo $MYVAR

