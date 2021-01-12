#!/bin/bash
set -x
source .env
while true; do python bot.py; sleep 30; done
