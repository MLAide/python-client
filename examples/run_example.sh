#!/bin/bash

printf "Enter experiment key: "
read -r EXPERIMENT_KEY
export MVC_EXPERIMENT_KEY="$EXPERIMENT_KEY"

printf "Running data preprocessing\n"
python data_preprocessing.py

printf "Running model training\n"
python training.py
