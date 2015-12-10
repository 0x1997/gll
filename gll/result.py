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


class Result(object):
    def __init__(self, input_pos):
        self.input_pos = input_pos


class Success(Result):
    def __init__(self, value, input_pos):
        super(Success, self).__init__(input_pos)
        self.value = value

    def __repr__(self):
        return '<Success: %s at %s>'.format(self.value, self.input_pos)


class Failure(Result):
    def __init__(self, error, input_pos):
        super(Failure, self).__init__(input_pos)
        self.error = error

    def __repr__(self):
        return '<Failure: %s at %s)>'.format(self.error, self.input_pos)
