from abcd_graph import ABCDGraph, ABCDParams


params = ABCDParams(vcount=1_000_000, min_degree=3, gamma=3, beta=2)
g = ABCDGraph(params, logger=True)

g.build()
