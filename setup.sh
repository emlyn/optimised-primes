#!/bin/bash

pip install -r requirements.txt

# install JS/CSS in correct place
jupyter nbextension install rise --py --sys-prefix

# enable the extension
jupyter nbextension enable rise --py --sys-prefix

echo "Run 'jupyter notebook' to load notebook"
