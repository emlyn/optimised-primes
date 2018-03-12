#!/bin/bash

echo "Clearing cell output"
jupyter nbconvert --to notebook --ClearOutputPreprocessor.enabled=True --inplace Primes.ipynb

echo "Evaluating notebook, this may take a few minutes"
PRIMES_INCREMENTAL=False PRIMES_REPEATS=5 jupyter nbconvert --to notebook --execute Primes.ipynb --output temp.ipynb

echo "Converting to html"
jupyter nbconvert --reveal-prefix=. --to slides temp.ipynb --output index
rm temp.ipynb

echo "Moving into gh-pages"
mv index.slides.html gh-pages/index.html
rm -f gh-pages/resources/*
cp resources/* gh-pages/resources/
