Technical Analysis
==================

.. toctree::
   :maxdepth: 1


The technical analysis indicators presented on this page take
the form of ``python`` functions and may be imported as follows:

    .. jupyter-execute::

        import practice.finance.technical_analysis as ta


To assist with the demonstration and visualization of the indicators
imported above, the following dataset will be used throughout the
examples presented on this page:

    .. jupyter-execute::

        import os
        import pandas
        import practice

        basedir = os.path.dirname(practice.__file__)
        subpath = 'data/data.csv.gz'
        path = os.path.join(*[basedir]+subpath.split('/'))

        DF = pandas.read_csv(path, compression='gzip')
        ix = pandas.to_datetime(DF.pop('date'))
        DF = DF.set_index(ix)

        price = DF['close']
        print(DF.head())


    .. image:: ../../images/finance/DataOhlc.png
       :align: center


Moving Average
----------------

SMA
***********

A function for computing the simple moving average (SMA) is
depicted as follows:

    .. literalinclude:: ../../practice/finance/technical_analysis.py
       :pyobject: simpleMA


EMA
***********

In contrast to the simple moving average, which weights prices evenly
across a given window, the exponential moving average (EMA) weights
recent price observations more heavily than the older ones, and as
a result, depicts a trenline which reacts quicker to the recent price
movements.

While there are several hyperparameters for adjusting the weights,
the EMA function used on this page takes a simple form:

    .. literalinclude:: ../../practice/finance/technical_analysis.py
       :pyobject: expMA


A comparison of the SMA and EMA may be found in the following snippet
and plot:

    .. jupyter-execute::

        window = 30

        MA = pandas.DataFrame({
            'price': price,
            f'sma({window})': ta.simpleMA(price, window),
            f'ema({window})': ta.expMA(price, window), })

        print(MA.tail())

    .. image:: ../../images/finance/MovingAverage.png
       :align: center


Crossovers
----------------

A "crossover" occurs when either:

  1. the underlying price intersects with a technical indicator, or
  2. one technical indicator intersects with another.

Technical analysts use crossover events to assess how the price
will perform in the near future.

For example, a Technical Analysts might observe when a short term MA
intersects with a longer term MA.  When the short term MA intersects the long term MA from the bottom,
the period to come is more likely to be indicative of a bullish period.
If an intersection were to occur in the opposite direction, the period is more likely to be indicative of a bearish
period.

    .. jupyter-execute::

        short_window = 15
        long_window =  50
        lag = 1

        short = ta.simpleMA(price, short_window)
        long  = ta.simpleMA(price, long_window)
        cross = ta.crossover(short, long, lag)

        Crossover = pandas.DataFrame({
            'price': price,
            f'sma({long_window})': short,
            f'sma({short_window})': long,
            f'x({short_window},{long_window})': cross, })

        print(Crossover.tail())

    .. image:: ../../images/finance/Crossover.png
       :align: center



Bollinger Bands
----------------

Bollinger Bands are comprised of the following three trendlines, which
may be used by analysts to help identify oversold and overbought signals.

  1. ``+x`` standard deviations of the SMA
  2. the SMA
  3. ``-x`` standard deviations of the SMA

The following example depicts Bollinger Bands with ``x=2`` standard
deviations.

    .. jupyter-execute::

        window = 20
        stdevs = 2

        results = [
            price,
            ta.bollUpper(price, window, stdevs),
            ta.simpleMA(price, window),
            ta.bollLower(price, window, stdevs), ]

        names = [
            'price',
            f'upper({window},{stdevs})',
            f'sma({window})',
            f'lower({window},{stdevs})', ]

        Bollinger = pandas.DataFrame(dict(zip(names, results)))

        print(Bollinger.tail())


    .. image:: ../../images/finance/Bollinger.png
       :align: center


MACD
----------------

Moving Average Convergence Divergence (MACD) involves the following
three calculations; the last of which, the ``MACD distance``, may be used
by analysts in determining the magnitude of bullish or bearish momentum.

  1. MACD is the difference between a long and short EMA.
  2. The Signal Line is then the EMA of the MACD (``#1``).
  3. The MACD Distance is the difference between the MACD (``#1``) and
     Signal Line (``#2``).


This system is exemplified in the following snippet and plot:

    .. jupyter-execute::

        short_window = 12
        long_window = 26
        signal_window = 9

        short  = ta.expMA(price, short_window)
        long   = ta.expMA(price, long_window)
        macd   = ta.macd(price, short_window, long_window)
        signal = ta.expMA(macd, signal_window)
        dist   = ta.macdDistance(macd, signal)

        results = [
            price,
            short,
            long,
            macd,
            signal,
            dist, ]

        names = [
            'price',
            f'sma({short_window})',
            f'sma({long_window})',
            f'macd({short_window},{long_window})',
            f'signal({signal_window})',
            'distance', ]

        Macd = pandas.DataFrame(dict(zip(names, results)))

        print(Macd.tail())


    .. image:: ../../images/finance/Macd.png
       :align: center


The dependency tree of the aforementioned MACD system is depicted in
the following exhibit:

    .. image:: ../../images/finance/Macd_dep_tree.png
       :scale: 55 %
       :align: center



Oscillators
----------------

An oscillator is a trend indicator that fluctuates between an upper
and a lower bound.  Like Bollinger Bands, analysts use oscillators
to help identify oversold and overbought signals.



Stochastic
**********

    .. jupyter-execute::

        stoch_window = 14
        sma_window = 3

        stoch = ta.stochOscillator(price, stoch_window)
        sma   = ta.simpleMA(stoch, sma_window)

        StochOscillator = pandas.DataFrame({
            'price' : price,
            f'stoch({stoch_window})': stoch,
            f'sma({sma_window})': sma, })

        print(StochOscillator.tail())


    .. image:: ../../images/finance/StochasticOscillator.png
       :align: center

ROC
**********

Rate of Change

    .. jupyter-execute::

        short_n = 10
        medium_n = 50
        long_n = 100

        RocOscillator = pandas.DataFrame({
            'price' : price,
            f'roc({short_n})' : ta.rocOscillator(price, short_n),
            f'roc({medium_n})': ta.rocOscillator(price, medium_n),
            f'roc({long_n})'  : ta.rocOscillator(price, long_n), })

        print(RocOscillator.tail())


    .. image:: ../../images/finance/RocOscillator.png
       :align: center



RSI
**********

Relative Strength Index

    .. jupyter-execute::

        window = 14

        Rsi = pandas.DataFrame({
            f'rsiSma({window})' : ta.rsiSma(price, window),
            f'rsiEma({window})' : ta.rsiEma(price, window), })

        print(Rsi.tail())


    .. image:: ../../images/finance/RsiOscillator.png
       :align: center


MFI
**********

Money Flow Index

    .. jupyter-execute::

        window = 14

        high   = DF['high']
        low    = DF['low']
        close  = DF['close']
        volume = DF['volume']

        Mfi = pandas.DataFrame({
            'close'          : close,
            'typical_price'  : ta.typicalPrice(high, low, close),
            'money_flow'     : ta.rawMoneyFlow(high, low, close, volume),
            f'mfi({window})' : ta.mfi(high, low, close, volume, window), })

        print(Mfi.tail())


    .. image:: ../../images/finance/MfiOscillator.png
       :align: center
