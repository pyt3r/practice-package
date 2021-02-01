Bond Analysis
==============

.. toctree::
   :maxdepth: 1


The bond tools presented on this page take the form of ``python``
functions and may be imported as follows:

    .. jupyter-execute::

        import practice.finance.bond as bond


Present Valuation
------------------

The following function is used to calculate the present value
of a bond:

    .. autofunction:: practice.finance.bond.calcBondPrice


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

        bond_price = bond.calcBondPrice(ytm, freq, T, face, coupon)

        assert bond_price == (fval + coup).sum()

        price = PresentValues.sum().sum()
        print(f"\nThe present value of the bond is: ${price:.2f}\n""")
        print(PresentValues)

    .. image:: ../../images/finance/BondPresentValues.png
       :align: center

To back out the bond's yield, given the price, the following
function may be invoked:

    .. jupyter-execute::

        approxYtm = bond.calcYtm(price, face, T, coupon, freq)
        print(f"The approximate ytm is: {approxYtm*100:.2f}%""")


Duration
----------------

Duration may be thought of as the weighted average number of years
an investor must maintain a position in a bond until the present
value of the bond's cash flows equals the amount paid for the bond.
At a glance, the figure represents a bond's interest rate risk.

The Modified Duration is the first derivative of a bond's price with
respect to yield and may be computed as a function of Duration:

    .. jupyter-execute::

        d = bond.calcDuration(ytm, freq, T, face, coupon)
        mod_d = bond.calcModDuration(d, freq, ytm)

        print(f"""
          It takes {d:.3f} years to recoup the cost of the bond.

          The modified duration is {mod_d:.3f}, and therefore, a 1%
          change in rates would lead to an approximate change in...

          - duration of : {d-mod_d:.3f} years

          - price of    : {0.01*mod_d*100:.3f}%, or ${0.01*mod_d*price:.3f}
        """)


Convexity
----------------

Convexity builds on the concept of duration by measuring the
sensitivity of a bond's duration as interest rates change.

While the Modified Duration calculates a bond's price change in
response to a 1% rate change, convexity calculates the acceleration
of this price change in response to the corresponding rate change.

In short, Convexity is the first derivative of the modified duration
(or the second derivative of the price with respect to yield) and
may also be used to estimate price changes:

    .. jupyter-execute::

        dy = 0.01

        c = bond.calcConvexity(price, face, T, coupon, freq, dy)
        change_inc = bond.calcPriceChange(price, mod_d, c, dy)
        change_dec = bond.calcPriceChange(price, mod_d, c, -dy)

        print(f"""
          The convexity is {c:.3f}, and therefore...

           A 1% increase in rates would lead to a price change of:
            -${abs(change_inc):.3f}

           A 1% decrease in rates would lead to a price change of:
            +${change_dec:.3f}
        """)

Note that the Modified Duration is used to linearly estimate the price,
whereas Convexity is used to capture a more accurate estimate, as it takes
into account the curvature that the bond's price exhibits at different
interest rates:


    .. jupyter-execute::

        rate_range = 0.03

        cSensitivity = bond.calcConvexitySensitivity(ytm, freq, T, face, coupon, dy, rate_range)
        dSensitivity = bond.calcDurationSensitivity(ytm, freq, T, face, coupon, rate_range)

        DF = pandas.DataFrame({
            'using Convexity': cSensitivity,
            '$Change(C)': cSensitivity.diff(-1),
            'using Duration': dSensitivity,
            '$Change(D)': dSensitivity.diff(-1), })

        print(DF)


    .. image:: ../../images/finance/BondSensitivity.png
       :align: center
