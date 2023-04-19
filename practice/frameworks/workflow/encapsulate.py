
class WorkflowDF:
    """ wrapper around a dictionary to control access to columns """

    _order      = "order"
    _funcPath   = "funcPath"
    _inputKeys  = "inputKeys"
    _kwargs     = "kwargs"
    _outputKeys = "outputKeys"

    @classmethod
    def getColumns(cls):
        return [
            cls._order,
            cls._funcPath,
            cls._inputKeys,
            cls._kwargs,
            cls._outputKeys, ]

    def __init__(self, DF):
        self._validate(DF)
        self._data = DF.sort_values(self._order)[self.getColumns()].reset_index(drop=True)

    @classmethod
    def _validate(cls, DF):
        assert all(c in DF for c in cls.getColumns())

    def asNative(self):
        return self._data

    @property
    def order(self):
        return self._tolist(self._order)

    @property
    def funcPath(self):
        return self._tolist(self._funcPath)

    @property
    def inputKeys(self):
        return self._tolist(self._inputKeys)

    @property
    def kwargs(self):
        return self._tolist(self._kwargs)

    @property
    def outputKeys(self):
        return self._tolist(self._outputKeys)

    def _tolist(self, key):
        return self.asNative()[key].tolist()


class WorkflowDict:
    """ wrapper around a dictionary to control access to key-value pairs """

    _SPECIALKEY = "__data__"

    def __init__(self, data=None):
        data = data or {}
        self._validate(data)
        self._data = {self._SPECIALKEY: data}

    @classmethod
    def _validate(cls, data):
        assert cls._SPECIALKEY not in data

    def asNative(self):
        return self._data[self._SPECIALKEY]

    def __getitem__(self, item):
        if item != self._SPECIALKEY:
            return self.asNative()[item]
        return self._data

    def __setitem__(self, key, value):
        if key != self._SPECIALKEY:
            self.asNative()[key] = value
        else:
            self._data = value

    def update(self, data):
        for k, v in data.items():
            self[k] = v
