# coding: utf8

# Copyright (C) 2015 Zhe Wang <0x1998@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class GSSEdge(object):
    def __init__(self, return_state, target, nonpacked_node):
        self.return_state = return_state
        self.target = target
        self.nonpacked_node = nonpacked_node


class GSSNode(object):
    """
    A GSS Node records the return grammar position, needed to continue parsing
    after returning from a nonterminal.
    nt: X ::= aAb
    input_pos: current input position when the node is created
    """
    def __init__(self, nonterminal, input_pos):
        self.nonterminal = nonterminal
        self.input_pos = input_pos
        # G: set of GSSEdge
        self.edges = []

        # descriptor elimination set U: {Descriptor}
        # self.done = set()
        # popped elements P: {SPPFNode.right: (state, child)}
        self.results = {}

    def add_edge(self, input_pos, return_state, target, nonpacked_node):
        edge = GSSEdge(return_state, target, nonpacked_node)
        self.edges.append(edge)
        # TODO:

    # TODO:
    def pop(self, input_pos, end_of_rule_state, nonpacked_child_node):
        pass
