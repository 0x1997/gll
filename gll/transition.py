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
from gll.result import Failure
from gll.sppf import IntermediateNode


class Transition(object):
    def __init__(self, target_state):
        self.target = target_state

    def follow(self, runtime, descriptor):
        raise NotImplementedError


class TerminalTransition(Transition):
    def __init__(self, term_state, target_state):
        super(TerminalTransition, self).__init__(target_state)
        self.term_state = term_state

    def follow(self, runtime, descriptor):
        terminal = self.term_state.terminal
        result = terminal.match(runtime.input, descriptor.input_pos)
        if isinstance(result, Failure):
            runtime.record_error(self, result)
            return
        if terminal.action is not None:
            terminal.action(result)

        nonpacked_node = runtime.get_term_node(self.term_state,
                                               descriptor.input_pos,
                                               result.input_pos)
        if not self.target.is_first():
            nonpacked_node = IntermediateNode(self.target,
                                              descriptor.nonpacked_node,
                                              nonpacked_node)
        descriptor.input_pos = result.input_pos
        descriptor.nonpacked_node = nonpacked_node
        self.target.resume(runtime, descriptor)


class NonTerminalTransition(Transition):
    def __init__(self, nonterm_state, target_state):
        super(NonTerminalTransition, self).__init__(target_state)
        self.nonterm_state = nonterm_state

    def follow(self, runtime, descriptor):
        runtime.create_gss_edge(self.nonterm_state, descriptor.input_pos,
                                self.target, descriptor.gss_node,
                                descriptor.nonpacked_node)
