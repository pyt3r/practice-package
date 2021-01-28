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

    .. autofunction:: practice.finance.bond.calcFaceValues


Example
********

    .. jupyter-execute::

        import pandas

        ytm = 0.06
        freq = 2
        T = 2
        face = 100
        coupon = 0.05

        coup = bond.calcCoupons(ytm, freq, T, face, coupon).squeeze()
        fval = bond.calcFaceValues(ytm, freq, T, face).squeeze()

        PresentValues = pandas.DataFrame({
            f'coup({ytm},{face})' : coup,
            f'face({ytm},{face})' : fval, })

        total_coup = bond.evalCouponBond(ytm, freq, T, face, coupon)
        total_zero = bond.evalZeroCouponBond(ytm, freq, T, face)

        assert total_zero[ytm] == fval.sum()
        assert total_coup[ytm] == (fval + coup).sum()

        price = PresentValues.sum().sum()
        print(f"\nThe present value of the bond is: ${price:.2f}\n""")
        print(PresentValues)

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
The duration of a zero-coupon bond, for example, is equal to the
bond's time to maturity.

The Modified Duration is the first derivative of price with respect
to yield; in essence, the linear estimate of the bond's percent change
in price per percent change in interest rate.

    .. jupyter-execute::

        d = bond.calcDuration(ytm, freq, T, face, coupon)
        mod_d = bond.calcModDuration(d, freq, ytm)

        print(f"""
          It takes {d:.2f} years to recoup the cost of the bond.

          The modified duration is {mod_d:.2f}, and therefore, a 1%
          change in rates would lead to an approximate change in...

          - duration of : {d-mod_d:.2f} years

          - price of    : {0.01*mod_d*100:.2f}%, or ${0.01*mod_d*price:.2f}
        """)

Convexity
----------------

Convexity builds on the concept of duration by measuring the
sensitivity of a bond's duration as interest rates change.

While the modified duration calculates a bond's price change in
response to a 1% rate change, convexity calculates the acceleration
of this price change in response to the corresponding rate change;
in short, convexity is the first derivative of the modified duration
(or the second derivative of the price with respect to yield).

    .. jupyter-execute::

        dy = 0.01

        c = bond.calcConvexity(price, face, T, coupon, freq, dy)



Note that the Modified Duration is used to linearly estimate, the price,
whereas Convexity captures the curvature the bond's price exhibits at
different interest rates:


    .. jupyter-execute::

        # placeholder


When working with a portfolio of bonds, it is sometimes easier
to calculate the duration and convexity of the portfolio,
and then estimate the price change and risk at the portfolio-level
in lieu of doing so for each bond in the portfolio.
