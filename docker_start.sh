#!/bin/bash

PYTHON_ENV="production" PORT=80 WEB_CONCURRENCY=4 python main.py &
make serve-llm2 &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
