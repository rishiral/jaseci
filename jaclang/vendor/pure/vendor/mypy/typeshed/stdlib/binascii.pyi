import sys
from _typeshed import ReadableBuffer
from typing_extensions import TypeAlias

# Many functions in binascii accept buffer objects
# or ASCII-only strings.
_AsciiBuffer: TypeAlias = str | ReadableBuffer

def a2b_uu(__data: _AsciiBuffer) -> bytes: ...
def b2a_uu(__data: ReadableBuffer, *, backtick: bool = False) -> bytes: ...

if sys.version_info >= (3, 11):
    def a2b_base64(__data: _AsciiBuffer, *, strict_mode: bool = False) -> bytes: ...

else:
    def a2b_base64(__data: _AsciiBuffer) -> bytes: ...

def b2a_base64(__data: ReadableBuffer, *, newline: bool = True) -> bytes: ...
def a2b_qp(data: _AsciiBuffer, header: bool = False) -> bytes: ...
def b2a_qp(
    data: ReadableBuffer,
    quotetabs: bool = False,
    istext: bool = True,
    header: bool = False,
) -> bytes: ...

if sys.version_info < (3, 11):
    def a2b_hqx(__data: _AsciiBuffer) -> bytes: ...
    def rledecode_hqx(__data: ReadableBuffer) -> bytes: ...
    def rlecode_hqx(__data: ReadableBuffer) -> bytes: ...
    def b2a_hqx(__data: ReadableBuffer) -> bytes: ...

def crc_hqx(__data: ReadableBuffer, __crc: int) -> int: ...
def crc32(__data: ReadableBuffer, __crc: int = 0) -> int: ...
def b2a_hex(
    data: ReadableBuffer, sep: str | bytes = ..., bytes_per_sep: int = ...
) -> bytes: ...
def hexlify(
    data: ReadableBuffer, sep: str | bytes = ..., bytes_per_sep: int = ...
) -> bytes: ...
def a2b_hex(__hexstr: _AsciiBuffer) -> bytes: ...
def unhexlify(__hexstr: _AsciiBuffer) -> bytes: ...

class Error(ValueError): ...
class Incomplete(Exception): ...
