#!/bin/bash

# conda env name: kowiki

# set -euxo pipefail

# activate conda environment
eval "$(conda shell.bash hook)"
conda activate kowiki


log_dir=/home/s1/chanwoopark/dataset_scripts/kowikitext/logs
log_path=$log_dir/$(date +%Y%m%d%H%M%S).log
err_path=$log_dir/$(date +%Y%m%d%H%M%S).err
# Run the pipeline
python routine.py 2> $err_path 1> $log_path

