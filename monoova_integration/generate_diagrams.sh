#!/bin/bash

# A script to automatically convert all .plantuml files in the docs/ directory
# into PNG images.
#
# DEPENDENCIES:
#   - Java Runtime Environment (JRE)

# --- Configuration ---
PLANTUML_JAR="plantuml.jar"
DOCS_DIR="docs"
OUTPUT_FORMAT="png" # Can be changed to "svg"

# --- Functions ---

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to download the PlantUML jar file
download_plantuml() {
    echo "PlantUML jar not found. Downloading..."
    # Using curl to download from the official source. Following redirects.
    curl -L "https://sourceforge.net/projects/plantuml/files/plantuml.jar/download" -o "$PLANTUML_JAR"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to download plantuml.jar. Please check your internet connection."
        exit 1
    fi
    echo "Download complete."
}

# --- Main Script ---

# 1. Check for Java
if ! command_exists java; then
    echo "Error: Java is not installed. Please install a Java Runtime Environment (JRE) to continue."
    exit 1
fi

# 2. Check for PlantUML jar and download if it doesn't exist
if [ ! -f "$PLANTUML_JAR" ]; then
    download_plantuml
fi

# 3. Find and convert all .plantuml files
echo "Searching for .plantuml files in '$DOCS_DIR/'..."
find "$DOCS_DIR" -type f -name "*.plantuml" | while read -r file; do
    echo "Converting '$file' to $OUTPUT_FORMAT..."
    java -jar "$PLANTUML_JAR" -t"$OUTPUT_FORMAT" "$file"
    if [ $? -eq 0 ]; then
        echo " -> Successfully created ${file%plantuml}$OUTPUT_FORMAT"
    else
        echo " -> Failed to convert '$file'."
    fi
done

echo "Diagram generation complete."
