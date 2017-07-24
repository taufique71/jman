#!/bin/bash
#virtualenv -p /usr/bin/python ./
source ~/Codes/widespace-job-manager/bin/activate
pip install -r requirement.txt
python main.py
deactivate


#!/bin/bash -e

#BASEDIR=`dirname $0`/..

#if [ ! -d "$BASEDIR/ve" ]; then
    #virtualenv -q $BASEDIR/ve --no-site-packages
    #echo "Virtualenv created."
#fi

#if [ ! -f "$BASEDIR/ve/updated" -o $BASEDIR/requirements.pip -nt $BASEDIR/ve/updated ]; then
    #pip install -r $BASEDIR/requirements.pip -E $BASEDIR/ve
    #touch $BASEDIR/ve/updated
    #echo "Requirements installed."
#fi

#source $BASEDIR/ve/bin/activate
#cd $BASEDIR
#export PYTHONPATH=.

#exec python $@
