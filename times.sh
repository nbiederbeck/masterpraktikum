#!/bin/bash
hyperfine \
    'cd 01-20180416-DebyeScherrer         && rm -f build/main.pdf && make' \
    'cd 02-20180507-GepulsteNMR           && rm -f build/main.pdf && make' \
    'cd 03-20180611-Diodenlaser           && rm -f build/main.pdf && make' \
    'cd 04-20180702-Operationsverstaerker && rm -f build/main.pdf && make' \
--export-markdown times.md
