class Table:

    @classmethod
    def createFromRows(cls, rows, columns):
        tmpCols    = [i for i, _ in enumerate(rows)]
        tmpTable   = cls.createFromVals(rows, tmpCols)
        transposed = tmpTable.transpose()
        native     = transposed.asNative()
        return cls.createFromVals(native.values(), columns)

    @classmethod
    def createFromVals(cls, vals, columns):
        ix   = min(len(vals), len(columns))
        data = dict(zip(columns[:ix], vals))
        return cls.createWithSchema(data, columns)

    @classmethod
    def createFromDF(cls, DF, columns):
        data = {c: DF[c].values.tolist() for c in DF}
        return cls.createWithSchema(data, columns)

    @classmethod
    def createFromArrays(cls, one, *others):
        arrays = (one,) + others
        return cls.createWithoutSchema({i: arr for i, arr in enumerate(arrays)})

    @classmethod
    def createWithoutSchema(cls, data):
        return cls.createWithSchema(data, list(data.keys()))

    @classmethod
    def createWithSchema(cls, data, columns):
        return cls(data, columns)

    def __init__(self, data, columns):
        assert columns
        columns = columns if isinstance(columns, (list, tuple)) else [columns]
        self.validate(data, columns)
        self.data    = data
        self.columns = columns
        self.length  = len(self.data[self.columns[0]])

    @classmethod
    def validate(cls, data, columns):
        cls._validateKeys(data, columns)
        cls._validateVals(data)

    @staticmethod
    def _validateKeys(data, columns):
        assert len(columns) == len(set(columns))
        assert len(columns) > 0
        a = set(data.keys())
        b = set(columns)
        assert a ^ b == set()

    @staticmethod
    def _validateVals(data):
        vals = list(data.values())
        length = set(len(v) for v in vals)
        assert len(length) == 1

    def asNative(self):
        return self.data

    def asIterator(self):
        from practice.frameworks.iterator import Iterator
        return Iterator.fromDict(self.asNative())

    def transpose(self):
        data = {i: list(vals) for i, vals in enumerate(self.asIterator())}
        cols = list(data.keys())
        return self.createWithSchema(data, cols)

    def asDF(self):
        import pandas as pd
        return pd.DataFrame(self.asNative())

    def sort(self, *a, **kw):
        """ returns a sorted table based on parameters specified """
        sorted = self.asDF().sort_values(*a, **kw)
        return self.createFromDF(sorted, self.columns)
