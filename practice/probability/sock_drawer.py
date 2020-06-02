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
  1. Let's define the probability of drawing red after the first draw as

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

      the probability of drawing 2 consecutive reds may be represented as

      .. math::

        P(red_2|red_1) = \\frac{\\binom{N_{red}}{2}}{\\binom{N_{Total}}{2}},

      or more generally, the probability of drawing X consecutive reds is

      .. math::

        P(red_X|red_{(X-1)...1}) = \\frac{\\binom{N_{red}}{X}}
                                       {\\binom{N_{Total}}{X}},

      .. math::

        = \\frac{\\binom{N_{red}}{X}}{\\binom{N_{red} + N_{black}}{X}}

  In Code:

"""
import pandas
import numpy
from scipy.special import comb


def prob(n_red, n_black, x):
    """ the probability of drawing X consecutive reds """
    n_total = n_red + n_black
    pr = comb(n_red, x)
    pr /= comb(n_total, x)
    return pr


def createCombos(n_combos: int, names: list) -> dict:
    """ utility for creating combos of integers """
    n = len(names)
    range_ = range(1, n_combos + 1)
    mesh = numpy.meshgrid(*(n * [range_]))
    combos = numpy.array(mesh).reshape(n, -1)
    return dict(zip(names, combos))


class Solution:

    @staticmethod
    def a(target_pr):
        """(a) How small can the number of socks in the drawer be?"""

        combos = createCombos(
            n_combos=5,
            names=['n_red', 'n_black'], )

        DF = pandas.DataFrame(combos)
        pr = prob(**DF, x=2)

        isSolution = (pr == target_pr)

        return DF[isSolution]

    @staticmethod
    def b(target_pr):
        """(b) How small if the number of black socks is even?"""

        combos = createCombos(
            n_combos=30,
            names=['n_red', 'n_black'], )

        DF = pandas.DataFrame(combos)
        pr = prob(**DF, x=2)

        isSolution = (pr == target_pr)
        blackIsEven = DF['n_black'] % 2 == 0

        return DF[isSolution & blackIsEven]
# %%


def main():
    from practice.util.driver import Driver

    target_pr = 1 / 2

    for question in ['a', 'b']:
        Driver(Solution, question).run(target_pr=target_pr)


if __name__ == '__main__':
    main()
