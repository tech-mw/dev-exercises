# Node-Express Docker 最小サンプル

Node.js（Expressアプリ）を公式NodeイメージでDocker化する最小構成例です。
（開発環境ではnodemonでホットリロード）

---

## 環境
- Node: 20（Docker公式イメージ）
- Docker: 20.10以上

---

## ファイル構成
<pre>
PJ
├─── src（マウント対象）
│     ├── Dockerfile
│     ├── main.js
│     ├── package-lock.json
│     └── package.json
└─── venv
</pre>

---
## 仮想環境作成+active
```bash
python3 -m venv venv
source ./venv/bin/activate
```

## マウント対象dic作成+移動
```bash
mkdir src
cd src
```
## npm初期化 + express、nodomonインストール
- nodemonは開発環境化でホットリロードするため
```bash
npm init -y && \
npm install express && \
npm install --save-dev nodemon
```

## build
```bash
docker build -t node-express-app .
```

## 起動 + バインドマウント
- ホスト側でマウントするのは「src」だけ
- PJを全てマウントすると venv など不要なディレクトリが含まれるため分けています
- [host-path] は自分の環境に合わせて書き換えてください
```bash
docker run -d --rm \
    -p 3000:3000 \
    -v [host-path]/02-node-express-api/src:/usr/src/app \
    --name node-express-app-container node-express-app 
```

## 確認
- ブラウザアクセス（下記アクセスで「node-express-app」表示）
```bash
http://localhost:3000/
```
- コンテナ側マウント内容
  - Dockerfile  main.js  node_modules  package-lock.json  package.jsonがマウントされている
```bash
docker exec -it node-express-app-container bash -c "ls"
```

## 停止+削除
- 起動時に`--rm`指定なのでコンテナ停止時にコンテナ削除もされる
```bash
docker stop node-express-app-container && \
docker rmi node-express-app
```