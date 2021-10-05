from numpy import sqrt
from numpy import log


def calcVolatity(metric, window):
    """ Calculates the generalized volatility. """
    log_returns = logReturns(metric, window)
    return log_returns.rolling(window).std() * sqrt(window)


def logReturns(metric, window):
    return log(metric).diff(window)


def simpleReturns(metric, window):
    return metric.pct_change(window)


def beta(asset_returns, market_returns, window):
    """ Calculates the beta, or market risk premium """
    rolling = market_returns.rolling(window)
    return rolling.cov(asset_returns) / rolling.var()
