#!/bin/bash
# for execution without jupyter and just in a terminal, this script converts the .ipynb file to a 
# .py and launches it
jupyter nbconvert --to script load_and_apply_ner.ipynb
python load_and_apply_ner.py
rm load_and_apply_ner.py
