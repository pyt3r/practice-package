Technical Analysis
===================

.. toctree::
   :maxdepth: 1

.. jupyter-execute::
    :hide-code:

    import sys, os
    here = os.getcwd()
    basedir = os.path.join(here, '..')
    sys.path.insert(0, basedir)
    os.chdir(basedir)


The technical analysis functions presented on this page may be
imported as follows:

    .. jupyter-execute::

        import practice.technical_analysis as ta


In an attempt to demo and visualize the results of these tools, the
following dataset will be used:

    .. jupyter-execute::

        import pandas

        path = 'practice/data/jpm.csv.gz'
        DF = pandas.read_csv(path, compression='gzip')
        ix = pandas.to_datetime(DF.pop('date'))
        DF = DF.set_index(ix)

        print(DF.head())


    .. image:: ../../practice/technical_analysis/jpm_data.png


MAs & Crosses
----------------

A function for computing the simple moving average (MA) is
depicted as follows:

    .. literalinclude:: ../../practice/technical_analysis/__init__.py
       :pyobject: simpleMA

A function for computing the exponentially weighted MA is
depicted as follows:

    .. literalinclude:: ../../practice/technical_analysis/__init__.py
       :pyobject: expMA



When a short term Moving Average (MA) intersects a moving average with
a longer term, a crossover is said to have occurred.

    .. literalinclude:: ../../practice/technical_analysis/__init__.py
       :pyobject: crossover


Implementation:

    .. jupyter-execute::

        import practice


Bollinger Bands
----------------

The following functions may be used to calculate the upper and lower
Bollinger Bands:

    .. literalinclude:: ../../practice/technical_analysis/__init__.py
       :pyobject: bollUpper

    .. literalinclude:: ../../practice/technical_analysis/__init__.py
       :pyobject: bollLower

    .. literalinclude:: ../../practice/technical_analysis/__init__.py
       :pyobject: boll


Implementation:

    .. jupyter-execute::

        window = 20
        stdevs = 2

        Bollinger = pandas.DataFrame({
            'avg'   : ta.simpleMA(DF['price'], window),
            'upper' : ta.bollUpper(DF['price'], window, stdevs),
            'lower' : ta.bollLower(DF['price'], window, stdevs), })

        print(Bollinger.tail())


    .. image:: ../../practice/technical_analysis/bollinger.png
       :align: center

    .. image:: ../../practice/technical_analysis/bollinger_dep_tree.png
       :scale: 60 %
       :align: center

