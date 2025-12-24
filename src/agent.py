import json
import sys

from dotenv import load_dotenv

from .llm import call_llm
from .tools_python import TOOL_NAME as PYTHON_REPL_NAME
from .tools_python import python_repl
from .tools_tavily import TOOL_NAME as TAVILY_NAME
from .tools_tavily import tavily_search

TOOLS = {
    TAVILY_NAME: tavily_search,
    PYTHON_REPL_NAME: python_repl,
}

from datetime import datetime


SYSTEM_PROMPT = """あなたは親切なAIアシスタントです。
必要に応じてtoolを呼び出し、十分な情報が揃ったら最終回答してください。
以下にユーザー入力と前回までのツール実行結果が記載されたscratchpadが与えられます。

使用可能なtool:
- tavily_search: 
  - 概要: web検索を実行します。
  - 利用するシーン: WEBから情報を収集する必要がある場合に利用してください。
  - 引数: 検索キーワードを文字列で指定します。
  - 戻り値: 検索結果の文字列が返されます。
- python_repl: 
  - 概要: pythonコードを実行します。
  - 利用するシーン: 数字の計算を行う場合に必ず利用してください。
  - 引数: pythonスクリプト。実行結果を取得するにはprintで値を出力してください。
  - 戻り値: 実行結果の文字列が返されます。

ルール:
- 新しい情報が必要ならtoolを使う。
- actionは1つのみ。
- 出力は必ずJSON 1つだけで、余計なテキストは出力しない。
  - actionは必ず "tool" または "final" のどちらかです。

今日の日時:
{datetime}

出力JSONスキーマ:
下記のいずれか1つ
- {{"action":"tool","tool":"tavily_search","input":"..."}}
- {{"action":"final","output":"..."}}

User Input: {user_query}
Scratchpad :
{scratchpad}
"""


def run_agent(user_query: str) -> str:
    scratchpad: list[dict] = []

    max_steps = 10
    for step in range(1, max_steps + 1):
        print(f"\n==== Start STEP {step} ====")
        
        prompt = SYSTEM_PROMPT.format(
            datetime=datetime.now(),
            user_query=user_query,
            scratchpad=json.dumps(scratchpad, ensure_ascii=False, indent=2),
        )
        raw = call_llm(prompt)
        action = json.loads(raw)

        if action.get("action") == "tool":
            print(f"Processing tool action.")

            tool_name = action.get("tool")
            tool_input = action.get("input", "")
            tool_func = TOOLS.get(tool_name)
            
            print(f"TOOL CALL: {tool_name}({tool_input})")
            tool_output = tool_func(tool_input)
            print(f"TOOL OUTPUT (preview): {tool_output[:30]}")
            
            scratchpad.append(
                {
                    "action": "tool",
                    "tool": tool_name,
                    "input": tool_input,
                    "observation": tool_output,
                }
            )
            continue

        if action.get("action") == "final":
            print(f"Processing final action.")
            return str(action.get("output", "")).strip()

        # print(f"[step {step}] invalid action: {action}")

        scratchpad.append({"error": f"Unknown action: {action.get('action')}"})

    return "Max steps reached without a final answer."


def main() -> int:
    load_dotenv()
    if len(sys.argv) < 2:
        print("Usage: python -m src.agent \"your question\"")
        return 1

    user_query = " ".join(sys.argv[1:])
    answer = run_agent(user_query)
    print(answer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
