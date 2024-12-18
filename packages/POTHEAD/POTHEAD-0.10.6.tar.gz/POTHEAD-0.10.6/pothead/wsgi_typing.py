# Thanks to https://gist.github.com/dahlia/e618b303ab64c0e7e32b1f7957ca283a#file-wsgi_typing-py

import types
from typing import Any, Callable, Iterable, Mapping, Optional, Sequence, Tuple

__all__ = (
    "Environ",
    "ExcInfo",
    "ResponseStream",
    "StartResponse",
    "WriteCallable",
    "WsgiApplication",
)


# https://www.python.org/dev/peps/pep-3333/#the-write-callable
WriteCallable = Callable[[bytes], Any]

# https://docs.python.org/3/library/sys.html#sys.exc_info
ExcInfo = Tuple[type, BaseException, types.TracebackType]

# https://www.python.org/dev/peps/pep-3333/#the-start-response-callable
StartResponse = Callable[
    [
        str,  # status
        Sequence[Tuple[str, str]],  # response headers
        Optional[ExcInfo],  # exc_info
    ],
    WriteCallable,  # write() callable
]

# https://www.python.org/dev/peps/pep-3333/#environ-variables
Environ = Mapping[str, object]

# https://www.python.org/dev/peps/pep-3333/#buffering-and-streaming
ResponseStream = Iterable[bytes]

# https://www.python.org/dev/peps/pep-3333/#specification-details
WsgiApplication = Callable[
    [
        Environ,  # environ
        StartResponse,  # start_response() function
    ],
    ResponseStream,  # bytestring chunks
]
