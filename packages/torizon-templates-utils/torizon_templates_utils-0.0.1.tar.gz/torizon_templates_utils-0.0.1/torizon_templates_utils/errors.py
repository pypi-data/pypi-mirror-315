
import sys
from enum import Enum
from torizon_templates_utils.colors import Color, BgColor, print

class _error_struct:
    code: int
    message: str

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


class Error(Enum):
    ENOPKG = _error_struct(
        65, "Package not installed"
    )
    EUSER = _error_struct(
        69, "User fault"
    )
    ENOCONF = _error_struct(
        1, "Not configured"
    )
    ENOFOUND = _error_struct(
        404, "Not found"
    )


def Error_Out(msg: str, error: Error) -> None:
    print(f"\n{msg}", color=Color.RED)
    print(f"Error cause: {error.value.message}\n", color=Color.RED)
    sys.exit(error.value.code)

def last_return_code() -> int:
    # we are ignoring the type here because this will get the current
    # xonsh shell instance
    return __xonsh__.last.returncode # type: ignore
