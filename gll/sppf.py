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
from gll.state import DUMMY_STATE


class NonPackedNode(object):
    def __init__(self, state, left, right):
        self.state = state
        self.left = left
        self.right = right


class NonTerminalNode(NonPackedNode):
    def __init__(self, state, left, right):
        super(NonTerminalNode, self).__init__(state, left, right)
        # [PackedNode]
        self.children = []


class TerminalNode(NonPackedNode):
    pass


class IntermediateNode(NonPackedNode):
    """
    Groups the symbols of an alternative in a left-associative manner
    A ::= a.b  where |a|,|b| > 0
    """
    def __init__(self, state, left, right):
        super(IntermediateNode, self).__init__(state, left, right)
        # [PackedNode]
        self.children = []


class DummyNode(NonPackedNode):
    def __init__(self):
        super(DummyNode, self).__init__(DUMMY_STATE, -1, 0)


class PackedNode(object):
    """
    Represents a derivation
    state: A ::= a.b
    pivot: the right extent of the left child
    """
    def __init__(self, rule_state, left_child, right_child=None):
        self.state = rule_state
        self.left_child = left_child
        self.right_child = right_child
        self.pivot = left_child.left
