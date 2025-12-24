from io import StringIO
import sys

TOOL_NAME = "python_repl"

class PythonREPL:
    """Simulates a standalone Python REPL with persistent globals."""

    def __init__(self) -> None:
        self._globals: dict = {}

    def run(self, command: str) -> str:
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            exec(command, self._globals)
            sys.stdout = old_stdout
            output = mystdout.getvalue()
        except Exception as exc:
            sys.stdout = old_stdout
            output = str(exc)
        if output.strip() == "":
            return "[no output] Python実行完了。実行結果を取得した場合は、printを利用してください。"
        return output


def python_repl(command: str) -> str:
    return _PYTHON_REPL.run(command)

_PYTHON_REPL = PythonREPL()
