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


class State(object):
    def __init__(self):
        self.transitions = []

DUMMY_STATE = State()


class TerminalState(State):
    def __init__(self, terminal):
        super(TerminalState, self).__init__()
        self.terminal = terminal


class NonTerminalState(State):
    def __init__(self, nonterminal):
        super(NonTerminalState, self).__init__()
        self.nonterminal = nonterminal


class RuleState(State):
    def __init__(self, rule, rule_pos, sym_pos):
        super(RuleState, self).__init__()
        self.rule = rule
        self.rule_pos = rule_pos
        self.sym_pos = sym_pos

    def is_first(self):
        return self.sym_pos == 0

    def next_state(self):
        next_sym_pos = self.sym_pos + 1
        if next_sym_pos == len(self.rule):
            return EndOfRuleState(self.rule, self.rule_pos, next_sym_pos,
                                  self.rule.head.state)
        return RuleState(self.rule, self.rule_pos, next_sym_pos)
        # state = RuleState(self.rule, self.rule_pos, next_sym_pos)
        # state.set_follow_test = self.rule.get_follow_test(next_sym_pos)
        # return state

    def resume(self, runtime, descriptor):
        for transition in self.transitions:
            transition.follow(runtime, descriptor)


class EndOfRuleState(RuleState):
    def __init__(self, rule, rule_pos, sym_pos, nonterm_state):
        super(EndOfRuleState, self).__init__(rule, rule_pos, sym_pos)
        self.nonterm_state = nonterm_state

    def resume(self, runtime, descriptor):
        for transition in self.transitions:
            transition.follow(runtime, descriptor)


class EpsilonState(EndOfRuleState):
    def __init__(self, rule, rule_pos, sym_pos, nonterm_state, epsilon_state):
        super(EpsilonState, self).__init__(rule, rule_pos, sym_pos,
                                           nonterm_state)
        self.epsilon_state = epsilon_state
