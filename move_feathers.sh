#!/bin/bash

source_dir="/Users/jamesjones/game_logs"
destination_dir="/Users/jamesjones/git/MFN/feathers"

# Create the destination directory if it doesn't exist
mkdir -p "$destination_dir"

# Look for .feather files in the source directory and its subdirectories
find "$source_dir" -type f -name "*.feather" -exec cp {} "$destination_dir" \;

