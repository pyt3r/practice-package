from practice.frameworks.table import Table


class Iterator:

    @classmethod
    def fromArrays(cls, one, another, *others):
        arrays = (one, another) + others
        data   = {i: array for i, array in enumerate(arrays)}
        return cls.fromDict(data)

    @classmethod
    def fromDict(cls, data):
        table = Table.createWithoutSchema(data)
        return cls.fromTable(table)

    @classmethod
    def fromTable(cls, table):
        return cls(table)

    def __init__(self, table):
        self.table     = table
        self.primaries = {k: Primary(v) for k, v in table.asNative().items()}
        self.length    = table.length
        self.setViewOrder(self.getKeys())

    def setViewOrder(self, order):
        assert all(k in self.getKeys() for k in order)
        self._order = order

    def getViewOrder(self):
        return self._order

    def getKeys(self):
        return list(self.primaries.keys())

    def reset(self):
        self._run(Primary.reset)

    def asNative(self):
        keys = self.getViewOrder()
        vals = self._run(Primary.asNative)
        return dict(zip(keys, vals))

    def getPrimary(self, key):
        array = self.primaries[key].asNative()
        return Primary(array)

    def asTable(self):
        return Table.createWithoutSchema(self.asNative())

    def __iter__(self):
        self.reset()
        while self.isNextable():
            yield next(self)
        self.reset()

    def __next__(self):
        return self.getNext()

    def getNext(self):
        return self._run(Primary.getNext)

    def peekNext(self):
        return self._run(Primary.peekNext)

    def getPrev(self):
        return self._run(Primary.getPrev)

    def getSelected(self, i):
        return self._run(Primary.getSelected, i)

    def isNextable(self):
        return all(self._run(Primary.isNextable))

    def _run(self, func, *a, **kw):
        results = {k: func(primary, *a, **kw) for k, primary in self.primaries.items()}
        return tuple(results[k] for k in self.getViewOrder())


class Primary:
    def __init__(self, array):
        self._reset(array)

    def _reset(self, array):
        self.array = array
        self.length = len(array)
        self.cursor = 0

    def reset(self):
        self._reset(self.array)

    def asNative(self):
        return self.array

    def getNext(self):
        return next(self)

    def __iter__(self):
        self.reset()
        while self.isNextable():
            yield next(self)
        self.reset()

    def __next__(self):
        cursor = self.cursor
        if not self.isNextable():
            raise StopIteration
        self.cursor += 1
        return self.array[cursor]

    def peekNext(self):
        if self.isNextable():
            return self.array[self.cursor]

    def getPrev(self):
        cursor = self.cursor - 2
        if cursor > 2:
            raise StopIteration
        self.cursor = cursor
        return next(self)

    def getSelected(self, i):
        valid = 0 <= i < self.length
        if not valid:
            raise ValueError(f"i={i} not in range=[0, {self.length})")
        self.reset()
        self.cursor = i
        return next(self)

    def isNextable(self):
        return self.cursor < self.length