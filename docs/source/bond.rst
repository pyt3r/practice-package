Bond Pricing
=============================

.. toctree::
   :maxdepth: 1


The bond pricing tools presented on this page take the form of
``python`` functions and may be imported as follows:

    .. jupyter-execute::

        import practice.finance.bond as bond


Many of the definitions and examples presented this page were
leveraged from the following sources:

    - https://www.investopedia.com/terms/b/bond-valuation.asp
    - https://www.investopedia.com/terms/d/duration.asp
    - https://www.investopedia.com/terms/m/macaulayduration.asp
    - https://www.investopedia.com/terms/m/modifiedduration.asp
    - https://www.investopedia.com/terms/c/convexity.asp


Present Valuation
------------------

The following function is used to calculate the present value
of a bond:

    .. autofunction:: practice.finance.bond.evalCouponBond


To help demonstrate the concept of present valuation, the following
helper functions are used in the example below:

    .. autofunction:: practice.finance.bond.calcCoupons

    .. autofunction:: practice.finance.bond.calcFaceValue


Example
********

    .. jupyter-execute::

        import pandas

        ytm = 0.06
        freq = 2
        T = 2
        face = 100
        coupon = 0.05

        coup = bond.calcCoupons(ytm, freq, T, face, coupon)
        fval = bond.calcFaceValue(ytm, freq, T, face)

        PresentValues = pandas.DataFrame({
            f'coup({ytm},{face})' : coup,
            f'face({ytm},{face})' : fval, })

        total_coup = bond.evalCouponBond(ytm, freq, T, face, coupon)
        total_zero = bond.evalZeroCouponBond(ytm, freq, T, face)

        assert total_zero == fval.sum()
        assert total_coup == (fval + coup).sum()

        price = PresentValues.sum().sum()
        print(PresentValues)
        print(f"\nThe present value of the bond is:${price:.2f}""")

    .. image:: ../../images/finance/BondPresentValues.png
       :align: center

To back out the yield, given the price, the following
function may be invoked:

    .. jupyter-execute::

        approxYtm = bond.calcYtm(price, face, T, coupon, freq)
        print(f"The approximate ytm is: {approxYtm*100:.2f}%""")



Duration
----------------

Duration may be thought of as the weighted average number of years
an investor must maintain a position in a bond until the present
value of the bond's cash flows equals the amount paid for the bond.

As an example, the duration for a $1,000 face value bond that pays
a 6% coupon and matures in 3 years with an interest rate of 6% per
year, compounded semi-annually would be calculated as follows:

    .. jupyter-execute::

        d = bond.calcDuration(ytm, freq, T, face, coupon)
        print(f"It takes {d:.2f} years to recoup the cost of the bond.")


Modified Duration
------------------

The modified duration is the first derivative of price with respect
to yield.

    .. jupyter-execute::

        mod_d = bond.calcModDuration(d, freq, ytm)

        print(f"""
          The modified duration is {mod_d:.2f}, which implies that
          a 1% change in yield leads to a {mod_d:.2f}% in price.""")


Convexity
----------------

Convexity builds on the concept of duration by measuring the
sensitivity of the duration of a bond as yields change.

While the modified duration calculates a bond's price change in
response to a 1% rate change, convexity calculates the
acceleration of this price change in response to the corresponding
rate change, and is in effect, the derivative of the modified
duration.

    .. jupyter-execute::

        dy = 0.01

        c = bond.calcConvexity(price, face, T, coupon, freq, dy)

        print(f"""
          The convexity is {c:.2f}, which implies that
          A {dy*100:.2f}% change in yield leads to a modified
          duration change of {c*dy*100:.2f}.""")


When working with portfolio of bonds, it is sometimes easier
to calculate the duration and convexity of the portfolio,
and then estimate the price change and risk at the portfolio-level
in lieu of doing so for each bond in the portfolio.
