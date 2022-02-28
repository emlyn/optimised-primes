import os
from bokeh.io import output_notebook, push_notebook, show
from bokeh.layouts import layout
from bokeh.models.callbacks import CustomJS
from bokeh.models.formatters import BasicTickFormatter, NumeralTickFormatter
from bokeh.models.ranges import DataRange1d
from bokeh.models.sources import ColumnDataSource
from bokeh.models.widgets import Button, Panel, Paragraph, Slider, Tabs, Toggle
from bokeh.palettes import Category10
from bokeh.plotting import figure
from collections import OrderedDict
from IPython.display import display, Javascript
from itertools import count, islice
from math import log
from timeit import timeit


def getint(name, default):
    return int(os.environ.get(name, str(default)))


def getbool(name, default):
    return os.environ.get(name, str(default)).lower() == 'true'


def null_func():
    "Wrapper that does nothing, so we can estimate timing overhead"
    def null_gen():
        yield 0
    return list(islice(null_gen(), 0, 1))[0]


_repeats = getint('PRIMES_REPEATS', 3)
_incremental = getbool('PRIMES_INCREMENTAL', True)
_palette = Category10[10]
_lines = OrderedDict()
_overhead = timeit(null_func, number=1000, globals=globals()) / 1000.0


def iterations():
    for x in count():
        for i in (1, 2, 5):
            yield i * 10 ** x


def approx_nth(n):
    "Return a number greater or equal to nth prime for sieve type algorithms"
    return int(2.2 * n + 1) if n < 6 else int(n * (log(n) + log(log(n))))


def plot_line_separate(genfn, source, handle):
    "Time a generator while plotting result, using a separate generator for each point"
    # Generate first 1000 primes to warm up the code first
    list(islice(genfn(approx_nth(1000)), 999, 1000))[0]
    for r in range(_repeats):
        for n, i in enumerate(iterations()):
            def timed():
                return list(islice(genfn(approx_nth(i)), i - 1, i))[0]
            t = timeit(timed, number=1, globals=globals()) - _overhead
            if r == 0:
                # First time, stream every measurememt to the plot
                source.stream(dict(x=[i], y=[t]))
            else:
                # Then patch in any lower measurements
                if t < source.data['y'][n]:
                    source.patch(dict(x=[(n, i)], y=[(n, t)]))
            if handle:
                push_notebook(handle=handle)
            if r == 0:
                # First time through keep going until just over 1 second elapsed
                # with a slight buffer in case following measurements bring it down
                if t >= 1.2:
                    break
            else:
                # On following passes remeasure each existing point
                if n >= len(source.data['x']) - 1:
                    break


def plot_line_combined(genfn, source, handle):
    "Time a generator while plotting result, using a single generator for the line"
    # Generate first 1000 primes to warm up the code first
    list(islice(genfn(), 999, 1000))[0]
    for r in range(_repeats):
        t = 0.0
        last_i = 0
        last_t = 0.0
        gen = genfn()
        for n, i in enumerate(iterations()):
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
            if handle:
                push_notebook(handle=handle)
            last_i = i
            if r == 0:
                # First time through keep going until just over 1 second elapsed
                # with a slight buffer in case following measurements bring it down
                if last_t > 1.2:
                    break
            else:
                # On following passes remeasure each existing point
                if n >= len(source.data['x']) - 1:
                    break


def timing_plot(genfn):
    "Draw a timing plot for a prime generator function"
    global _lines

    def plot(fig, name, vals, num, dash='solid'):
        "Add a line with points to a plot"
        col = _palette[num % len(_palette)]
        fig.line('x', 'y', legend_label=name, source=vals, line_dash=dash, color=col)
        fig.scatter('x', 'y', legend_label=name, source=vals, marker='o', color=col)
    name = genfn.__name__
    exist = None
    args = dict(plot_width=800, plot_height=400, toolbar_location='above', title="Timing")
    linfig = figure(y_range=[0, 1], x_range=DataRange1d(start=0), **args)
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
        fig.legend.click_policy = 'hide'
        fig.legend.background_fill_alpha = 0.5
    linfig.yaxis.formatter = BasicTickFormatter()
    logfig.yaxis.formatter = BasicTickFormatter(use_scientific=True, precision=0)
    lintab = Panel(child=linfig, title="Linear")
    logtab = Panel(child=logfig, title="Log")
    tabs = Tabs(tabs=[lintab, logtab])
    handle = None
    if _incremental:
        # Incremental: show plot now, then incrementally add points
        handle = show(tabs, notebook_handle=True)

    if genfn.__code__.co_argcount == 0:
        # Generate line in one go
        plot_line_combined(genfn, source, handle)
    else:
        # Generator takes size, need to generate points separately
        plot_line_separate(genfn, source, handle)

    if not _incremental:
        # Plot not shown yet, show it now
        show(tabs)
    # save line data to show on next plot
    _lines[name] = source.data


def primes_clear():
    global _lines
    _lines = OrderedDict()


def primes_incremental(enabled):
    global _incremental
    _incremental = enabled


def primes_repeats(num):
    global _repeats
    _repeats = num


_init_js = '''
require(['base/js/namespace', 'base/js/events'],
function (Jupyter, events) {
    function swap_src(el, src, t) {
        var old = el.src;
        el.src = src;
        setTimeout(function() {el.src = old;}, t);
    }

    // save a reference to the cell we're currently executing inside of,
    // to avoid clearing it later (which would remove this js)
    var this_cell = $(element).closest('.cell').data('cell');

    function primes_clear() {
        // Call Python callback
        Jupyter.notebook.kernel.execute('from helpers import primes_clear\\n' +
                                        'primes_clear()');
        // Clear (other) cell outputs
        Jupyter.notebook.get_cells().forEach(function (cell) {
            if (cell.cell_type === 'code' && cell !== this_cell) {
                cell.clear_output();
            }
        });
        Jupyter.notebook.set_dirty(true);
        // Make sieve clickable to start gif
        sieve.src = 'resources/sieve1.png';
        sieve.onclick = function() {
            swap(document.getElementById('sieve'), 'resources/sieve.gif', 37000);
        };
    }

    function primes_incremental(enabled) {
        // Call Python callback
        var en = enabled ? 'True' : 'False';
        Jupyter.notebook.kernel.execute('from helpers import primes_incremental\\n' +
                                        'primes_incremental(' + en + ')');
    }

    function primes_repeats(num) {
        // Call Python callback
        Jupyter.notebook.kernel.execute('from helpers import primes_repeats\\n' +
                                        'primes_repeats(' + num + ')');
    }

    window.primes_clear = primes_clear;
    window.primes_incremental = primes_incremental;
    window.primes_repeats = primes_repeats;
});
'''


def init():
    output_notebook()
    display(Javascript(_init_js))
    clearbutton = Button(label="Clear")
    clearbutton.js_on_click(CustomJS(code='primes_clear();'))
    increm = Toggle(label='Incremental', active=True)
    increm.js_on_click(CustomJS(code='primes_incremental(cb_obj.active)'))
    repeats = Slider(start=1, end=10, value=3)
    repeats.js_on_change('value', CustomJS(code='primes_repeats(cb_obj.value)'))
    show(layout([
        [clearbutton, Paragraph(text='Clear timing plots and cell outputs (before restarting slideshow).')],
        [increm, Paragraph(text='Update timing plots incrementally (disable for static slide show).')],
        [repeats, Paragraph(text='Repeats for timing measurements (higher is more accurate, but slower).')]]))
