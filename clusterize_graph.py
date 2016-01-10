import glob
import snap
import colorsys

def rgb_to_hex(rgb):
    return '#' + ''.join(['%02x' % int(p * 255) for p in rgb])

def get_colours(count):
    count = count + 1
    colours = [colorsys.hsv_to_rgb(float(h) / count, 1, 1) for h in range(count)]
    return [rgb_to_hex(c) for c in colours]


for graph in glob.glob("data/*.edges"):
	print("Graph: " + graph)
	g = snap.LoadEdgeList(snap.PUNGraph, graph, 0, 1)
	

	NIdColorH = snap.TIntStrH()
	CmtyV = snap.TCnComV()
	snap.CommunityGirvanNewman(g, CmtyV)
	rainbow = get_colours(len(CmtyV))
	comunities = list(CmtyV)
	for c in CmtyV:
		for n in c:
			NIdColorH[n] = rainbow[comunities.index(c)]

	snap.DrawGViz(g, snap.gvlSfdp, "out\\" + graph.split("\\")[-1] + "cgn.png", " ", False, NIdColorH)


