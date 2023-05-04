#!/bin/bash

if [[ -z "${CFG_DEV}" ]]; then
    echo Production mode
    python3 index.py
else
    echo Development mode
    python3 dbutils.py create
    nodemon -w aime --legacy-watch index.py
fi

