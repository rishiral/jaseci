from _typeshed import Incomplete, SupportsGetItem, SupportsLenAndGetItem, Unused
from abc import abstractmethod
from collections.abc import Iterable, Iterator, MutableSequence
from typing import Final
from typing_extensions import Self, TypeAlias

from .fixer_base import BaseFix
from .pgen2.grammar import Grammar

_NL: TypeAlias = Node | Leaf
_Context: TypeAlias = tuple[str, int, int]
_Results: TypeAlias = dict[str, _NL]
_RawNode: TypeAlias = tuple[int, str, _Context, list[_NL] | None]

HUGE: Final = 0x7FFFFFFF

def type_repr(type_num: int) -> str | int: ...

class Base:
    type: int
    parent: Node | None
    prefix: str
    children: list[_NL]
    was_changed: bool
    was_checked: bool
    def __eq__(self, other: object) -> bool: ...
    @abstractmethod
    def _eq(self, other: Base) -> bool: ...
    @abstractmethod
    def clone(self) -> Self: ...
    @abstractmethod
    def post_order(self) -> Iterator[Self]: ...
    @abstractmethod
    def pre_order(self) -> Iterator[Self]: ...
    def replace(self, new: _NL | list[_NL]) -> None: ...
    def get_lineno(self) -> int: ...
    def changed(self) -> None: ...
    def remove(self) -> int | None: ...
    @property
    def next_sibling(self) -> _NL | None: ...
    @property
    def prev_sibling(self) -> _NL | None: ...
    def leaves(self) -> Iterator[Leaf]: ...
    def depth(self) -> int: ...
    def get_suffix(self) -> str: ...

class Node(Base):
    fixers_applied: MutableSequence[BaseFix] | None
    # Is Unbound until set in refactor.RefactoringTool
    future_features: frozenset[Incomplete]
    # Is Unbound until set in pgen2.parse.Parser.pop
    used_names: set[str]
    def __init__(
        self,
        type: int,
        children: Iterable[_NL],
        context: Unused = None,
        prefix: str | None = None,
        fixers_applied: MutableSequence[BaseFix] | None = None,
    ) -> None: ...
    def _eq(self, other: Base) -> bool: ...
    def clone(self) -> Node: ...
    def post_order(self) -> Iterator[Self]: ...
    def pre_order(self) -> Iterator[Self]: ...
    def set_child(self, i: int, child: _NL) -> None: ...
    def insert_child(self, i: int, child: _NL) -> None: ...
    def append_child(self, child: _NL) -> None: ...
    def __unicode__(self) -> str: ...

class Leaf(Base):
    lineno: int
    column: int
    value: str
    fixers_applied: MutableSequence[BaseFix]
    def __init__(
        self,
        type: int,
        value: str,
        context: _Context | None = None,
        prefix: str | None = None,
        fixers_applied: MutableSequence[BaseFix] = [],
    ) -> None: ...
    def _eq(self, other: Base) -> bool: ...
    def clone(self) -> Leaf: ...
    def post_order(self) -> Iterator[Self]: ...
    def pre_order(self) -> Iterator[Self]: ...
    def __unicode__(self) -> str: ...

def convert(gr: Grammar, raw_node: _RawNode) -> _NL: ...

class BasePattern:
    type: int
    content: str | None
    name: str | None
    def optimize(
        self,
    ) -> (
        BasePattern
    ): ...  # sic, subclasses are free to optimize themselves into different patterns
    def match(self, node: _NL, results: _Results | None = None) -> bool: ...
    def match_seq(
        self, nodes: SupportsLenAndGetItem[_NL], results: _Results | None = None
    ) -> bool: ...
    def generate_matches(
        self, nodes: SupportsGetItem[int, _NL]
    ) -> Iterator[tuple[int, _Results]]: ...

class LeafPattern(BasePattern):
    def __init__(
        self,
        type: int | None = None,
        content: str | None = None,
        name: str | None = None,
    ) -> None: ...

class NodePattern(BasePattern):
    wildcards: bool
    def __init__(
        self,
        type: int | None = None,
        content: str | None = None,
        name: str | None = None,
    ) -> None: ...

class WildcardPattern(BasePattern):
    min: int
    max: int
    def __init__(
        self,
        content: str | None = None,
        min: int = 0,
        max: int = 0x7FFFFFFF,
        name: str | None = None,
    ) -> None: ...

class NegatedPattern(BasePattern):
    def __init__(self, content: str | None = None) -> None: ...

def generate_matches(
    patterns: SupportsGetItem[int | slice, BasePattern] | None,
    nodes: SupportsGetItem[int | slice, _NL],
) -> Iterator[tuple[int, _Results]]: ...
