#!/bin/sh

echo "data folder: $1" 
echo "experiment name: $2"

Xvfb :99 -screen 0 1024x768x24 &
export DISPLAY=:99

python imgs2poses.py $1

mv $1/sparse_points.ply $1/sparse_points_interest.ply

python gen_cameras.py $1

python generate_data_image.py --data_dir=$1

mv $1/preprocessed ../../data/$2