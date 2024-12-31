#!/bin/sh

# Variables
INPUT_CSV="text_links.csv"
SAVE_FOLDER="data" # Folder to save files

# Ensure the save folder exists
mkdir -p "$SAVE_FOLDER"

# Process the CSV
while IFS=',' read -r filename url; do
    # Skip the header row if it matches "filename,url"
    if [ "$filename" = "filename" ] && [ "$url" = "url" ]; then
        continue
    fi

    filename=$(echo "$filename" | tr -d '\r' | xargs)
    url=$(echo "$url" | tr -d '\r' | xargs)
    echo "$url"
    echo "$filename"

    # Check if URL starts with a valid scheme
    if [[ "$url" =~ ^https?:// ]]; then
        # Download the file using wget
        wget -O "$SAVE_FOLDER/$filename" "$url"
    else
        echo "Invalid URL scheme: $url"
    fi
done < "$INPUT_CSV"

echo "Download complete. Files are saved in $SAVE_FOLDER."