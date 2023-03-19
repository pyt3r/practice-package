import collections
import graphviz
from practice.frameworks import inspector


def buildDag(outputs, funcs, inputs):
    funcNames = [inspector.Inspector(f).getName() for f in funcs]
    return _buildDag(outputs, funcNames, inputs)


def _buildDag(outputs, funcNames, inputs):
    dag = graphviz.Digraph()
    names = _renameFuncs(funcNames)

    dag.attr("node", shape="circle")
    for fun in names:
        dag.node(fun)

    dag.attr("node", shape="rectangle")
    for fun, o in _getEdges(names, outputs):
        dag.node(o)
        dag.edge(fun, o)

    for fun, i in _getEdges(names, inputs):
        dag.node(i)
        dag.edge(i, fun)

    return dag


def _renameFuncs(funcs):
    counts = collections.Counter(funcs)
    newfuncs = []
    for f in reversed(funcs):
        counts[f] -= 1
        cnt = counts[f]
        new = f"{f}[{cnt}]" if cnt else f
        newfuncs.append(new)
    return list(reversed(newfuncs))


def _getEdges(funcs, xputs):
    edges = set()
    for f, puts in zip(funcs, xputs):
        for x in puts:
            edges.add((f, x))
    return edges


