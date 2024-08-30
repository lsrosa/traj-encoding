# -*- coding: utf-8 -*-

from networkx_viewer import Viewer
import networkx as nx
import requests 

# rewrite this with https://pyvis.readthedocs.io/en/latest/tutorial.html
# test also https://github.com/oowekyala/citegraph

def build(bibtex_db):
    edges = []
    nodes = {}

    for e in bibtex_db.values():
        try:
            nodes[e["doi"]] = e["ID"]
        except KeyError:
            print("(!) No doi found for " + e["ID"] + "! Skipping...")
            continue
        
    for n1 in nodes:
        print("Checking who " + nodes[n1] + " cited...")
        # n1 is doi (node 1)
        n = n1.replace('https://doi.org/', '') # remove http part of full DOIs
        url = f"https://opencitations.net/index/coci/api/v1/citations/{n}"
        #print('requesting: ', url)
        r = requests.get(url)
        #print(r)
        data = r.json()
        #print(data)
        
        if(data == []):
            print(f"(!) Unforunately API didn't provide any citations for: {nodes[n1]}")
            continue

        for d in data:
            n2 = d['citing']
            if n2 in nodes:
                edges.append([nodes[n2], nodes[n1]])

    with open('edges.txt', 'w') as f:
        for e in edges:
            f.write(f"{e[0]} {e[1]}\n")
    
    return

def draw():
    edge_list_path = r"edges.txt"
    DG = nx.read_edgelist(edge_list_path,create_using=nx.DiGraph())

    try:
        app = Viewer(DG)
        app.mainloop()
    except IndexError:
        print("(!) Citation network is empty. Try adding more papers...")
    

    