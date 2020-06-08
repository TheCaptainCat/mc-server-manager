#! /bin/bash
source ./venv/bin/activate
python ./mc.py &
python ./server.py run_server &