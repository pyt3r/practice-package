Financial Analysis
====================

.. toctree::
   :maxdepth: 1


The financial analysis tools presented on this page take the form
of ``python`` functions and may be imported as follows:

    .. jupyter-execute::
        
        import practice.finance.financial_analysis as fa


To assist with the demonstration and visualization of the indicators
imported above, the following dataset will be used throughout the
examples presented on this page:

    .. jupyter-execute::

        import os
        import pandas as pd

        subpaths = {
            'asset': 'data/asset.5y.csv.gz',
            'market': 'data/market.5y.csv.gz', }

        def read(subpath):
            import practice
            basedir = os.path.dirname(practice.__file__)
            path = os.path.join(*[basedir] + subpath.split('/'))
            DF = pd.read_csv(path, compression='gzip')
            ix = pd.to_datetime(DF.pop('date'))
            return DF.set_index(ix)

        data = {}
        for name, subpath in subpaths.items():
            DF = read(subpath)
            data[name] = DF['close']

        DF = pd.DataFrame(data)

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


        asset_returns = fa.simpleReturns(asset, returns_window)
        market_returns = fa.simpleReturns(market, returns_window)

        results = [
            fa.calcVolatity(asset, annual_window),
            fa.calcVolatity(market, annual_window),
            fa.beta(asset_returns, market_returns, beta_window20),
            fa.beta(asset_returns, market_returns, beta_window50),
            fa.beta(asset_returns, market_returns, annual_window), ]

        DF = pd.DataFrame(dict(zip(columns, results)))
        print(DF.tail())

    .. image:: ../../images/finance/Beta.png
       :align: center

The corresponding dependency tree is depicted in the following figure:

    .. image:: ../../images/finance/Beta_dep_tree.png
       :scale: 55 %
       :align: center



Log Returns
------------

The simple return, or the percent difference in price, is a normalized metric, which
is valuable in comparing the performance of multiple assets. The returns (`r`)
of an asset across `x` time periods may be defined as follows, where `p`
is price and `t` is time.

    .. math::
    
        r_{t} = \frac{p_{t} - p_{t-x}}{p_{t}}


Taking the simple return equation from above, the log return relationship may be derived,
as follows, using the assumption that prices are distributed log normally.


    .. math::

        r_{t} = \frac{p_{t} - p_{t-x}}{p_{t}}

        r_{t} + 1 = \frac{p_{t}}{p_{t-x}}

        \log{(r_{t} + 1)} = \log{(\frac{p_{t}}{p_{t-x}})}

        \log{(r_{t} + 1)} = \log{(p_{t}) - \log{(p_{t-x})}}



Whether or not prices are distributed log normally, log returns offer the following benefits:

  * `Mathematical convenience`: many theoretical models assume continuously compounded
    rates of return as it eases the calculus involved in determining rates of change

    .. math::

        e^x = \int{e^x}\,dx = \frac{d}{\,dx}e^x


  * `Good approximations` for short holding periods, or cases where the returns are assumed
    to be small

    .. math::

        \log{(r + 1)} \approx r, r \ll 1


  * `Time additivity`: the `x`-period log return is equivalent to the sum of the log returns
    over each time period in `x`.

    Consider the case using simple returns, which does not have the property of time additivity.

    .. math::

        \prod_{0\leq i\leq x}(r_{i} + 1) = (r_{0} + 1)(r_{1} + 1)...(r_{x} + 1)

    Now consider the case using log returns.

    .. math::

        \sum_{0\leq i\leq x}\log{(r_{i} + 1)} = \log{(r_{0} + 1)} + \log{(r_{1} + 1)} + ... + \log{(r_{x} + 1)}


    The following example demonstrates the concept of time additivity as it applies
    to log returns.

    .. jupyter-execute::

        import numpy as np

        AssetPrices = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [3, 4, 5, 6, 7],
            'C': [5, 6, 7, 8, 9],
        })

        LogReturns1    = fa.logReturns(AssetPrices, 1)
        TimeAdditivity = LogReturns1.sum()
        LogReturnsMax  = fa.logReturns(AssetPrices, len(AssetPrices) - 1)

        print(f"\n\nLog returns (using max window):\n\n{LogReturnsMax.iloc[-1]}")
        print(f"\n\nLog returns (using time additivity):\n\n{TimeAdditivity}")


    While log returns are additive across time, they are not additive across the portfolio assets.
    For additivity across portfolio components, simple returns must be used.


`Sources`:
  * https://www.investopedia.com/articles/investing/102014/lognormal-and-normal-distribution.asp
  * https://quantivity.wordpress.com/2011/02/21/why-log-returns/

