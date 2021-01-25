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

The following functions are used to assist in the
present valuation of a bond:

    .. autofunction:: practice.finance.bond.calcCoupons

    .. autofunction:: practice.finance.bond.calcFaceValue

Example
********

    .. jupyter-execute::

        import pandas

        ytm = 0.03
        pppy = 2
        y = 2
        face = 1000
        coupon_rate = 0.05

        coup = bond.calcCoupons(ytm, pppy, y, face, coupon_rate)
        fval = bond.calcFaceValue(ytm, pppy, y, face)

        PresentValues = pandas.DataFrame({
            f'coup({ytm},{face})' : coup,
            f'face({ytm},{face})' : fval, })

        total_coup = bond.evalCoupon(ytm, pppy, y, face, coupon_rate)
        total_zero = bond.evalZeroCoupon(ytm, pppy, y, face)

        assert total_zero == fval.sum()
        assert total_coup == (fval + coup).sum()

        print(PresentValues)
        print(f"\nThe present value of the bond is: {PresentValues.sum().sum()}")


    .. image:: ../../images/finance/BondPresentValues.png
       :align: center


Duration
----------------

Duration may be thought of as the weighted average number of years
an investor must maintain a position in a bond until the present
value of the bond's cash flows equals the amount paid for the bond.


Compounding Example
*******************
Assuming a $1,000 face value bond that pays a 6% coupon and matures
in 3 years with an interest rates of 6% per year with semi-annual
compounding, the duration would be calculated as follows:

    .. jupyter-execute::

        ytm = 0.06
        pppy = 2
        y = 3
        face = 100
        coupon_rate = 0.06

        d = bond.calcDuration(ytm, pppy, y, face, coupon_rate)

        print(f"""
            The duration is {d:.2f} years,
            which is less than the time to maturity
            of {y} years.
            In other words, it takes {d:.2f} years to
            recoup the true cost of the bond. """)


Modified Duration
*******************

Assuming a three-year bond with a face value of $100 that
pays a 10% coupon semi-annually and has a yield to maturity
of 6%, the duration and modified duration may be calculated
as follows:

    .. jupyter-execute::

        pppy = 2
        ytm = 0.06
        y = 3
        face = 100
        coupon_rate = 0.10

        d = bond.calcDuration(ytm, pppy, y, face, coupon_rate)
        mod_d = bond.calcModDuration(d, pppy, ytm)

        print(f"""
            In this case, if, say, interest rates were to rise and ultimately
            increase the YTM from {ytm*100}% to {ytm*100+1}%, then the bond's
            value should fall by {mod_d:.2f}%.\n
            Similarly, if the YTM were to fall from {ytm*100}% to {ytm*100-1}%,
            then the bond's price should rise by {mod_d:.2f}%.""")



Convexity
----------------

Convexity builds on the concept of duration by measuring the
sensitivity of the duration of a bond as yields change.

While the modified duration calculates a bond's price change in
response to a 1% rate change, convexity calculates the
acceleration of this price change in response to
the corresponding rate change.


