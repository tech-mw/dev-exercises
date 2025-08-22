# Stable Diffusion CLI Sample (Python)

AI画像生成ライブラリ「Stable Diffusion」を使用したミニマムなPython CLI サンプルです

---

## 概要
- Stable Diffusion（diffusers）を利用して画像を生成する最小スクリプト
- 日本語で入力したプロンプトを自動的に英語へ翻訳してから生成  
  （`--no_translate` オプションで翻訳をスキップ可能）
- option指定可：サイズ（縦/横）、出力ファイル名、出力フォーマット(jpg or png)、出力ディレクトリ、翻訳有無切替
- height / width は 8 の倍数のみ許可
- 初回実行時はモデルがダウンロードされるため時間がかかる（2回目以降はキャッシュが効いて高速化）
---

## 環境
- Python3.12
---

## 環境作成
このプロジェクトは **Python 3.12 系** を前提としています。  
（3.13 以降は一部ライブラリが対応していないため、今回は 3.12 系を利用しています）

### Python 3.12 を有効にする方法
#### pyenv を利用する場合
```bash
# インストール可能な Python バージョン一覧を確認
$ pyenv install -l | grep 3.12

# Python 3.12 系をインストール（例：3.12.6）
$ pyenv install 3.12.6

# カレントディレクトリの Python バージョンを指定
$ pyenv local 3.12.6

# バージョン確認
$ python3 --version
Python 3.12.6
```

### 仮想環境作成
```bash
$ python3 -m venv venv
```

### 仮想環境activate
```bash
$ source ./venv/bin/activate
```

### requirement.txt作成
```
certifi==2024.8.30
charset-normalizer==3.3.2
diffusers==0.30.3
filelock==3.16.1
fsspec==2024.9.0
huggingface-hub==0.25.0
idna>=2.5,<4
importlib_metadata==8.5.0
Jinja2==3.1.4
MarkupSafe==2.1.5
mpmath==1.3.0
networkx==3.3
numpy==1.26.4
packaging==24.1
pillow==10.4.0
PyYAML==6.0.2
regex==2024.9.11
requests==2.32.3
safetensors==0.4.5
sympy==1.13.2
tokenizers==0.19.1
torch==2.2.2
tqdm==4.66.5
transformers==4.44.2
typing_extensions==4.12.2
urllib3==2.2.3
zipp==3.20.2
googletrans==4.0.0-rc1
accelerate==0.34.2
```

### 依存関係インストール
```bash
$ pip install -r requirements.txt
```

## 使い方
```
usage: app.py [-h] [--height HEIGHT] [--width WIDTH] [--filename FILENAME]
              [--img_format {png,jpg}] [--output_dir OUTPUT_DIR] [--no_translate]

Stable Diffusionで画像を生成します

options:
  -h, --help            show this help message and exit
  --height HEIGHT       生成画像の高さ（8で割り切れる必要があります）
  --width WIDTH         生成画像の幅（8で割り切れる必要があります）
  --filename FILENAME   出力ファイル名
  --img_format {png,jpg}
                        出力フォーマット
  --output_dir OUTPUT_DIR
                        出力先ディレクトリ（存在しない場合は自動作成）
  --no_translate        翻訳を行わず、入力文字列をそのまま使用する
  
  
実行例（翻訳有/サイズ指定無/PNG）：$ python3 app.py --img_format png --filename sample
実行例（翻訳無/サイズ指定有/JPG）：$ python3 app.py --no_translate --width 80 --height 80 --img_format jpg --filename sample
```

## サンプル画像
### 例1
```
A smiling junior high school student
（笑顔の中学生）
```
![サンプル画像1](./images/sample01.png)

### 例2
```
High school students working up a refreshing sweat during morning practice during summer vacation
（夏休みの朝練習で爽やかな汗を流す高校生たち）
```
![サンプル画像2](./images/sample02.png)