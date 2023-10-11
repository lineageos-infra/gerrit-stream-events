#!/bin/bash
set -euo pipefail
IFS=$'\n\t'


mkdir -p ~/.ssh
chmod 600 ~/.ssh
ssh-keyscan -p 29418 review.lineageos.org > ~/.ssh/known_hosts
echo $GERRIT_SSH_KEY > ~/.ssh/id_rsa


ssh review.lineageos.org -p 29418 gerrit stream-events | python main.py

