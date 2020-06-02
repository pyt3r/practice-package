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

.. _binomial coefficient (combination): https://en.wikipedia.org/wiki/Combination

      .. math::

        \\binom{n}{k} = \\frac{n(n-1) ... (n-k+1)}{k(k-1) ... 1},

      the probability of drawing 2 consecutive reds may be generalized as,

      .. math::

        P(red_2|red_1) = \\frac{\\binom{N_{red}}{2}}{\\binom{N_{Total}}{2}},

      and ultimately,

        = \\frac{\\binom{N_{red}}{2}}{\\binom{N_{red} + N_{black}}{2}}

  In Code:


"""


class Solution:

    @staticmethod
    def a(n_red: int, n_black: int, n_draws: int) -> float:
        from itertools import combinations
        n_total = n_red + n_black
        pr = combinations(n_red, n_draws)
        pr /= combinations(n_total, n_draws)
        return pr
# %%
