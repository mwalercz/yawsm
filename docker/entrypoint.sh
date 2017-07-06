#!/usr/bin/env sh
EGGDIR="dq_broker.egg-info"

#if [ -d "$EGGDIR" ]; then
#    rm -rf ${EGGDIR}
#fi

echo 'Building development egg'
pip install -e .
pip install -r requirements_dev.txt

"$@"
