import pandas
import numpy


def evalCoupon(ytm, pppy, y, face, coupon_rate):
    """
    Parameters
    ----------
    ytm: number
      yield to maturity / annual discount rate;
      the expected rate of return if every coupon payment was
      invested at a fixed interest rate until the bond matures

    pppy: number
      number of payment time per year, i.e. semi-annual -> 2

    y: number
      time to maturity, in years

    face: number
      face value / amt to be paid in full by maturity

    coupon_rate: number
      annual coupon rate

    Returns
    -------
    valulation : number
      The valuation of a coupon bond
    """
    fval = calcFaceValue(ytm, pppy, y, face)
    coup = calcCoupons(ytm, pppy, y, face, coupon_rate)
    cash = fval + coup
    return cash.sum()


def evalZeroCoupon(ytm, pppy, y, face):
    """
    Parameters
    ----------
    ytm: number
      yield to maturity / annual discount rate;
      the expected rate of return if every coupon payment was
      invested at a fixed interest rate until the bond matures

    pppy: number
      number of payment time per year, i.e. semi-annual -> 2

    y: number
      time to maturity, in years

    face: number
      face value / amt to be paid in full by maturity

    Returns
    -------
    valuation : number
      The valuation of a zero-coupon bond
    """
    cash = calcFaceValue(ytm, pppy, y, face)
    return cash.sum()


def calcCoupons(ytm, pppy, y, face, coupon_rate):
    """ present value of coupon payments """
    pptm = calcPptm(pppy, y)
    crpp = calcCrpp(coupon_rate, pppy)
    cppp = calcCppp(crpp, face)
    time = getPeriods(pptm)
    return presentValue(ytm, time, cppp)


def calcFaceValue(ytm, pppy, y, face):
    """ present value of final zero coupon payment """
    pptm = calcPptm(pppy, y)
    time = getPeriods(pptm)
    inScope = (time == time.max())
    return inScope * presentValue(ytm, time, face)


def getPeriods(pptm):
    time = numpy.ones(pptm).cumsum()
    return pandas.Series(time, index=time)


def calcCrpp(coupon_rate, pppy):
    """ coupon rate per period """
    return coupon_rate / pppy


def calcCppp(crpp, face):
    """ coupon payments per period """
    return crpp * face


def calcPptm(pppy, y):
    """ payment time to maturity """
    return pppy * y


def presentValue(rate, pptm, value):
    """
    Parameters
    ----------
    rate:
      discount rate;
      the expected rate of return if every coupon payment was
      invested at a fixed interest rate until the bond matures

    pptm:
      payment time to maturity

    value:
      future value / value at maturity

    Returns
    -------
    present_value
    """
    tmp = (1 + rate) ** pptm
    return value / tmp


def calcDuration(ytm, pppy, y, face, coupon_rate):
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

    k: number
      compounding periods per year, i.e. semi-annual -> 2

    y: number
      time to maturity, in years

    face: number
      face value / amt to be paid in full by maturity

    coupon_rate: number
      annual coupon rate

    Returns
    -------
    duration : number
      The duration of a bond, in years
    """

    ytm_pp = ytm / pppy

    pptm = calcPptm(pppy, y)
    time = getPeriods(pptm)

    fval = calcFaceValue(ytm_pp, pppy, y, face)
    coup = calcCoupons(ytm_pp, pppy, y, face, coupon_rate)
    cash = coup + fval

    tmp = (time * cash).sum() / cash.sum()
    return tmp / pppy


def calcModDuration(duration, pppy, ytm):
    tmp = 1 + (ytm / pppy)
    return duration / tmp
