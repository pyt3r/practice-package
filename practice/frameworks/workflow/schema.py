
ORDER      = "order"
FUNCS      = "funcPath"
INPUTS     = "inputKeys"
KWLIST     = "kwargs"
OUTPUTS    = "outputKeys"
DEFAULT_KW = "defaultkwargs"

def getExternalColumns():
    return [ ORDER, FUNCS, INPUTS, KWLIST, OUTPUTS, ]

def getInternalColumns():
    return getExternalColumns() + [ DEFAULT_KW ]
