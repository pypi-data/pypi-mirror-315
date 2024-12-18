# Standard libraries
from collections.abc import Callable, Iterator
from typing import NoReturn, Protocol, TypeVar, runtime_checkable

# Third-party libraries
import attrs

# Local libraries
from oxy.exceptions import UnwrapError

T = TypeVar("T")
U = TypeVar("U")
R = TypeVar("R")
E = TypeVar("E")


class Maybe(Protocol[T]):
    def is_something(self) -> bool: ...
    def is_nothing(self) -> bool: ...
    def contains(self, item: T) -> bool: ...
    def expects(self, msg: str) -> T: ...
    def unwrap(self) -> T: ...
    def unwrap_or(self, default: T) -> T: ...
    def unwrap_or_else(self, f: Callable[[], T]) -> T: ...
    def map(self, f: Callable[[T], U]) -> "Maybe[U]": ...
    def map_or(self, default: U, f: Callable[[T], U]) -> U: ...
    def map_or_else(self, default: Callable[[], U], f: Callable[[T], U]) -> U: ...
    def iter(self) -> Iterator[T]: ...
    def filter(self, predicate: Callable[[T], bool]) -> "Maybe[T]": ...
    def ok_or(self, err: E) -> "Result[T, E]": ...
    def ok_or_else(self, err: Callable[[], E]) -> "Result[T, E]": ...
    def and_then(self, f: Callable[[T], "Maybe[T]"]) -> "Maybe[T]": ...
    def or_else(self, f: Callable[[], "Maybe[T]"]) -> "Maybe[T]": ...
    def xor(self, other: "Maybe[T]") -> "Maybe[T]": ...
    def zip(self, value: "Maybe[U]") -> "Maybe[tuple[T, U]]": ...
    def zip_with(
        self, other: "Maybe[U]", f: Callable[[tuple[T, U]], R]
    ) -> "Maybe[R]": ...
    def flatten_one(self) -> "Maybe[T]": ...
    def flatten(self) -> "Maybe[T]": ...
    def transpose(self) -> "Result[Maybe[T], E]": ...
    def __bool__(self) -> bool: ...
    def __contains__(self, item: T) -> bool: ...
    def __iter__(self) -> Iterator[T]: ...
    def __eq__(self, other: object) -> bool: ...


@attrs.frozen
class Something(Maybe[T]):
    _value: T

    def is_something(self) -> bool:
        return True

    def is_nothing(self) -> bool:
        return False

    def contains(self, item: T) -> bool:
        return self._value == item

    def expects(self, msg: str) -> T:
        return self._value

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default: T) -> T:
        return self._value

    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        return self._value

    def map(self, f: Callable[[T], U]) -> Maybe[U]:
        return Something(f(self._value))

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return f(self._value)

    def map_or_else(self, default: Callable[[], U], f: Callable[[T], U]) -> U:
        return f(self._value)

    def iter(self) -> Iterator[T]:
        return iter([self._value])

    def filter(self, predicate: Callable[[T], bool]) -> Maybe[T]:
        return self if predicate(self._value) else Nothing()

    def ok_or(self, err: E) -> "Result[T, E]":
        return Ok(self._value)

    def ok_or_else(self, err: Callable[[], E]) -> "Result[T, E]":
        return Ok(self._value)

    def and_then(self, f: Callable[[T], Maybe[T]]) -> Maybe[T]:
        return f(self._value)

    def or_else(self, f: Callable[[], Maybe[T]]) -> Maybe[T]:
        return self

    def xor(self, other: Maybe[T]) -> Maybe[T]:
        match other:
            case Something():
                return Nothing()
            case Nothing():
                return self
            case _:
                raise TypeError("called `xor` with a type other than `Maybe`")

    def zip(self, other: Maybe[U]) -> Maybe[tuple[T, U]]:
        match (self, other):
            case (Something(s), Something(o)):
                return Something((s, o))
            case _:
                return Nothing()

    def zip_with(self, other: Maybe[U], f: Callable[[tuple[T, U]], R]) -> Maybe[R]:
        match (self, other):
            case (Something(s), Something(o)):
                return Something(f((s, o)))
            case _:
                return Nothing()

    def flatten_one(self) -> Maybe[T]:
        match self._value:
            case Something():
                return self._value
            case Nothing():
                return Nothing()
            case _:
                return self

    def flatten(self) -> Maybe[T]:
        current = self
        while True:
            match current._value:
                case Something():
                    current = current._value
                case Nothing():
                    return Nothing()
                case _:
                    break
        return current

    def transpose(self) -> "Result[Maybe[T], E]":
        match self._value:
            case Ok(inner):
                return Ok(Something(inner))
            case Err(err):
                return Err(err)
            case _:
                raise TypeError(
                    "called `transpose` on a `Something` value that is not a `Result`"
                )

    def __bool__(self) -> bool:
        return True

    def __contains__(self, item: T) -> bool:
        return self._value == item

    def __iter__(self) -> Iterator[T]:
        return iter([self._value])

    def __eq__(self, other: object) -> bool:
        match other:
            case Something(value):
                return bool(self._value == value)
            case _:
                return False


@attrs.frozen
class Nothing(Maybe[T]):
    def is_something(self) -> bool:
        return False

    def is_nothing(self) -> bool:
        return True

    def contains(self, item: T) -> bool:
        return False

    def expects(self, msg: str) -> T:
        raise UnwrapError(msg)

    def unwrap(self) -> T:
        raise UnwrapError("called `unwrap` on a `Nothing` value")

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        return f()

    def map(self, f: Callable[[T], U]) -> Maybe[U]:
        return Nothing()

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return default

    def map_or_else(self, default: Callable[[], U], f: Callable[[T], U]) -> U:
        return default()

    def iter(self) -> Iterator[T]:
        return iter([])

    def filter(self, predicate: Callable[[T], bool]) -> Maybe[T]:
        return self

    def ok_or(self, err: E) -> "Result[T, E]":
        return Err(err)

    def ok_or_else(self, err: Callable[[], E]) -> "Result[T, E]":
        return Err(err())

    def and_then(self, f: Callable[[T], Maybe[T]]) -> Maybe[T]:
        return self

    def or_else(self, f: Callable[[], Maybe[T]]) -> Maybe[T]:
        return f()

    def xor(self, other: Maybe[T]) -> Maybe[T]:
        return other if other.is_something() else Nothing()

    def zip(self, value: Maybe[U]) -> Maybe[tuple[T, U]]:
        return Nothing()

    def zip_with(self, other: Maybe[U], f: Callable[[tuple[T, U]], R]) -> Maybe[R]:
        return Nothing()

    def flatten_one(self) -> Maybe[T]:
        return self

    def flatten(self) -> Maybe[T]:
        return self

    def transpose(self) -> "Result[Maybe[T], E]":
        return Ok(self)

    def __bool__(self) -> bool:
        return False

    def __contains__(self, item: T) -> bool:
        return False

    def __iter__(self) -> Iterator[T]:
        return iter([])

    def __eq__(self, other: object) -> bool:
        match other:
            case Nothing():
                return True
            case _:
                return False


@runtime_checkable
class Result(Protocol[T, E]):
    def is_ok(self) -> bool: ...
    def is_err(self) -> bool: ...
    def contains(self, value: T) -> bool: ...
    def contains_err(self, err: E) -> bool: ...
    def ok(self) -> Maybe[T]: ...
    def err(self) -> Maybe[E]: ...
    def map(self, f: Callable[[T], U]) -> "Result[U, E]": ...
    def map_or(self, default: U, f: Callable[[T], U]) -> U: ...
    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U: ...
    def map_err(self, f: Callable[[E], U]) -> "Result[T, U]": ...
    def iter(self) -> Iterator[T]: ...
    def and_then(self, f: Callable[[T], "Result[T, E]"]) -> "Result[T, E]": ...
    def or_else(self, f: Callable[[E], U]) -> "Result[T, U]": ...
    def unwrap(self) -> T: ...
    def unwrap_or(self, default: T) -> T: ...
    def unwrap_or_else(self, default: Callable[[], T]) -> T: ...
    def expect(self, msg: str) -> T: ...
    def unwrap_err(self) -> E: ...
    def expect_err(self, msg: str) -> E: ...
    def flatten_one(self) -> "Result[T, E]": ...
    def flatten(self) -> "Result[T, E]": ...
    def transpose(self) -> Maybe["Result[T, E]"]: ...
    def __bool__(self) -> bool: ...
    def __contains__(self, item: T) -> bool: ...
    def __iter__(self) -> Iterator[T]: ...
    def __eq__(self, other: object) -> bool: ...


@attrs.frozen
class Ok(Result[T, E]):
    _value: T

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def contains(self, value: T) -> bool:
        return self._value == value

    def contains_err(self, err: E) -> bool:
        return False

    def ok(self) -> Maybe[T]:
        return Something(self._value)

    def err(self) -> Maybe[E]:
        return Nothing()

    def map(self, f: Callable[[T], U]) -> Result[U, E]:
        return Ok(f(self._value))

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return f(self._value)

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        return f(self._value)

    def map_err(self, f: Callable[[E], U]) -> Result[T, U]:
        return Ok(self._value)

    def iter(self) -> Iterator[T]:
        return iter([self._value])

    def and_then(self, f: Callable[[T], Result[T, E]]) -> Result[T, E]:
        return f(self._value)

    def or_else(self, f: Callable[[E], U]) -> Result[T, U]:
        return Ok(self._value)

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default: T) -> T:
        return self._value

    def unwrap_or_else(self, default: Callable[[], T]) -> T:
        return self._value

    def expect(self, msg: str) -> T:
        return self._value

    def unwrap_err(self) -> E:
        raise UnwrapError("called `unwrap_err` on an `Ok` value")

    def expect_err(self, msg: str) -> E:
        raise UnwrapError("called `expect_err` on an `Ok` value")

    def flatten_one(self) -> Result[T, E]:
        match self._value:
            case Ok():
                return self._value
            case Err():
                return self._value
            case _:
                return self

    def flatten(self) -> Result[T, E]:
        current = self
        while True:
            match current._value:
                case Ok():
                    current = current._value
                case Err():
                    return current._value
                case _:
                    break
        return current

    def transpose(self) -> Maybe[Result[T, E]]:
        match self._value:
            case Something(inner):
                return Something(Ok(inner))
            case _:
                return Nothing()

    def __bool__(self) -> bool:
        return True

    def __contains__(self, item: T) -> bool:
        return self._value == item

    def __iter__(self) -> Iterator[T]:
        return iter([self._value])

    def __eq__(self, other: object) -> bool:
        match other:
            case Ok(value):
                return bool(self._value == value)
            case _:
                return False


@attrs.frozen
class Err(Result[T, E]):
    _error: E

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def contains(self, value: T) -> bool:
        return False

    def contains_err(self, err: E) -> bool:
        return self._error == err

    def ok(self) -> Maybe[T]:
        return Nothing()

    def err(self) -> Maybe[E]:
        return Something(self._error)

    def map(self, f: Callable[[T], U]) -> Result[U, E]:
        return Err(self._error)

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return default

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        return default(self._error)

    def map_err(self, f: Callable[[E], U]) -> Result[T, U]:
        return Err(f(self._error))

    def iter(self) -> Iterator[T]:
        return iter([])

    def and_then(self, f: Callable[[T], Result[T, E]]) -> Result[T, E]:
        return self

    def or_else(self, f: Callable[[E], U]) -> Result[T, U]:
        return Err(f(self._error))

    def unwrap(self) -> NoReturn:
        raise UnwrapError("called `unwrap` on an `Err` value")

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, default: Callable[[], T]) -> T:
        return default()

    def expect(self, msg: str) -> T:
        raise UnwrapError(msg)

    def unwrap_err(self) -> E:
        return self._error

    def expect_err(self, msg: str) -> E:
        return self._error

    def flatten_one(self) -> Result[T, E]:
        return self

    def flatten(self) -> Result[T, E]:
        return self

    def transpose(self) -> Maybe[Result[T, E]]:
        return Something(self)

    def __bool__(self) -> bool:
        return False

    def __contains__(self, item: T) -> bool:
        return False

    def __iter__(self) -> Iterator[T]:
        return iter([])

    def __eq__(self, other: object) -> bool:
        match other:
            case Err(error):
                return bool(self._error == error)
            case _:
                return False
