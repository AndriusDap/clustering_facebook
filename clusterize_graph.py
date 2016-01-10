import glob
import snap
import colorsys
import os
from multiprocessing import Pool
import sys

def rgb_to_hex(rgb):
    return '#' + ''.join(['%02x' % int(p * 255) for p in rgb])

def get_colours(count):
    count = count + 1
    colours = [colorsys.hsv_to_rgb(float(h) / count, 1, 1) for h in range(count)]
    return [rgb_to_hex(c) for c in colours]

def describe_communities(graph, communityType, communities):
	print ("{0}: {1} comunitySizes: [{2}]".format(graph, communityType, str.join(", ", [str(len(c)) for c in communities])))

def detectComunities(method, freshGraph, graph, basename, name):	
	comunities = snap.TCnComV()
	modularity = method(graph, comunities)
	describe_communities(basename, name, comunities)
	plot_comunities(freshGraph, comunities, basename + "_" + name + ".png")
	return modularity, comunities


def clusterize(graph):
	basename = "out\\" + graph.split("\\")[-1].split("/")[-1]
	print(basename)
	sys.stdout.flush()
	g = snap.LoadEdgeList(snap.PUNGraph, graph, 0, 1)
	cnm = snap.LoadEdgeList(snap.PUNGraph, graph, 0, 1)
	freshGraph = snap.LoadEdgeList(snap.PUNGraph, graph, 0, 1)

	#modularity, GirvanNewmanCommunities = detectComunities(snap.CommunityGirvanNewman, freshGraph, g, basename, "GirvanNewman")
	modularityCNM, CNMCommunities = detectComunities(snap.CommunityCNM, freshGraph, cnm, basename, "CNM")

	nodes = snap.TIntV()
	for n in freshGraph.Nodes():
		nodes.Add(n.GetId())
	modularityBefore = snap.GetModularity(freshGraph, nodes)

	print("{0}: modularity modularity CNM {1} modularity before {2}".format(graph,
		modularityCNM, modularityBefore))
	sys.stdout.flush()

def plot_comunities(graph, CmtyV, filename):
	rainbow = get_colours(len(CmtyV))
	comunities = list(CmtyV)

	NIdColorH = snap.TIntStrH()
	for c in CmtyV:
		for n in c:
			NIdColorH[n] = rainbow[comunities.index(c)]

		pass
	snap.DrawGViz(graph, snap.gvlSfdp, filename, " ", False, NIdColorH)

if __name__ == "__main__":
	try:
		os.mkdir("out")
	except:
		pass
	pool = Pool(4)
	pool.map(clusterize, glob.glob("data/*.edges"))
	#[clusterize(f) for f in glob.glob("data/*.edges")]