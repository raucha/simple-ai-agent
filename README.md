# Simple AI Agent

## Setup

```bash
uv sync

mv .env.example .env
nano .env
## Add below API keys
# TAVILY_API_KEY=
# OPEN_AI_API_KEY=
```

## Run

```bash
# 計算させる
uv run python -m src.agent "フィボナッチ数の30番目の数字を計算して"

# 調べ物をさせる
uv run python -m src.agent "明日の天気を教えて"
```

## 実行結果例
<!-- <details>
<summary>フィボナッチ数を計算させる</summary>

```bash
uv run python -m src.agent "フィボナッチ数の30番目の数字を計算して"
```

</details>


<details>
<summary>明日の天気を教えて</summary>

```bash
uv run python -m src.agent "明日の天気を教えて"
```

</details> -->


<details>
<summary>モンテカルロ法で確率計算</summary>

```bash
uv run python -m src.agent "サイコロを 2 個振って合計 が 12 以上になる確率を厳密計算とモンテカルロ法の両方で求めて"

==== Start STEP 1 ====
Processing tool action.
TOOL CALL: python_repl(# サイコロ2個の合計が12以上になる確率（厳密計算）
# サイコロは6面なので、2個振ると出る目の合計は2～12
# それぞれの目の出る組み合わせを数える

total = 0
success = 0
for i in range(1, 7):
    for j in range(1, 7):
        total += 1
        if i + j >= 12:
            success += 1
exact_prob = success / total
print(exact_prob)
)
TOOL OUTPUT (preview): 0.027777777777777776


==== Start STEP 2 ====
Processing tool action.
TOOL CALL: python_repl(import random
# モンテカルロ法でサイコロ2個の合計が12以上になる確率を推定
trials = 1000000
success = 0
for _ in range(trials):
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    if dice1 + dice2 >= 12:
        success += 1
monte_carlo_prob = success / trials
print(monte_carlo_prob)
)
TOOL OUTPUT (preview): 0.027617


==== Start STEP 3 ====
Processing final action.
サイコロを2個振って合計が12以上になる確率は、

・厳密計算では約0.0278（=2.78%）
・モンテカルロ法による推定では約0.0276（=2.76%）

となります。どちらもほぼ同じ値で、サイコロ2個で合計12以上（つまり12のみ）は非常にまれなことが分かります。
```

</details>



<details>
<summary>irisのデータセットを取得して画像として可視化</summary>

```bash
uv add matplotlib pandas
uv run python -m src.agent "ユリのデータセットを取得して、各特徴量をヒストグラムとして画像化して"

==== Start STEP 1 ====
Processing tool action.
TOOL CALL: tavily_search(ユリ データセット ダウンロード)
TOOL OUTPUT (preview): - データセットをダウンロードできるサイト : r/data

==== Start STEP 2 ====
Processing tool action.
TOOL CALL: tavily_search(iris データセット 特徴量)
TOOL OUTPUT (preview): - Iris データセットの探索的データ分析
  https

==== Start STEP 3 ====
Processing tool action.
TOOL CALL: tavily_search(iris データセット ダウンロード csv)
TOOL OUTPUT (preview): - Irisデータセットのダウンロード | Excel VB

==== Start STEP 4 ====
Processing tool action.
TOOL CALL: python_repl(import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# irisデータセットをseabornから直接取得
iris = sns.load_dataset('iris')

# 特徴量ごとにヒストグラムを描画
features = iris.columns[:-1]
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes = axes.flatten()
for i, feature in enumerate(features):
    sns.histplot(iris[feature], kde=True, ax=axes[i])
    axes[i].set_title(f'{feature} histogram')
plt.tight_layout()
plt.savefig('iris_histograms.png')
print('iris_histograms.png'))
TOOL OUTPUT (preview): No module named 'seaborn'

==== Start STEP 5 ====
Processing tool action.
TOOL CALL: python_repl(import pandas as pd
import matplotlib.pyplot as plt

# seabornが使えないので、pandasでirisデータセットを取得
url = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv'
iris = pd.read_csv(url)

# 特徴量ごとにヒストグラムを描画
features = iris.columns[:-1]
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes = axes.flatten()
for i, feature in enumerate(features):
    axes[i].hist(iris[feature], bins=20, color='skyblue', edgecolor='black')
    axes[i].set_title(f'{feature} histogram')
plt.tight_layout()
plt.savefig('iris_histograms.png')
print('iris_histograms.png'))
TOOL OUTPUT (preview): iris_histograms.png


==== Start STEP 6 ====
Processing final action.
Iris（アヤメ）データセットの各特徴量（sepal_length, sepal_width, petal_length, petal_width）についてヒストグラムを作成し、1枚の画像（iris_histograms.png）として保存しました。この画像には4つの特徴量それぞれの分布が表示されています。ご希望のヒストグラム画像は『iris_histograms.png』です。
```
![Iris Histograms](doc/iris_histograms.png)


</details>