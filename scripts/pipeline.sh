#!/bin/bash

set -euxo pipefail

date=$1
if [ -z "$date" ]; then
    echo "Please provide a date"
    exit 1
fi

echo "Running pipeline for date: $date"

# Run the pipeline
source=https://dumps.wikimedia.org/kowiki/$date

save_dir=../kowiki_data/$date
workspace=$save_dir/workspace
mkdir -p $save_dir
mkdir -p $workspace

# Download the data

function download(){
    unzipped_filename=$1
    unzipped_path=$workspace/$unzipped_filename
    zipped_path=$workspace/$unzipped_filename.bz2
    if [ -f $unzipped_path ]; then
        echo "File already exists: $unzipped_path"
    else
        wget -c -O $zipped_path $source/$unzipped_filename.bz2
        bzip2 -d $zipped_path
    fi
}

fname_article=kowiki-$date-pages-articles.xml
fname_index=kowiki-$date-pages-articles-multistream-index.txt
download $fname_article &
download $fname_index &
wait

python split_dump_to_wikitext_files.py --date $date
python concatenate.py --date $date
python generate_dataset.py --date $date