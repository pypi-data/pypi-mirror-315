#!/bin/bash

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run the Nexus Agent application using Streamlit
streamlit run src/main.py "$@"
