#!/bin/bash

export CMAKE_ARGS="-DLLAMA_METAL=on"
export FORCE_CMAKE=1
pip install llama-cpp-python
pip install -r requirements.txt
streamlit run app.py