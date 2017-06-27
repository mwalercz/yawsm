#!/bin/bash
EGGDIR="ws_dist_queue.egg-info"

if [ -d "$EGGDIR" ]; then
    rm -rf ${EGGDIR}
fi

echo 'Building development egg'
pip install -q -e .
pip install -q -r requirements_dev.txt

"$@"
