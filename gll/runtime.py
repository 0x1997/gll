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
from collections import defaultdict
from gll.gss import GSSNode
from gll.sppf import DummyNode, TerminalNode


class Descriptor(object):
    def __init__(self, rule_state, input_pos, gss_node, nonpacked_node):
        self.state = rule_state
        self.input_pos = input_pos
        self.gss_node = gss_node
        self.nonpacked_node = nonpacked_node

    def resume(self, runtime):
        self.state.resume(runtime, self)


class Runtime(object):
    def __init__(self, grammar, input):
        self.input = input
        self.start = grammar.start
        self.start_gss_node = GSSNode(grammar.start, 0)
        # R: [Descriptor]
        self.pending = [Descriptor(state, 0, self.start_gss_node, DummyNode())
                        for state in grammar.start.first_states()]
        self.states = defaultdict(dict)
        self.error = None

    def has_next(self):
        return len(self.pending) != 0

    def dispatch(self):
        while self.has_next():
            descriptor = self.pending.pop()
            descriptor.resume(self)
        return self.start_gss_node.results.get(self.input.len - 1)

    def record_error(self, *args):
        self.error = args

    def add(self, *args):
        self.pending.append(Descriptor(*args))

    def get_term_node(self, term_state, i, j):
        term_nodes = self.states[term_state]
        node = term_nodes.get(i)
        if node is None:
            node = term_nodes[i] = TerminalNode(term_state, i, j)
        return node

    def create_gss_edge(self, nonterm_state, input_pos, return_state,
                        target_gss_node, nonpacked_node):
        gss_nodes = self.states[nonterm_state]
        node = gss_nodes.get(input_pos)
        if node is not None:
            node.add_edge(input_pos, return_state, target_gss_node,
                          nonpacked_node)
            return
        node = gss_nodes[input_pos] = GSSNode(nonterm_state, input_pos)
        node.add_edge(input_pos, return_state, target_gss_node, nonpacked_node)
        for state in nonterm_state.nonterminal.look_ahead_test(input_pos):
            self.pending.append(Descriptor(state, input_pos, node, DummyNode()))
