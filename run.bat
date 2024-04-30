@echo off

REM Check if the activate script exists
IF EXIST ".venv\Scripts\activate.bat" (
    echo Activating existing virtual environment.
    CALL ".venv\Scripts\activate.bat"
) ELSE (
    echo Virtual environment does not exist. Creating virtual environment.
    python -m venv .venv
    CALL ".venv\Scripts\activate.bat"
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
    pip3 install -r requirements.txt
)

REM Check if the model checkpoint file exists
IF NOT EXIST "saved_models\isnetis.ckpt" (
    echo Downloading model checkpoint.
    mkdir saved_models
    curl -L "https://huggingface.co/skytnt/anime-seg/resolve/main/isnetis.ckpt?download=true" -o "saved_models\isnetis.ckpt"
)

REM Run the inference script
python inference.py
