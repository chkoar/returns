# -*- coding: utf-8 -*-

from abc import ABCMeta
from functools import wraps
from inspect import iscoroutinefunction
from typing import Any, TypeVar

from returns.primitives.container import (
    FixableContainer,
    GenericContainerTwoSlots,
    ValueUnwrapContainer,
)
from returns.primitives.exceptions import UnwrapFailedError

_ValueType = TypeVar('_ValueType')
_ErrorType = TypeVar('_ErrorType')


class Result(
    GenericContainerTwoSlots[_ValueType, _ErrorType],
    FixableContainer,
    ValueUnwrapContainer,
    metaclass=ABCMeta,
):
    """Base class for _Failure and _Success."""


class _Failure(Result[Any, _ErrorType]):
    """
    Represents a calculation which has failed.

    It should contain an error code or message.
    Should not be used directly.
    """

    def map(self, function):  # noqa: A003
        """Returns the '_Failure' instance that was used to call the method."""
        return self

    def bind(self, function):
        """Returns the '_Failure' instance that was used to call the method."""
        return self

    def fix(self, function):
        """
        Applies function to the inner value.

        Applies 'function' to the contents of the '_Success' instance
        and returns a new '_Success' object containing the result.
        'function' should accept a single "normal" (non-container) argument
        and return a non-container result.
        """
        return _Success(function(self._inner_value))

    def rescue(self, function):
        """
        Applies 'function' to the result of a previous calculation.

        'function' should accept a single "normal" (non-container) argument
        and return Result a '_Failure' or '_Success' type object.
        """
        return function(self._inner_value)

    def value_or(self, default_value):
        """Returns the value if we deal with '_Success' or default otherwise."""
        return default_value

    def unwrap(self):
        """Raises an exception, since it does not have a value inside."""
        if isinstance(self._inner_value, Exception):
            raise UnwrapFailedError(self) from self._inner_value

        raise UnwrapFailedError(self)

    def failure(self):
        """Unwraps inner error value from failed container."""
        return self._inner_value


class _Success(Result[_ValueType, Any]):
    """
    Represents a calculation which has succeeded and contains the result.

    Contains the computation value.
    Should not be used directly.
    """

    def map(self, function):  # noqa: A003
        """
        Applies function to the inner value.

        Applies 'function' to the contents of the '_Success' instance
        and returns a new '_Success' object containing the result.
        'function' should accept a single "normal" (non-container) argument
        and return a non-container result.
        """
        return _Success(function(self._inner_value))

    def bind(self, function):
        """
        Applies 'function' to the result of a previous calculation.

        'function' should accept a single "normal" (non-container) argument
        and return Result a '_Failure' or '_Success' type object.
        """
        return function(self._inner_value)

    def fix(self, function):
        """Returns the '_Success' instance that was used to call the method."""
        return self

    def rescue(self, function):
        """Returns the '_Success' instance that was used to call the method."""
        return self

    def value_or(self, default_value):
        """Returns the value if we deal with '_Success' or default otherwise."""
        return self._inner_value

    def unwrap(self):
        """Returns the unwrapped value from the inside of this container."""
        return self._inner_value

    def failure(self):
        """Raises an exception, since it does not have an error inside."""
        raise UnwrapFailedError(self)


def Success(inner_value):  # noqa: N802
    """Public unit function of protected `_Success` type."""
    return _Success(inner_value)


def Failure(inner_value):  # noqa: N802
    """Public unit function of protected `_Failure` type."""
    return _Failure(inner_value)


def is_successful(container):
    """
    Determins if a container was successful or not.

    We treat container that raise ``UnwrapFailedError`` on ``.unwrap()``
    not successful.
    """
    try:
        container.unwrap()
    except UnwrapFailedError:
        return False
    else:
        return True


def safe(function):  # noqa: C901
    """
    Decorator to covert exception throwing function to 'Result' container.

    Show be used with care, since it only catches 'Exception' subclasses.
    It does not catch 'BaseException' subclasses.

    Supports both async and regular functions.
    """
    if iscoroutinefunction(function):
        async def decorator(*args, **kwargs):
            try:
                return _Success(await function(*args, **kwargs))
            except Exception as exc:
                return _Failure(exc)
    else:
        def decorator(*args, **kwargs):
            try:
                return _Success(function(*args, **kwargs))
            except Exception as exc:
                return _Failure(exc)
    return wraps(function)(decorator)


def pipeline(function):  # noqa: C901
    """
    Decorator to enable 'do-notation' context.

    Should be used for series of computations that rely on ``.unwrap`` method.

    Supports both async and regular functions.
    """
    if iscoroutinefunction(function):
        async def decorator(*args, **kwargs):
            try:
                return await function(*args, **kwargs)
            except UnwrapFailedError as exc:
                return exc.halted_container
    else:
        def decorator(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except UnwrapFailedError as exc:
                return exc.halted_container
    return wraps(function)(decorator)
