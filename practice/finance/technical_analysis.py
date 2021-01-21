from numpy import sign


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
    x = s1 - s2
    x = x*0 + sign(x)
    return x.shift(lag)


def stochOscillator(metric, window):
    low = metric.rolling(window).min()
    high = metric.rolling(window).max()
    tmp = metric - low
    tmp /= high - low
    return tmp


def rocOscillator(metric, n):
    return metric.diff(n) / metric


def rsiSma(metric, window):
    return rsiBase(metric, window, funcMA=simpleMA)


def rsiEma(metric, window):
    return rsiBase(metric, window, funcMA=expMA)


def rsiBase(metric, window, funcMA):
    diff = metric.diff()
    signs = sign(diff)
    isPositive = (signs + 1) / 2
    isNegative = (signs - 1).abs() / 2

    gain = isPositive * diff
    loss = isNegative * diff.abs()

    avgGain = funcMA(gain, window)
    avgLoss = funcMA(loss, window)

    rsi = avgGain / avgLoss
    rsi = 100 / (1 + rsi)
    return 100 - rsi


def mfi(high, low, close, volume, window):
    tmp = mfiRatio(high, low, close, volume, window)
    tmp += 1
    return 100 - (100 / tmp)


def mfiRatio(high, low, close, volume, window):
    price = typicalPrice(high, low, close)
    mf = rawMoneyFlow(high, low, close, volume)

    diff = price.diff()
    signs = sign(diff)
    isPositive = (signs + 1) / 2
    isNegative = (signs - 1).abs() / 2

    mf_positive = mf * isPositive
    mf_negative = mf * isNegative

    ratio  = mf_positive.rolling(window).sum()
    ratio /= mf_negative.rolling(window).sum()
    return ratio


def rawMoneyFlow(high, low, close, volume):
    return typicalPrice(high, low, close) * volume


def typicalPrice(high, low, close):
    return (high + low + close) / 3
