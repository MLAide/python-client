#!/bin/bash

printf "Enter API key: "
read -r API_KEY
export MLAIDE_API_KEY="$API_KEY"
