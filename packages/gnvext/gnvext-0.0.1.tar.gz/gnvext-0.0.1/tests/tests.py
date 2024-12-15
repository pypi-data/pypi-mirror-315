"""
The MIT License (MIT)

Copyright (c) 2024-present DouleLove

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from gnvext.converters.converters import (
    BooleanEnvVariable,
    CollectionEnvVariable,
    FloatEnvVariable,
    IntegerEnvVariable,
    StringEnvVariable
)
from gnvext.tests.base import EnvVariablesTestSuite
from gnvext.tests.utils import MISSING, generic_suite_runner


class TestStringEnvVariable(EnvVariablesTestSuite):
    CLS_TO_TEST = StringEnvVariable
    TESTCASES = [
        ['abcd', 'abcd'],
        ['ab cd', 'ab cd'],
        [MISSING, 'abcd', 'abcd'],
        [MISSING, None],
        [MISSING, 10, 10],
    ]


class TestIntegerEnvVariable(EnvVariablesTestSuite):
    CLS_TO_TEST = IntegerEnvVariable
    TESTCASES = [
        ['123', 123],
        ['12 34', ValueError],
        ['   1234 ', 1234],
        ['1234.0', ValueError],
        [MISSING, 1234, 1234],
        [MISSING, None],
        [MISSING, 17.4, 17.4],
    ]


class TestFloatEnvVariable(EnvVariablesTestSuite):
    CLS_TO_TEST = FloatEnvVariable
    TESTCASES = [
        ['1234.0', 1234.0],
        ['5735.7', 5735.7],
        ['123 4.0', ValueError],
        ['1234. 4', ValueError],
        ['1234', 1234.0],
        [MISSING, 1234.4, 1234.4],
        [MISSING, None],
        [MISSING, 17, 17],
    ]


class TestBooleanEnvVariable(EnvVariablesTestSuite):
    CLS_TO_TEST = BooleanEnvVariable
    TESTCASES = [
        ['True', True],
        ['  t', True],
        ['1', True],
        ['true', True],
        ['   False   ', False],
        [' false ', False],
        ['0', False],
        ['f', False],
        [MISSING, True, True],
        [MISSING, False, False],
        [MISSING, None],
        [MISSING, 'True', 'True'],
    ]


class TestCollectionEnvVariable(EnvVariablesTestSuite):
    CLS_TO_TEST = CollectionEnvVariable
    TESTCASES = [
        ['val1, val2, val3', ['val1', 'val2', 'val3']],
        ['[val1, val2]', ['val1', 'val2']],
        ['[val1, val2,]', ['val1', 'val2']],
        ['(val1, val2,)', ['val1', 'val2']],
        ['val1, val2 val3', ['val1', 'val2', 'val3']],
        ['"val1", "val2", "val3"', ['val1', 'val2', 'val3']],
        ['  [abcd]    ', ['abcd']],
        [""" ["abcd", 'abc', " '] """, ['abcd', 'abc', '"', "'"]],
        [""" "abcd", "'", '"', b """, ['abcd', "'", '"', 'b']],
        [' [ ab,cd,,abcd, "val2"  ]  ', ['ab,cd,,abcd', 'val2']],
        [MISSING, ['val1', 'val2', 'val3'], ['val1', 'val2', 'val3']],
        [MISSING, None],
        [MISSING, (1, 2, 3), (1, 2, 3)],
    ]


if __name__ == '__main__':
    with generic_suite_runner() as suite:
        suite.addTest(TestStringEnvVariable())
        suite.addTest(TestIntegerEnvVariable())
        suite.addTest(TestFloatEnvVariable())
        suite.addTest(TestBooleanEnvVariable())
        suite.addTest(TestCollectionEnvVariable())
