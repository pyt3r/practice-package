from enum import Enum


class SCHEMA:
    ORDER   = "order"
    FUNCS   = "funcPath"
    INPUTS  = "inputKeys"
    KWLIST  = "kwargs"
    OUTPUTS = "outputKeys"

    @classmethod
    def getColumns(cls):
        return [
            cls.ORDER,
            cls.FUNCS,
            cls.INPUTS,
            cls.KWLIST,
            cls.OUTPUTS, ]


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
