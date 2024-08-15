import pydoc
import json

from typing import Dict, TypeVar, Type

from pydantic import field_validator
# from practice.lib.pydantic import base
import pydantic as base

# BaseModelInst = TypeVar('practice.lib.pydantic.base.BaseModel')
BaseModelInst = TypeVar('pydantic.BaseModel')
BaseModelType = Type[ base.BaseModel]


def toJson( model: BaseModelType, **kw ) -> str:
    data = toDict( model )
    return json.dumps( data, **kw )

def fromJson( loadable: str ) -> BaseModelType:
    data = json.loads( loadable )
    return fromDict( data )

def toDict( model: BaseModelType ) -> Dict:
    dictModel = ToDictModel( pmodel=model, kwargs=model )
    return dictModel.model_dump()

def fromDict( data: Dict ) -> BaseModelType:
    dictModel = FromDictModel( **data )
    return dictModel.pmodel( **dictModel.kwargs )


class ToDictModel(base.BaseModel):
    pmodel : BaseModelInst
    kwargs : BaseModelInst

    @field_validator( 'pmodel' )
    @classmethod
    def mustBeBaseModelInstance( cls, pmodel: BaseModelInst ) -> str:
        cls._mustBeBaseModelInstance( pmodel )
        klass = pmodel.__class__
        return f"{ klass.__module__ }.{ klass.__name__ }"

    @field_validator( 'kwargs' )
    @classmethod
    def mustBeDumpable( cls, pmodel: BaseModelInst ) -> Dict:
        cls._mustBeBaseModelInstance( pmodel )
        return pmodel.model_dump()

    @staticmethod
    def _mustBeBaseModelInstance( pmodel: BaseModelInst ) -> None:
        if not isinstance(pmodel, base.BaseModel):
            raise TypeError( f'{ pmodel= } must be an instance of { base.BaseModel }')


class FromDictModel(base.BaseModel):
    pmodel : str
    kwargs : Dict

    @field_validator( 'pmodel' )
    @classmethod
    def mustBeBaseModelSubclass( cls, pmodel: str ) -> BaseModelType:
        Model = pydoc.locate( pmodel )
        valid = Model and issubclass(Model, base.BaseModel)
        if not valid:
            raise TypeError( f'{ pmodel= } must be subclassed from { base.BaseModel }')
        return Model
