# Optimised Primes

> There's more to them than meets the eye.\
> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &mdash; Optimus Prime

A Jupyter (Python) notebook exploring a few simple prime generating algorithms in an interactive slideshow.

Starting from the most naïve algorithm, and slowly improving it to arrive at a reasonably optimised
and clever algorithm based on the sieve of Eratosthenes,
that I found on a page that has since been taken down and now only exists in the wayback machine
[here](https://web.archive.org/web/20150710134640/http://diditwith.net/2009/01/20/YAPESProblemSevenPart2.aspx).

Uses [RISE](https://github.com/damianavila/RISE) to display the notebook as slides,
and [Bokeh](https://bokeh.pydata.org/en/latest/) for plotting the charts.

## Installing / Running

You can view a static version (i.e. the code has all been pre-evaluated) of the slide show
[here](https://emlyn.github.io/optimised-primes), or view the notebook on
[nbviewer](https://nbviewer.jupyter.org/github/emlyn/optimised-primes/blob/master/Primes.ipynb).

If you want to run it interactively (i.e. evaluate the code yourself):

- Clone this repo so that you have a copy of the code locally.
- Run the `setup.sh` script to install dependencies and plugins (this only has to be done the first time).
- Run `jupyter notebook` to start the notebook server.
- In the browser window that opens click on `Primes.ipynb` to load the notebook.
- Evaluate the first cell (select it then press `shift+Enter` or `ctrl+Enter`) to initialise notebook.
- Click the <img src="resources/show.png" width="34" height="25" alt="RISE Slideshow button"> "Enter/Exit RISE Slideshow" button (or press `alt+r`) to start the slideshow.
- Make sure you evaluate each cell in the slideshow (by clicking inside it and pressing `shift+Enter` or `ctrl+Enter`), as later cells will depend on previous results.
