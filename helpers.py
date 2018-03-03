from bokeh.io import output_notebook, push_notebook, show
from bokeh.models.formatters import BasicTickFormatter, NumeralTickFormatter
from bokeh.models.ranges import DataRange1d
from bokeh.models.sources import ColumnDataSource
from bokeh.models.widgets import Panel, Tabs
from bokeh.palettes import Category10
from bokeh.plotting import figure
from collections import OrderedDict
from itertools import count, islice
from math import log
from timeit import timeit

_repeats = 3
_incremental = True
_palette = Category10[10]
_lines = OrderedDict()

def _null_func():
    "Wrapper that does nothing, so we can estimate timing overhead"
    def null_gen():
        yield 0
    return list(islice(null_gen(), 0, 1))[0]

_overhead = timeit(_null_func, number=1000, globals=globals()) / 1000.0

def _iterations():
    for x in count():
        for i in (1, 2, 5):
            yield i * 10 ** x

def _approx_nth(n):
    "Return a number greater or equal to nth prime for sieve type algorithms"
    return int(2.2 * n + 1) if n < 6 else int(n * (log(n) + log(log(n))))

def _plot_line_separate(genfn, source, handle):
    "Time a generator while plotting result, using a separate generator for each point"
    # Generate first 1000 primes to warm up the code first
    list(islice(genfn(_approx_nth(1000)), 999, 1000))[0]
    for r in range(_repeats):
        for n, i in enumerate(_iterations()):
            def timed():
                return list(islice(genfn(_approx_nth(i)), i - 1, i))[0]
            t = timeit(timed, number=1, globals=globals()) - _overhead
            if r == 0:
                # First time, stream every measurememt to the plot
                source.stream(dict(x=[i], y=[t]))
            else:
                # Then patch in any lower measurements
                if t < source.data['y'][n]:
                    source.patch(dict(x=[(n, i)], y=[(n, t)]))
            push_notebook(handle=handle)
            if r == 0:
                # First time through keep going until just over 1 second elapsed
                # with a slight buffer in case following measurements bring it down
                if t >= 1.2: break
            else:
                # On following passes remeasure each existing point
                if n >= len(source.data['x']) - 1: break

def _plot_line_combined(genfn, source, handle):
    "Time a generator while plotting result, using a single generator for the line"
    # Generate first 1000 primes to warm up the code first
    list(islice(genfn(), 999, 1000))[0]
    for r in range(_repeats):
        t = 0.0
        last_i = 0
        last_t = 0.0
        gen = genfn()
        for n, i in enumerate(_iterations()):
            def timed():
                num = i - last_i
                return list(islice(gen, num - 1, num))[0]
            t = timeit(timed, number=1, globals=globals()) - _overhead
            last_t += t
            if r == 0:
                # First time, stream every measurememt to the plot
                source.stream(dict(x=[i], y=[last_t]))
            else:
                # Then patch in any lower measurements, updating following points
                # as the measurements are cumulative
                if last_t < source.data['y'][n]:
                    diff = source.data['y'][n] - last_t
                    source.patch(dict(y=[(y, source.data['y'][y] - diff)
                                         for y in range(n, len(source.data['y']))]))
                else:
                    last_t = source.data['y'][n]
            push_notebook(handle=handle)
            last_i = i
            if r == 0:
                # First time through keep going until just over 1 second elapsed
                # with a slight buffer in case following measurements bring it down
                if last_t > 1.2: break
            else:
                # On following passes remeasure each existing point
                if n >= len(source.data['x']) - 1: break

def timing_plot(genfn):
    "Draw a timing plot for a prime generator function"
    def plot(fig, name, vals, num, dash='solid'):
        "Add a line with points to a plot"
        col = _palette[num % len(_palette)]
        fig.line('x', 'y', legend=name, source=vals, line_dash=dash, color=col)
        fig.scatter('x', 'y', legend=name, source=vals, marker='o', color=col)
    name = genfn.__name__
    exist = None
    args = dict(plot_width=800, plot_height=400, toolbar_location='above', title="Timing")
    linfig = figure(y_range=[0,1], x_range=DataRange1d(start=0), **args)
    logfig = figure(y_range=[1e-6, 1], x_range=DataRange1d(start=1),
                    x_axis_type='log', y_axis_type='log', **args)
    num = 0
    # add previous lines
    for k, v in _lines.items():
        plot(linfig, k, v, num, 'dashed')
        plot(logfig, k, v, num, 'dashed')
        if k == name:
            exist = num
        num += 1
    source = ColumnDataSource(data=dict(x=[], y=[]))
    for fig in (linfig, logfig):
        plot(fig, name, source, exist or num)
        fig.xaxis.axis_label = "Primes"
        fig.xaxis.formatter = NumeralTickFormatter(format='0[.]0 a')
        fig.xgrid.minor_grid_line_color = 'lightgrey'
        fig.xgrid.minor_grid_line_alpha = 0.2
        fig.yaxis.axis_label = "Seconds"
        fig.legend.location = 'bottom_right'
        fig.legend.click_policy='hide'
        fig.legend.background_fill_alpha = 0.5
    linfig.yaxis.formatter = BasicTickFormatter()
    logfig.yaxis.formatter = BasicTickFormatter(use_scientific=True, precision=0)
    lintab = Panel(child=linfig, title="Linear")
    logtab = Panel(child=logfig, title="Log")
    tabs = Tabs(tabs=[lintab, logtab])
    handle = show(tabs, notebook_handle=True)
    if genfn.__code__.co_argcount == 0:
        _plot_line_combined(genfn, source, handle)
    else:
        _plot_line_separate(genfn, source, handle)
    # save line data to show on next plot
    _lines[name] = source.data

from IPython.display import Javascript

# Cell clearing code based on:
# https://stackoverflow.com/questions/45638720/jupyter-programmatically-clear-output-from-all-cells-when-kernel-is-ready

def init(repeats=3):
    global _repeats
    _repeats = repeats
    output_notebook()
    Javascript('''
require(['base/js/namespace', 'base/js/events'],
function (Jupyter, events) {
    function swap_src(el, src, t) {
        console.log("swap", el, src, t);
        var old = el.src;
        el.src = src;
        setTimeout(function() {el.src = old;}, t);
    }

    // save a reference to the cell we're currently executing inside of,
    // to avoid clearing it later (which would remove this js)
    var this_cell = $(element).closest('.cell').data('cell');
    function init_presentation() {
        // Clear (other) cell outputs
        Jupyter.notebook.get_cells().forEach(function (cell) {
            if (cell.cell_type === 'code' && cell !== this_cell) {
                cell.clear_output();
            }
            Jupyter.notebook.set_dirty(true);
        });
        // Make sieve clickable to start gif
        sieve.src = 'resources/sieve1.png';
        sieve.onclick = function() {
            swap(document.getElementById("sieve"), 'resources/sieve.gif', 37000);
        };
    }

    if (Jupyter.notebook._fully_loaded) {
        // notebook has already been fully loaded, so init now
        init_presentation();
    }
    // Also clear on any future load
    // (e.g. when notebook finishes loading, or when a checkpoint is reloaded)
    events.on('notebook_loaded.Notebook', init_presentation);
});
''')
