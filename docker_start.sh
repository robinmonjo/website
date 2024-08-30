#!/bin/bash

PYTHON_ENV="production" PORT=80 WEB_CONCURRENCY=4 .venv/bin/python main.py &
make serve-llm &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
