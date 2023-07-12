from practice.frameworks.rows import Rows
from practice.frameworks import exception as ex


class Table:

    @classmethod
    def fromDF(cls, DF, columns):
        arrays = [ DF[c].values.tolist() for c in DF ]
        return cls.fromArrays(arrays, columns)

    @classmethod
    def fromArrays(cls, arrays, columns):
        data = dict( zip(columns, arrays) )
        return cls.fromDict(data, columns)

    @classmethod
    def fromDict(cls, data, columns):
        rows = Rows.fromDict(data)
        return cls.fromRows(rows, columns)

    @classmethod
    def fromList(cls, data, columns):
        rows = Rows.fromList(data)
        return cls.fromRows(rows, columns)

    @classmethod
    def fromRows(cls, rows, columns):
        return cls(rows, columns)

    def __init__(self, rows, columns):
        ex.ObjectIsEmptyOrNone.raiseIf( columns )
        columns = columns if isinstance(columns, (list, tuple)) else [columns]
        self.validate(rows, columns)
        self.rows    = rows
        self.ncols   = rows.ncols
        self.nrows   = rows.nrows
        self.columns = columns

    @classmethod
    def validate(cls, rows, columns):
        ex.MustBeUnique.raiseIf( columns )
        ex.MustBeTheSame( rows.ncols, len(columns) )

    def asNative(self):
        arrays = self.asRows().asArrays()
        return dict(zip(self.columns, arrays))

    def asRows(self):
        values = self.rows.asNative()
        return Rows.fromList(values)

    def asIterator(self):
        from practice.frameworks.iterator import Iterator
        return Iterator.fromTable(self)

    def asDF(self):
        import pandas as pd
        return pd.DataFrame(self.asNative())

    def sortViaDF(self, *a, **kw):
        """ returns a sorted table based on parameters specified """
        sorted = self.asDF().sort_values(*a, **kw)
        return self.fromDF(sorted, self.columns)
