from practice.lib.pydantic import ser_des, base
from typing import ClassVar
import unittest


class TestCase( unittest.TestCase ):

    def test_to_and_from_json(self):
        data = {
            'b': {'bdata': 1},
            'c': {'cdata': '2'},
        }

        obj = A( **data )
        serialized = ser_des.toJson(obj)
        deserialized = ser_des.fromJson(serialized)

        self.assertEqual( obj, deserialized )


class B(base.BaseModel):
    bdata: int


class C(base.BaseModel):
    cdata: float


class A(base.BaseModel):
    b: B
    c: C

    x: ClassVar = 1

    def y( self ):
        pass
