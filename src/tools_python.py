from io import StringIO
import sys

TOOL_NAME = "python_repl"

class PythonREPL:
    """Simulates a standalone Python REPL with persistent globals."""

    def __init__(self) -> None: 
        # Pythonインタプリタ内でグローバル変数を保持するための辞書を作成
        self._globals: dict = {}

    def run(self, command: str) -> str:
        # 標準出力先を退避
        old_stdout = sys.stdout
        
        # 標準出力をmystdoutに流し込む
        sys.stdout = mystdout = StringIO()
        try:
            exec(command, self._globals)

            # 標準出力先を復元
            sys.stdout = old_stdout

            # exec処理内のprint出力を取得
            output = mystdout.getvalue()
        except Exception as exc:
            sys.stdout = old_stdout
            output = str(exc)
        if output.strip() == "":
            return "[no output] Python実行完了。実行結果を取得した場合は、printを利用してください。"
        
        # exec処理内のprint出力を返す
        return output


def python_repl(command: str) -> str:
    return _PYTHON_REPL.run(command)

_PYTHON_REPL = PythonREPL()
