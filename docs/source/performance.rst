Asset Performance
==================

.. toctree::
   :maxdepth: 1


The performance indicators presented on this page take the form
of ``python`` functions and may be imported as follows:

    .. jupyter-execute::

        import practice.finance.performance as perf


To assist with the demonstration and visualization of the indicators
imported above, the following dataset will be used throughout the
examples presented on this page:

    .. jupyter-execute::

        import os
        import pandas

        subpaths = {
            'asset': 'data/asset.5y.csv.gz',
            'market': 'data/market.5y.csv.gz', }

        def read(subpath):
            import practice
            basedir = os.path.dirname(practice.__file__)
            path = os.path.join(*[basedir] + subpath.split('/'))
            DF = pandas.read_csv(path, compression='gzip')
            ix = pandas.to_datetime(DF.pop('date'))
            return DF.set_index(ix)

        data = {}
        for name, subpath in subpaths.items():
            DF = read(subpath)
            data[name] = DF['close']

        DF = pandas.DataFrame(data)

        asset = DF['asset']
        market = DF['market']

        print(DF.head())

    .. image:: ../../images/finance/AssetOhlc.png
       :align: center


Beta
----------

Beta is the risk measurement that captures the volatility of a security with
respect to the overall market volatility, or systematic risk.

For example, a security with a Beta of 1.20 is said to be 20% more volatile
than the market.  If this market had an intraday return of 10%, then the
security would be expected to have an intraday return of 12% (`= 1.20 x 10%`).

Mathematically, Beta may be calculated using either linear regression or
the Capital Asset Pricing Model.


    .. jupyter-execute::

        returns_window = 1
        annual_window = 252
        beta_window20 = 20
        beta_window50 = 50

        columns = [
            fr'$\sigma$-asset({annual_window})',
            fr'$\sigma$-market({annual_window})',
            fr'$\beta$({beta_window20})',
            fr'$\beta$({beta_window50})',
            fr'$\beta$({annual_window})', ]


        asset_returns = perf.percentChange(asset, returns_window)
        market_returns = perf.percentChange(market, returns_window)

        results = [
            perf.calcVolatity(asset, annual_window),
            perf.calcVolatity(market, annual_window),
            perf.beta(asset_returns, market_returns, beta_window20),
            perf.beta(asset_returns, market_returns, beta_window50),
            perf.beta(asset_returns, market_returns, annual_window), ]

        DF = pandas.DataFrame(dict(zip(columns, results)))
        print(DF.tail())

    .. image:: ../../images/finance/Beta.png
       :align: center

The corresponding dependency tree is depicted in the following figure:

    .. image:: ../../images/finance/Beta_dep_tree.png
       :scale: 55 %
       :align: center