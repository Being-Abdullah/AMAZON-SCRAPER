#!/bin/bash

# Define the list of files
files=(
  "product_48dd2d45a4a5.csv"
  "product_8bea9c87802e.csv"
  "product_af36506169fd.csv"
  "product_e2609b38cc8b.csv"
  "product_064c1b6daf9a.csv"
  "product_4ff972c05c3d.csv"
  "product_8ce7325abc6b.csv"
  "product_b005f08158c7.csv"
  "product_e556a4579e1b.csv"
  "product_095328994f23.csv"
  "product_5732a877872b.csv"
  "product_8d4614ed520a.csv"
  "product_c82988bc10fa.csv"
  "product_eadc7025c380.csv"
  "product_edb89f05077d.csv"
  "product_faed54178223.csv"
  "product_fd8000871698.csv"
  # Add other filenames here
)

# Destination path
destination="C:/Users/LogicMount/Desktop"

# Download each file
for file in "${files[@]}"; do
  scp "root@37.27.112.54:/home/data/$file" "$destination"
done
