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
from gll.result import Success
from gll.lookahead import LookAheadTest, FollowTest
from gll.state import TerminalState, NonTerminalState, RuleState, EpsilonState
from gll.transition import TerminalTransition, NonTerminalTransition


class Symbol(object):
    def __init__(self, grammar):
        self.grammar = grammar
        self.action = None

    def __rshift__(self, action):
        self.action = action
        return self


class Terminal(Symbol):
    def __init__(self, grammar, matcher):
        super(Terminal, self).__init__(grammar)
        self.matcher = matcher
        self.state = TerminalState(self)

    def get_transition(self, target_state):
        return TerminalTransition(self.state, target_state)

    def match(self, input, pos):
        return self.matcher.match(input, pos)


class Epsilon(Terminal):
    def __init__(self, grammar):
        super(Epsilon, self).__init__(grammar, None)

    def match(self, input, pos):
        return Success(None, pos)


class NonTerminal(Symbol):
    def __init__(self, grammar):
        super(NonTerminal, self).__init__(grammar)
        self.rules = []
        self.state = NonTerminalState(self)
        self.look_ahead_test = LookAheadTest(grammar.look_ahead_count)
        self.follow_test = FollowTest()

    def add_rule(self, *symbols):
        rule = Rule(self, symbols)
        position = len(self.rules)
        self.rules.append(rule)
        rule.chain_states(position)

    def first_states(self):
        return [rule.first_state for rule in self.rules]

    def get_transition(self, target_state):
        return NonTerminalTransition(self.state, target_state)

    def __len__(self):
        return len(self.rules)

    def deterministic(self):
        return len(self.rules) == 1


class Rule(object):
    def __init__(self, head, body):
        self.head = head
        self.body = body
        self.first_state = None

    def chain_states(self, rule_pos):
        rule_len = len(self.body)
        if rule_len == 0:
            self.first_state = EpsilonState(self, rule_pos, 0, self.head.state,
                                            self.head.grammar.epsilon_state)
            return

        self.first_state = RuleState(self, rule_pos, 0)
        state = self.first_state
        for pos in range(rule_len):
            transition = self.body[pos].get_transition(state.next_state())
            state.transitions.append(transition)
            state = transition.target

    def __len__(self):
        return len(self.body)
