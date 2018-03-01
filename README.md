# Optimised Primes

> There's more to them than meets the eye.
> &nbsp; &nbsp; &nbsp; &nbsp; - Optimus Prime

A Python notebook looking at different prime generating algorithms in an interactive slideshow.
Uses [Bokeh](https://bokeh.pydata.org/en/latest/) for charts and [RISE](https://github.com/damianavila/RISE) for slides.

Starting from the most naïve algorithm, and slowly improving it to arrive at a reasonably optimised and clever algorithm
based on the sieve of Eratosthenes, that I found on a page that has been taken down and only exists in the wayback machine
[here](https://web.archive.org/web/20150710134640/http://diditwith.net/2009/01/20/YAPESProblemSevenPart2.aspx).

## Installing / Running

You can view a static version of the notebook on
[nbviewer](https://nbviewer.jupyter.org/github/emlyn/optimised-primes/blob/master/Primes.ipynb).

Or to run it interactively or as a slide show:

Clone this repo, and before running for the first time,
run the `setup.sh` script to install dependencies and plugins.
Run `jupyter notebook` to start the notebook server,
and in the browser window that opens click on `Primes.ipynb` to load the notebook.

Evaluate the first cell (select it then press `shift+Enter` or `ctrl+Enter`), and then click the
<img src="resources/show.png" width="34" height="25" alt="RISE Slideshow button"> "Enter/Exit RISE Slideshow"
button to start.
