#!/bin/bash
cp -r ./ /opt/ulysses
cd /opt/ulysses
mkdir -p data/logs
pip install virtualenv
virtualenv env --python python3.7
pip install -r requirements.txt
cp data/static/com.github.vicentealencar.ulysses.plist /Library/LaunchDaemons
launchctl load -w /Library/LaunchDaemons/com.github.vicentealencar.ulysses.plist
