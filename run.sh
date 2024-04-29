# Check if the activate script exists
if [ -f "./.venv/bin/activate" ]; then
    echo "Activating existing virtual environment."
    source "./.venv/bin/activate"
else
    echo "Virtual environment does not exist. Creating virtual environment."
    python3 -m venv .venv
    source "./.venv/bin/activate"
    pip install -r requirements.txt  # Ensure to use -r to install from a requirements file
fi

# Check if the model checkpoint file exists
if [ ! -f "./saved_models/isnetis.ckpt" ]; then  # Fixed syntax error in if statement
    echo "Downloading model checkpoint."
    mkdir -p ./saved_models  # Ensure the directory exists
    # Corrected curl command to specify the output file path with -o
    curl -L "https://huggingface.co/skytnt/anime-seg/resolve/main/isnetis.ckpt?download=true" -o "./saved_models/isnetis.ckpt"
fi

# Run the inference script
python3 inference.py
