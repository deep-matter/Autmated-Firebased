#!/bin/bash

python -m venv Firebase

if  [ "$(uname)" == "Linux" ]; then
    source Firebase/bin/activate
elif [ "$(uname)" != "Windows" ]; then
    source Firebase/Scripts/activate.bat
fi

pip install -r requirements.txt



