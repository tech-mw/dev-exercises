🛠️**進行中 – 定期的なアップデートと継続的な改善が計画されています**🛠️

## 利用技術
[![My Skills](https://skillicons.dev/icons?i=python,django,fastapi,nodejs,express,mysql,docker,redis,bash,git)](https://skillicons.dev)

## リポジトリ構成

<pre>
PJ/
├── 01_basics/ 
│    ├─── docker
│    │     ├── 01-fastapi-single
│    │     ├── 02_environments
│    │     ├── 03-init-mysql
│    │     └── 04-python-redis
│    ├─── git
│    │     ├── 01-detached-non-fast-forward
│    │     └── 02-detached-fast-forward
│    └─── mysql
│          └── 01-ebook-schema-sql
├── 02_environments/
└── 03_webapps/
</pre>
---
## 1. 01_basics
- python、dockerなど最小構成を通して仕組みを体系的に実演するセクション

### 1-1. docker
#### 1-1-1. [01-fastapi-single](./01_basics/docker/01-fastapi-single/README.md)
- FastAPIをPython公式イメージで最小構成Docker化 
- 特徴
  - uvicorn実行
  - シンプルなエンドポイント
#### 1-1-2. [02_environments](./01_basics/docker/02-node-express-api/README.md)
- Node.js（Expressアプリ）を公式NodeイメージでDocker化
- 特徴
  - 開発用にnodemonホットリロード対応
  - バインドマウントでホストソースを即反映
  - venvなど不要ファイルを含めない構造を推奨
#### 1-1-3. [03-init-mysql](./01_basics/docker/03-init-mysql/README.md)
- Mysqlを公式MysqlイメージでDocker化
- 特徴
  - 初期化用SQLをinitdb.dに置くだけで自動実行
  - ホスト側のSQLファイルをバインドマウントして管理
#### 1-1-4. [04-python-redis](./01_basics/docker/04-python-redis/README.md)
- Python+Redis公式イメージでDocker化
- 特徴
  - redisコンテナ作成時に初期データ登録

### 1-2. git
#### 1-2-1. [01-detached-non-fast-forward](01_basics/git/01-detached-non-fast-forward/README.md)
- detached HEAD状態の動作検証：non-fast-forward
- 特徴
  - HEADの仕組みと挙動を理解するために、意図的に detached HEAD × non-fast-forward にして検証 
  - TerminalとSourceTreeでの表示の違いを比較（各状態でTerminalとSourceTreeそれぞれの表示画面をスクリーンショット）

#### 1-2-2. [02-detached-fast-forward](01_basics/git/02-detached-fast-forward/README.md)
- detached HEAD状態の動作検証：fast-forward
- 特徴
  - HEADの仕組みと挙動を理解するために、意図的に detached HEAD × fast-forward にして検証
  - TerminalとSourceTreeでの表示の違いを比較（各状態でTerminalとSourceTreeそれぞれの表示画面をスクリーンショット）

### 1-3. mysql
#### 1-3-1. [01-ebook-schema-sql](01_basics/mysql/README.md)
- Mysqlを公式イメージでDocker化、簡易的な電子書籍アプリを想定したモデルとSQLサンプル
- 特徴
  - ユーザー情報、書籍情報、書籍購入履歴、書籍閲覧履歴 4つのテーブルとサンプルデータを流し込み、初期構築
  - [期間内に特定の出版社を書籍を購入した累計額をユーザー毎に集計]など実務的なSQLサンプル

---
## 2. 02_environments
- 環境構築系セクション（複数サービス連携やCI/CDなど）
---
## 3. 03_webapps
- Webアプリ開発セクション