#!/bin/sh

echo -n "INTRANET_AUTOLOGIN: "
read INTRANET_AUTOLOGIN

./front/pce-create-sign-session-linux-x64/pce-create-sign-session &

export INTRANET_AUTOLOGIN=$INTRANET_AUTOLOGIN

echo "################################################################################################"
echo "                                    CTRL+C TO KILL THIS APP                                     "
echo "################################################################################################"

pipenv run uvicorn main:app --host 0.0.0.0 --port 8000