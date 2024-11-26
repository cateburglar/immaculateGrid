#!/usr/bin/env bash

file=$(find -f ./dbSetup/static/csv | fzf)
head -n 1 ${file} | tr ',' '\n'
