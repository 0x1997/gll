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
import re
from gll.result import Success, Failure
from gll.symbol import *


class Matcher(object):
    def match(self, input, i):
        raise NotImplementedError


class Literal(Matcher):
    def __init__(self, pattern):
        super(Literal, self).__init__()
        self.pattern = pattern

    def match(self, input, i):
        j = i + len(self.pattern)
        if input.str.startswith(self.pattern, i):
            return Success(self.pattern, j)
        return Failure('Expected: %s, Found: %s'.format(self.pattern,
                                                        input.str[i:j]), i)


class Regex(Matcher):
    def __init__(self, pattern):
        super(Regex, self).__init__()
        self.pattern = re.compile(pattern)
        self.pattern_str = pattern

    def match(self, input, i):
        m = self.pattern.search(input.str, i)
        if m:
            return Success(m.group(), m.end())
        return Failure('Expected: %s'.format(self.pattern_str), i)


class FirstFollowSets(object):
    def __init__(self, grammar):
        self.grammar = grammar


class Grammar(object):
    def __init__(self, look_ahead_count=1):
        self.look_ahead_count = look_ahead_count
        self.start = None
        self.first_follow_sets = FirstFollowSets(self)
        self.epsilon = Epsilon(self)
        self.epsilon_state = TerminalState(self.epsilon)

        # first_follow_set
        # convert(rule)
        # for nt in nonterminals: set_first_follow_tests

    def literal(self, string):
        return Terminal(self, Literal(string))

    def regex(self, pattern):
        return Terminal(self, Regex(pattern))

    def any(self, *symbols):
        nt = NonTerminal(self)
        for sym in symbols:
            if isinstance(sym, Symbol):
                nt.add_rule(sym)
            else:
                nt.add_rule(*sym)
        return nt

    def seq(self, *symbols):
        nt = NonTerminal(self)
        nt.add_rule(*symbols)
        return nt

    def opt(self, symbol):
        return self.any(symbol, self.epsilon)

    def plus(self, symbol):
        return self.any([symbol, symbol], symbol)

    def star(self, symbol):
        return self.any(self.plus(symbol), self.epsilon)

    def set_start(self, start):
        assert isinstance(start, NonTerminal)
        self.start = start
