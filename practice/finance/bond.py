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
    fval = calcFaceValue(ytm, freq, T, face)
    coup = calcCoupons(ytm, freq, T, face, coupon)
    cash = fval + coup

    return cash.sum()


def evalZeroCouponBond(ytm, freq, T, face):
    cash = calcFaceValue(ytm, freq, T, face)
    return cash.sum()


def calcCoupons(ytm, freq, T, face, coupon):
    """ present value of coupon payments """
    pptm = calcPptm(freq, T)
    crpp = calcCrpp(coupon, freq)
    cppp = calcCppp(crpp, face)
    time = getPeriods(pptm)
    return presentValue(ytm, freq, time, cppp)


def calcFaceValue(ytm, freq, T, face):
    """ present value of final zero coupon payment """
    pptm = calcPptm(freq, T)
    time = getPeriods(pptm)
    inScope = (time == time.max())
    return inScope * presentValue(ytm, freq, time, face)


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


def presentValue(rate, freq, pptm, value):
    """
    Parameters
    ----------
    rate:
      discount rate;
      the expected rate of return if every coupon payment was
      invested at a fixed interest rate until the bond matures

    freq:
      frequency

    pptm:
      payment time to maturity

    value:
      future value / value at maturity

    Returns
    -------
    present_value
    """
    tmp = (1 + rate / freq) ** pptm
    return value / tmp


def calcDuration(ytm, freq, T, face, coupon):
    """
    source: https://www.investopedia.com/terms/m/macaulayduration.asp

    Calculates Macaulay Duration, which is defined as the
    weighted average term to maturity of the cash flows of a bond.
    Duration measures how long it takes, in years, for an investor
    to be repaid the bond’s price by the bond’s total cash flows.

    At the same time, duration is a measure of sensitivity of a
    bond's or fixed income portfolio's price to changes in interest
    rates.

    In general, the higher the duration, the more a bond's price
    will drop as interest rates rise (and the greater the interest
    rate risk). As a general rule, for every 1% change in interest
    rates (increase or decrease), a bond’s price will change
    approximately 1% in the opposite direction, for every year of
    duration.

    If a bond has a duration of five years and interest rates increase
    1%, the bond’s price will drop by approximately 5% (1% X 5 years).
    Likewise, if interest rates fall by 1%, the same bond’s price
    will increase by about 5% (1% X 5 years).

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

    fval = calcFaceValue(ytm, freq, T, face)
    coup = calcCoupons(ytm, freq, T, face, coupon)
    cash = coup + fval

    tmp = (time * cash).sum() / cash.sum()
    return tmp / freq


def calcModDuration(duration, freq, ytm):
    tmp = 1 + (ytm / freq)
    return duration / tmp


def calcYtm(price, face, T, coupon, freq, guess=0.05):
    """ Calculates the approximate YTM """
    fun = lambda y: evalCouponBond(y, freq, T, face, coupon) - price
    return optimize.newton(fun, guess)


def calcConvexity(price, face, T, coupon, freq, dy):
    """ Calculates the approximate convexity """
    ytm = calcYtm(price, face, T, coupon, freq)
    upper = evalCouponBond(ytm + dy, freq, T, face, coupon)
    lower = evalCouponBond(ytm - dy, freq, T, face, coupon)

    c = upper + lower - 2 * price
    c /= price * dy ** 2
    return c
