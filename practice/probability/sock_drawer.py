"""
Sock Drawer
===============

Excerpted from
`Fifty Challenging Problems in Probability with Solutions`
by Frederick Mosteller


Problem:
  A drawer contains red socks and black socks.
  When two socks are drawn at random, the
  probability that both are red is 1/2.

    (a) How small can the number of socks in the drawer be?

    (b) How small if the number of black socks is even?

Solution:
  1. Let's define the probability of drawing red after 1 draw as

      .. math:: P(red_1) = \\frac{N_{red}}{N_{total}},

      where

      .. math:: N_{total} = N_{red} + N_{black}


  2. Let's define the probability of drawing 2 consecutive reds as

      .. math::

        P(red_2|red_1) = P(red_1) *
          \\frac{N_{red} - 1}{N_{total} - 1},

      which can be expanded to

      .. math::

        = \\frac{N_{red}}{N_{total}} *
          \\frac{N_{red} - 1}{N_{total} - 1}


  3. Using the `binomial coefficient (combination)`_ equation,

.. _binomial coefficient (combination):
    https://en.wikipedia.org/wiki/Combination

      .. math::

        \\binom{n}{k} = \\frac{n(n-1) ... (n-k+1)}{k(k-1) ... 1},

      the probability of drawing 2 consecutive reds may be generalized as,

      .. math::

        P(red_2|red_1) = \\frac{\\binom{N_{red}}{2}}{\\binom{N_{Total}}{2}},

      and ultimately,

      .. math::

        = \\frac{\\binom{N_{red}}{2}}{\\binom{N_{red} + N_{black}}{2}}

  In Code:

"""
import pandas
import numpy
from scipy.special import comb


class Solution:

    @staticmethod
    def a(n_red: numpy.array,
          n_black: numpy.array,
          n_draws: int) -> numpy.array:
        n_total = n_red + n_black
        pr = comb(n_red, n_draws)
        pr /= comb(n_total, n_draws)
        return pr
# %%


def createRedBlackCombos(n_combos: int) -> dict:
    range_ = range(1, n_combos + 1)
    meshgrid = numpy.meshgrid(range_, range_)
    combos = numpy.array(meshgrid).reshape(2, -1)
    return dict(zip(['n_red', 'n_black'], combos))


def main():
    from practice.util.driver import Driver

    n_combos = 5
    kwargs = createRedBlackCombos(n_combos)

    driver = Driver(Solution, 'a')
    result = driver.run(**kwargs, n_draws=2)

    Result = pandas.DataFrame(kwargs)
    print("\n\n >> And the answer is...\n")
    print(Result[result == 0.5])


if __name__ == '__main__':
    main()
