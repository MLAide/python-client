#!/bin/bash

printf "Enter project key: "
read -r PROJECT_KEY
export MVC_PROJECT_KEY="$PROJECT_KEY"

printf "Enter experiment key: "
read -r EXPERIMENT_KEY
export MVC_EXPERIMENT_KEY="$EXPERIMENT_KEY"

printf "Running data preprocessing\n"
python data_ingest.py

printf "Running model training\n"
python training.py
