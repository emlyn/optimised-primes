# Optimised Primes

> There's more to them than meets the eye.\
> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &mdash; Optimus Prime

A Jupyter (Python) notebook exploring a few simple prime generating algorithms in an interactive slideshow.

## Viewing

The easiest way is to just view a pre-generated version of the slideshow or notebook. However, you won't be able to evaluate any code yourself.

### Slides

A static version of the slides, with pre-generated plots, is viewable [here](https://emlyn.github.io/optimised-primes).

### Notebook

Alternatively, you can view it in the normal notebook format on [nbviewer](https://nbviewer.jupyter.org/github/emlyn/optimised-primes/blob/master/Primes.ipynb).

## Running

### Online

If you would like to run the code yourself (and possibly edit it), you can run the notebook online with [binder](https://mybinder.org/v2/gh/emlyn/optimised-primes/master?filepath=Primes.ipynb). It will take a little while to load the environment, then:
- Evaluate the first cell (by pressing `shift+Enter` or `ctrl+Enter`) to initialise the notebook.
- Press the <img src="resources/show.png" width="34" height="25" alt="RISE Slideshow button"> "Enter/Exit RISE Slideshow" button (or press `alt+r`) to start the slideshow.
- Make sure you evaluate each cell in the slideshow (by clicking inside it and pressing `shift+Enter` or `ctrl+Enter`), as later cells will depend on previous results.

### Local

You can also run it locally on your computer:
- Clone this repo so that you have a copy of the code locally.
- Run the `pip install -r requirements.txt` to install dependencies (this only has to be done the first time).
- Run `jupyter notebook` to start the notebook server.
- In the browser window that opens click on `Primes.ipynb` to load the notebook.
- Run the notebook (as decribed above).

## Credits

The clever algorithm at the end (based on the Sieve of Eratosthenes) was found on a webpage that now appears to be offline.
An archive of it is still viewable on the wayback machine
[here](https://web.archive.org/web/20150710134640/http://diditwith.net/2009/01/20/YAPESProblemSevenPart2.aspx).

Timing plots are graphed with [Bokeh](https://bokeh.pydata.org/en/latest/).

Notebook is displayed as slides using [RISE](https://github.com/damianavila/RISE).
