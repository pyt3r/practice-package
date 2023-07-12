import unittest
from practice.frameworks import exception as ex

class CommonCases(unittest.TestCase):

    def test_raiseIf_none(self):
        self.assertIsNone( ex.MustBeUnique.raiseIf([1,2,3]) )

    def test_raiseIf_invalid(self):
        exc = ex.MustBeUnique
        msg = "duplicates=\[2\]"
        with self.assertRaisesRegex(exc, msg):
            exc.raiseIf([1,2,3,2])


class AccumulatorCases(unittest.TestCase):

    def test_accumulate(self):
        one = ex.Accumulator()
        one.addEntry( ValueError(1) )
        one.addEntry( TypeError("int") )

        other = ex.Accumulator()
        other.addEntry( ValueError(2) )
        other.addEntry( TypeError("float") )

        one.extendEntries( other )

        msg = """[
            "ValueError( 1 )",
            "TypeError( int )",
            "ValueError( 2 )",
            "TypeError( float )"
        ]"""
        with self.assertRaisesRegex(ex.AccumulatedErrors, msg):
            one.raiseError() if one.hasErrors() else None

    def test_accumulate_lazy(self):

        exceptions = [
            ex.MustBeUnique([1,2,3,2]),
            ex.MustBeUnique([1,2,3]),
            ex.MustFullyIntersect([1,2,3,2], [2,3,4]),
            ex.MustFullyIntersect([1,2,3,2], [1,2,3]),
            ex.MustNotIntersect([1,2,3,2], [2,3,4]),
            ex.MustBeTheSameLengths([] ,[1], [1,2], []),
            ex.MustBeDifferentLengths([] ,[], [], []),
            ex.MustBeTheSame(*[1,1,1,1,1]),
            ex.MustBeTheSame(*[1,1,1,1,1, 2]),
        ]
        one = ex.Accumulator.fromList(exceptions)

        entries = one.getEntries()
        self.assertListEqual(entries, [
            'MustBeUnique( duplicates=[2] )',
            'MustFullyIntersect( outliers={1, 4} )',
            'MustNotIntersect( intersections={2, 3} )',
            'MustBeTheSameLengths( lengthsHistogram={0: 2, 1: 1, 2: 1} )',
            'MustBeDifferentLengths( lengthsHistogram={0: 4} )',
            'MustBeTheSame( histogram={1: 5, 2: 1} )'])


class AccumulatedIndexCases(unittest.TestCase):

    def test_intArray(self):
        data = ['1', 1.0, 1, 2, 2.0, '2', 3]
        one = ex.Accumulator.map( data, ex.TypeMismatch, int )
        self.assertListEqual( one.getIndices(), [0, 1, 4, 5] )

