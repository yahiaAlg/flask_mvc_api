#!/bin/bash

# Script to create Flask PDF app project structure

# Project root (current directory)
# Create directories
mkdir -p app/controllers \
         app/services \
         app/schemas \
         app/models \
         tests

# Create files
# app root files
touch app/config.py \
      app/__init__.py

# controllers, services, schemas, models placeholders
touch app/controllers/__init__.py \
      app/services/__init__.py \
      app/schemas/__init__.py \
      app/models/__init__.py

# tests placeholder
touch tests/__init__.py

# entry point and requirements
touch run.py requirements.txt

echo "Flask PDF app project structure created."
