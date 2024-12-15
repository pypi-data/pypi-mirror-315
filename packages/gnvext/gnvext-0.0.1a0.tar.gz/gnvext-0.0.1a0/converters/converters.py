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

__all__ = (
    'StringEnvVariable',
    'IntegerEnvVariable',
    'FloatEnvVariable',
    'BooleanEnvVariable',
    'CollectionEnvVariable',
)

import ast
from typing import Any, Callable, Iterable

from gnvext.converters.base import EnvVariable as _EnvVariable


class StringEnvVariable(_EnvVariable):
    """
    class to extract env variable as a string
    """

    def convert(self, value: str) -> str:
        return value


class IntegerEnvVariable(_EnvVariable):
    """
    class to extract env variable as an integer
    """

    def convert(self, value: str) -> int:
        return int(value)


class FloatEnvVariable(_EnvVariable):
    """
    class to extract env variable as a floating number
    """

    def convert(self, value: str) -> float:
        return float(value)


class BooleanEnvVariable(_EnvVariable):
    """
    class to extract env variable as a boolean object

    Attributes
    ----------
    TRUTHY_VALUES:
        values to be recognized as truthy
    FALSY_VALUES:
        values to be recognized as falsy
    """

    TRUTHY_VALUES = ('True', 'true', 'T', 't', '1')
    FALSY_VALUES = ('False', 'false', 'F', 'f', '0')

    def convert(self, value: str | bool) -> bool:
        if isinstance(value, bool):
            return value

        value = self._getenv()
        cleaned = value.strip()

        if cleaned in self.TRUTHY_VALUES:
            return True
        if cleaned in self.FALSY_VALUES:
            return False

        raise ValueError(f'could not convert "{value}" to bool')


class CollectionEnvVariable(_EnvVariable):
    """
    class to extract env variable as a collection

    Attributes
    ----------
    CONVERT_COLLECTION_TYPE:
        the type to which the collection should be cast (list by default)
    """

    CONVERT_COLLECTION_TYPE: Callable = list
    _BRACKETS = '{}()[]'

    def convert(self, value: str | Iterable[Any]) -> Any:
        value = self._get_cleaned_value()

        # building collection from a cleaned string
        collection = ast.literal_eval(value)

        # convert collection to the expected type and return it
        return self.CONVERT_COLLECTION_TYPE(collection)

    def _get_split_values(self, brackets: str = _BRACKETS) -> list[str]:
        """
        removes brackets, leading and ending spaces and then splits
        """

        value = self._getenv().strip()
        no_brackets = value.strip(brackets)
        return no_brackets.split()

    @staticmethod
    def _wrap_value_to_quotes(value: str) -> str:
        """
        escapes all the quotes in the string
        and then wraps it into double quotes
        """

        value = value.strip().replace("'", "\\'").replace('"', '\\"')

        if value.endswith(','):
            value = value[:-1]

        if ((value.startswith('\\"') and value.endswith('\\"')
            or value.startswith("\\'") and value.endswith("\\'"))
                and len(value) != 2):
            value = value[2:-2]

        return f'"{value}"'

    def _get_cleaned_value(self, brackets: str = _BRACKETS) -> str:
        """
        makes a collection-convertable string from an env variable value
        """

        values = self._get_split_values(brackets=brackets)

        for idx, v in enumerate(values):
            values[idx] = self._wrap_value_to_quotes(v)

        value = f'({", ".join(values)},)'
        return value
