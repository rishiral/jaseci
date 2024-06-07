from multiprocessing.connection import _Address
from queue import Queue
from types import TracebackType
from typing import Any
from typing_extensions import Self

__all__ = ["Client", "Listener", "Pipe"]

families: list[None]

class Connection:
    _in: Any
    _out: Any
    recv: Any
    recv_bytes: Any
    send: Any
    send_bytes: Any
    def __enter__(self) -> Self: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...
    def __init__(self, _in: Any, _out: Any) -> None: ...
    def close(self) -> None: ...
    def poll(self, timeout: float = 0.0) -> bool: ...

class Listener:
    _backlog_queue: Queue[Any] | None
    @property
    def address(self) -> Queue[Any] | None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...
    def __init__(
        self,
        address: _Address | None = None,
        family: int | None = None,
        backlog: int = 1,
    ) -> None: ...
    def accept(self) -> Connection: ...
    def close(self) -> None: ...

def Client(address: _Address) -> Connection: ...
def Pipe(duplex: bool = True) -> tuple[Connection, Connection]: ...
