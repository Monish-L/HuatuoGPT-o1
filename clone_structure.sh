#!/bin/bash

# Script to recreate HuatuoGPT-o1 directory structure with a different name
# Usage: ./clone_structure.sh <new-project-name> [destination-path]

if [ -z "$1" ]; then
    echo "Usage: $0 <new-project-name> [destination-path]"
    echo "Example: $0 MyNewProject /home/user/"
    exit 1
fi

NEW_NAME="$1"
DEST_PATH="${2:-.}"  # Default to current directory if not specified
SOURCE_DIR="/home/user/HuatuoGPT-o1"

# Create the base directory
NEW_DIR="$DEST_PATH/$NEW_NAME"
echo "Creating directory structure for: $NEW_DIR"

# Create all directories
mkdir -p "$NEW_DIR"/{assets,configs,data,evaluation/data,ppo_utils}

echo "✓ Created directory structure:"
echo "  $NEW_DIR/"
echo "  ├── assets/"
echo "  ├── configs/"
echo "  ├── data/"
echo "  ├── evaluation/"
echo "  │   └── data/"
echo "  └── ppo_utils/"

# Copy important configuration files (non-data files)
echo ""
echo "Copying configuration files..."

# Copy .gitignore if it exists
if [ -f "$SOURCE_DIR/.gitignore" ]; then
    cp "$SOURCE_DIR/.gitignore" "$NEW_DIR/"
    echo "✓ Copied .gitignore"
fi

# Copy Python files from root
for file in "$SOURCE_DIR"/*.py; do
    if [ -f "$file" ]; then
        cp "$file" "$NEW_DIR/"
        echo "✓ Copied $(basename $file)"
    fi
done

# Copy markdown files
for file in "$SOURCE_DIR"/*.md; do
    if [ -f "$file" ]; then
        cp "$file" "$NEW_DIR/"
        echo "✓ Copied $(basename $file)"
    fi
done

# Copy requirements files
for file in "$SOURCE_DIR"/requirements*.txt; do
    if [ -f "$file" ]; then
        cp "$file" "$NEW_DIR/"
        echo "✓ Copied $(basename $file)"
    fi
done

# Copy config files
if [ -d "$SOURCE_DIR/configs" ]; then
    cp -r "$SOURCE_DIR/configs/"* "$NEW_DIR/configs/" 2>/dev/null
    echo "✓ Copied config files"
fi

# Copy ppo_utils files
if [ -d "$SOURCE_DIR/ppo_utils" ]; then
    cp -r "$SOURCE_DIR/ppo_utils/"* "$NEW_DIR/ppo_utils/" 2>/dev/null
    echo "✓ Copied ppo_utils files"
fi

# Copy evaluation scripts
if [ -f "$SOURCE_DIR/evaluation/"*.py ] 2>/dev/null; then
    cp "$SOURCE_DIR/evaluation/"*.py "$NEW_DIR/evaluation/" 2>/dev/null
    echo "✓ Copied evaluation scripts"
fi

echo ""
echo "================================================"
echo "✓ Successfully created $NEW_NAME"
echo "  Location: $NEW_DIR"
echo "================================================"
echo ""
echo "Note: This copies the structure and code files."
echo "Data files in /data and /evaluation/data are NOT copied."
echo "You can manually copy data files if needed."
