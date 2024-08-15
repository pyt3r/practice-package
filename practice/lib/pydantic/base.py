import pydantic
from pydantic import Extra, ConfigDict


class ExtraForbidden( pydantic.BaseModel ):
    model_config = ConfigDict( extra='forbid' )


class ExtraAllowed( pydantic.BaseModel ):
    model_config = ConfigDict( extra='allow' )


class BaseModel( ExtraForbidden ):
    """ patched base model """
