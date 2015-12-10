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
from gll import Input, Grammar, Parser, ParseException


def log(msg):
    def fn(res):
        print('%s: %s'.format(msg, res.value))
    return fn


def test_parser1():
    g = Grammar()

    e = g.any()
    e.add_rule(g.literal('a'))
    e.add_rule(g.literal('-'), e)
    e.add_rule(e, g.literal('+'), e)
    g.set_start(e)

    parser = Parser(g)
    parser.parse(Input.from_string('-a+a'))


def test_parser2():
    g = Grammar()

    prompt = g.literal('>>') >> log('prompt')
    digit0 = g.literal('0') >> log('digit0')
    digit1 = g.literal('1') >> log('digit1')
    digit = g.any(digit0, digit1) >> log('digit')
    nl = g.literal('\n') >> log('nl')
    space = g.star(g.literal(' '))
    line = g.seq(prompt, space, digit, nl) >> log('line')
    text = g.star(line) >> log('text')
    g.set_start(text)

    parser = Parser(g)
    parser.parse(Input.from_string('>> 0\n>> 1\n>> 1\n>> 0\n'))


def test_parser3():
    g = Grammar()

    a = g.literal('a') >> log('a')
    b = g.literal('b') >> log('b')
    c = g.literal('c') >> log('c')
    B = g.any(b)
    C = g.any() >> log('C')
    C.add_rule(a, C)
    C.add_rule(c)
    A = g.any([a, B, c], C) >> log('A')
    g.set_start(A)

    parser = Parser(g)
    parser.parse(Input.from_string('abc'))
    parser.parse(Input.from_string('aaaac'))
