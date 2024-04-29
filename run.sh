#!/bin/bash

# Check if the activate script exists
if [ -f "./.venv/bin/activate" ]; then
    echo "Activating existing virtual environment."
    source "./.venv/bin/activate"
else
    echo "Virtual environment does not exist. Creating virtual environment."
    python3 -m venv .venv
    source "./.venv/bin/activate"
    pip install -r requirements.txt  
fi

# Check if the model checkpoint file exists
if [ ! -f "./saved_models/isnetis.ckpt" ]; then  
    echo "Downloading model checkpoint."
    mkdir -p ./saved_models  
    curl -L "https://huggingface.co/skytnt/anime-seg/resolve/main/isnetis.ckpt?download=true" -o "./saved_models/isnetis.ckpt"
fi

# Run the inference script
python3 inference.py