import pandas
import numpy
from scipy import optimize


def evalCouponBond(ytm, freq, T, face, coupon):
    """
    Parameters
    ----------
    ytm: number
      yield to maturity / annual discount rate;
      the expected rate of return if every coupon payment was
      invested at a fixed interest rate until the bond matures

    freq: number
      number of payment time per year, i.e. semi-annual -> 2

    T: number
      time to maturity, in years

    face: number
      face value / amt to be paid in full by maturity

    coupon: number
      annual coupon rate

    Returns
    -------
    valuation : number
      The valuation of a coupon bond
    """
    fval = calcFaceValues(ytm, freq, T, face)
    coup = calcCoupons(ytm, freq, T, face, coupon)
    cash = fval + coup
    return cash.sum()


def evalZeroCouponBond(ytm, freq, T, face):
    cash = calcFaceValues(ytm, freq, T, face)
    return cash.sum()


def calcCoupons(ytm, freq, T, face, coupon):
    """ present value of coupon payments """
    pptm = calcPptm(freq, T)
    crpp = calcCrpp(coupon, freq)
    cppp = calcCppp(crpp, face)
    time = getPeriods(pptm)
    return calcPv(ytm, freq, time.values, cppp)


def calcFaceValues(ytm, freq, T, face):
    """ present value of final zero coupon payment """
    pptm = calcPptm(freq, T)
    time = getPeriods(pptm)
    mask = time == time.max()
    return mask * calcPv(ytm, freq, time.values, face)


def getPeriods(pptm):
    pptm_int = int(pptm)
    if pptm_int != pptm:
        raise TypeError(pptm, pptm_int)
    time = numpy.ones(pptm_int).cumsum()
    return pandas.Series(time, index=time)


def calcCrpp(coupon, freq):
    """ coupon rate per period """
    return coupon / freq


def calcCppp(crpp, face):
    """ coupon payments per period """
    return crpp * face


def calcPptm(freq, T):
    """ payment time to maturity """
    return freq * T


def calcPv(r, freq, periods, value):
    """
    Parameters
    ----------
    r:
      discount rate;
      the expected rate of return if every coupon payment was
      invested at a fixed interest rate until the bond matures

    freq:
      frequency

    periods:
      periods to maturity

    value:
      future value / value at maturity

    Returns
    -------
    present_value
    """
    tmp = (1 + r / freq) ** periods
    return value / tmp


def calcDuration(ytm, freq, T, face, coupon):
    """
    Calculates Macaulay Duration, which is defined as the
    weighted average term to maturity of the cash flows of a bond.
    Duration measures how long it takes, in years, for an investor
    to be repaid the bond’s price by the bond’s total cash flows.

    Parameters
    ----------
    ytm: number
      yield to maturity / annual discount rate;
      the expected rate of return if every coupon payment was
      invested at a fixed interest rate until the bond matures

    freq: number
      compounding periods per year, i.e. semi-annual -> 2

    T: number
      time to maturity, in years

    face: number
      face value / amt to be paid in full by maturity

    coupon: number
      annual coupon rate

    Returns
    -------
    duration : number
      The duration of a bond, in years
    """

    pptm = calcPptm(freq, T)
    time = getPeriods(pptm)

    fval = calcFaceValues(ytm, freq, T, face)
    coup = calcCoupons(ytm, freq, T, face, coupon)
    cash = coup + fval

    tmp = (time * cash).sum() / cash.sum()
    return tmp / freq


def calcYtm(price, face, T, coupon, freq, guess=0.05):
    """ Calculates the approximate YTM """
    fun = lambda y: evalCouponBond(y, freq, T, face, coupon) - price
    return optimize.newton(fun, guess)


def calcModDuration(duration, freq, ytm):
    """
    Calculates the modified duration:
    - first derivative of price w.r.t. yield
    """
    tmp = 1 + (ytm / freq)
    return duration / tmp


def calcConvexity(price, face, T, coupon, freq, dy):
    """
    Calculates the modified duration:
    - first derivative of the modified duration
    """
    ytm = calcYtm(price, face, T, coupon, freq)

    inc = evalCouponBond(ytm + dy, freq, T, face, coupon)
    dec = evalCouponBond(ytm - dy, freq, T, face, coupon)

    c = inc + dec - 2 * price
    c /= price * dy ** 2
    return c


def calcPriceChange(price, mod_d, c, dy):
    tmp = 1/2 * price * c * dy**2
    return tmp - (price * mod_d * dy)


def calcDurationSensitivity(ytm, freq, T, face, coupon, rate_range):
    price = evalCouponBond(ytm, freq, T, face, coupon)
    d = calcDuration(ytm, freq, T, face, coupon)
    mod_d = calcModDuration(d, freq, ytm)
    dy_vector = getDyVector(rate_range)
    changes = dy_vector * mod_d * price
    return pandas.Series(price - changes, index=dy_vector + ytm)


def calcConvexitySensitivity(ytm, freq, T, face, coupon, dy, rate_range):
    price = evalCouponBond(ytm, freq, T, face, coupon)
    d = calcDuration(ytm, freq, T, face, coupon)
    mod_d = calcModDuration(d, freq, ytm)
    c = calcConvexity(price, face, T, coupon, freq, dy)
    dy_vector = getDyVector(rate_range)
    changes = calcPriceChange(price, mod_d, c, dy_vector)
    return pandas.Series(changes + price, index=dy_vector + ytm)


def getDyVector(rate_range, multiplier=100):
    rate_range = int(rate_range * multiplier)
    vector = numpy.ones(rate_range * 2 + 1).cumsum() - (rate_range + 1)
    return vector / multiplier
