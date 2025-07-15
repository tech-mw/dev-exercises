🛠️**進行中 – 定期的なアップデートと継続的な改善が計画されています**🛠️

## 利用技術
[![My Skills](https://skillicons.dev/icons?i=python,django,fastapi,nodejs,express,mysql,docker,redis,bash)](https://skillicons.dev)

## リポジトリ構成

<pre>
PJ/
├── 01_basics/ 
│    └── docker
│        ├── 01-fastapi-single
│        └── 02_environments
├── 02_environments/
└── 03_webapps/
</pre>

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
## 2. 02_environments
- 環境構築系セクション（複数サービス連携やCI/CDなど）
## 3. 03_webapps
- Webアプリ開発セクション