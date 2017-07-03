#!/usr/bin/env sh
EGGDIR="ws_dist_queue.egg-info"

#if [ -d "$EGGDIR" ]; then
#    rm -rf ${EGGDIR}
#fi

echo 'Building development egg'
pip install -e .
pip install -r requirements_dev.txt

"$@"
