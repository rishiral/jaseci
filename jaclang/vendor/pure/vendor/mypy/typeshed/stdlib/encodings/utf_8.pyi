import codecs
from _typeshed import ReadableBuffer

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input: str, final: bool = False) -> bytes: ...

class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    @staticmethod
    def _buffer_decode(
        __data: ReadableBuffer, __errors: str | None = None, __final: bool = False
    ) -> tuple[str, int]: ...

class StreamWriter(codecs.StreamWriter):
    @staticmethod
    def encode(__str: str, __errors: str | None = None) -> tuple[bytes, int]: ...

class StreamReader(codecs.StreamReader):
    @staticmethod
    def decode(
        __data: ReadableBuffer, __errors: str | None = None, __final: bool = False
    ) -> tuple[str, int]: ...

def getregentry() -> codecs.CodecInfo: ...
def encode(__str: str, __errors: str | None = None) -> tuple[bytes, int]: ...
def decode(input: ReadableBuffer, errors: str | None = "strict") -> tuple[str, int]: ...
