#
# tsplib.py
# load TSPLIB instances of the traveling salesperson problem
# CSUF CPSC 335 - Spring 2014
#
# Example usage:
#
#   import tsplib
#   tsp = tsplib.load('burma14.xml.zip')
#   for i in range(tsp.vertex_count()):
#     if not tsp.is_edge(i, 0):
#       print('no edge from ' + str(i) + ' to 0')
#     else:
#       print('edge from ' + str(i) ' to 0 costs ' + str(tsp.distance(i, 0)))
#
# In case it matters, this file is licensed according to the BSD
# 2-clause license:
#
# Copyright (c) 2014, Kevin Wortman
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
#     Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
# 
#     Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import unittest
import xml.etree.ElementTree
import zipfile

# A TSP object is an instance of the traveling salesperson
# problem. You probably want to create them with the load() function
# below, not the constructor.
#
# A graph has n>0 vertices. Each vertex is identified by an index in
# range(n).
class TSP:
    def __init__(self, n, name, description):
        if (n <= 0 or
            not isinstance(name, str) or
            not isinstance(description, str)):
            raise ValueError
        self.name = name
        self.description = description
        self.adj = [ [None] * n for i in range(n) ]
    
    # Return the number of vertices in the graph.
    def vertex_count(self):
        return len(self.adj)

    # Return true if there exists an edge from from_vertex to
    # to_vertex.
    def is_edge(self, from_vertex, to_vertex):
        self._check_vertices(from_vertex, to_vertex)
        return self.adj[from_vertex][to_vertex] is not None

    # Return the weight of the edge from from_vertex to
    # to_vertex. Raises a ValueError exception if not
    # is_edge(from_vertex, to_vertex) .
    def distance(self, from_vertex, to_vertex):
        if not self.is_edge(from_vertex, to_vertex):
            raise ValueError
        return self.adj[from_vertex][to_vertex]

    # Helper that returns true if i is a valid vertex index for this
    # graph.
    def is_vertex(self, i):
        return i >= 0 and i < self.vertex_count()

    # Helper that raises IndexError if either i or j is not a valid
    # vertex index for this graph.
    def _check_vertices(self, i, j):
        if not self.is_vertex(i) or not self.is_vertex(j):
            raise IndexError
        
    # Creates a weight edge from from_vertex to to_vertex.
    def set_distance(self, from_vertex, to_vertex, distance):
        self._check_vertices(from_vertex, to_vertex)
        self.adj[from_vertex][to_vertex] = distance

# Loads a TSPLIB instance from file and returns it as a TSP
# object. file may be a file-like object, or a string which is
# interpreted as a path name. Raises an exception on error.
def load(file):
    zip = zipfile.ZipFile(file)
    members = zip.namelist()
    if len(members) != 1:
        raise ValueError
    xml_file = zip.open(members[0])
    tree = xml.etree.ElementTree.parse(xml_file)
    xml_file.close()
    zip.close()

    edges = []
    vertices = tree.find('graph').findall('vertex')
    for from_vertex in range(len(vertices)):
        for edge in vertices[from_vertex].findall('edge'):
            cost = float(edge.attrib['cost'])
            to_vertex = int(edge.text)
            edges.append(LoadEdge(from_vertex, to_vertex, cost))
    if len(edges) == 0:
        raise ValueError

    max_index = max([max(edge.frm, edge.to) for edge in edges])
    n = max_index + 1
    if n <= 0:
        raise ValueError

    name = tree.find('name').text
    description = tree.find('description').text

    tsp = TSP(n, name, description)
    for edge in edges:
        tsp.set_distance(edge.frm, edge.to, edge.cost)

    return tsp

# Helper class to store one edge XML tag after it's been loaded but
# before it's been incorporated into a TSP object.
class LoadEdge:
    def __init__(self, frm, to, cost):
        self.frm = frm
        self.to = to
        self.cost = cost

class TestTSP(unittest.TestCase):
    def setUp(self):
        self.br17 = load('br17.xml.zip')

    def test_load(self):
        self.assertIsInstance(self.br17, TSP)

        self.assertEqual(self.br17.vertex_count(), 17)

        self.assertFalse(self.br17.is_vertex(-1))
        for i in range(17):
            self.assertTrue(self.br17.is_vertex(i))
        self.assertFalse(self.br17.is_vertex(17))
        
        self.assertEqual(self.br17.distance(0, 0), 9.999000000000000e+03)
        self.assertEqual(self.br17.distance(0, 16), 5.000000000000000e+00)
        
        self.assertEqual(self.br17.distance(16, 0), 5.000000000000000e+00)
        self.assertEqual(self.br17.distance(16, 16), 9.999000000000000e+03)

if __name__ == '__main__':
    unittest.main()
