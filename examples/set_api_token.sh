#!/bin/bash

printf "Enter JWT token: "
read -r JWT_TOKEN
export MVC_API_TOKEN="$JWT_TOKEN"
