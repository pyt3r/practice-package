def simpleMA(metric, window):
    return metric.rolling(window).mean()


def expMA(metric, window):
    return metric.ewm(span=window, min_periods=window).mean()


def macd(metric, short_window, long_window):
    short = expMA(metric, short_window)
    long = expMA(metric, long_window)
    return short - long


def macdDistance(macd_metric, signal_metric):
    return macd_metric - signal_metric


def stDev(metric, window):
    return metric.rolling(window).std()


def bollUpper(metric, window, stdevs):
    return boll(metric, window, abs(stdevs))


def bollLower(metric, window, stdevs):
    return boll(metric, window, -abs(stdevs))


def boll(metric, window, stdevs):
    ma = simpleMA(metric, window)
    std = stDev(metric, window)
    return ma + (std * stdevs)


def crossover(s1, s2, lag):
    from numpy import sign
    x = s1 - s2
    x = x*0 + sign(x)
    return x.shift(lag)
