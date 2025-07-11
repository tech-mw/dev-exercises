# FastAPI Docker 最小サンプル

FastAPIアプリをPython公式イメージでDocker化する最小構成例です。

---

## 環境
- Python: 3.13-slim（Docker公式イメージ）
- Docker: 20.10以上

---

## ファイル構成
```
.
├── Dockerfile
├── main.py
└── requirements.txt
```

---

## イメージ作成
- `docker build -t [任意：イメージ名] .`
```bash
docker build -t fastapi-docker .
```

---

## コンテナ起動
- Dockerfileでuvicornのポートを8000に指定しているため8000:8000とする
- `[ホスト側ポート番号]:[コンテナ側ポート番号] --name [任意：コンテナ名] [使用イメージ名]`
- `docker run -d -p [ホスト側ポート番号]:[コンテナ側ポート番号] --name [任意：コンテナ名] [使用イメージ名]`

```bash
docker run -d -p 8000:8000 --name fastapi-docker-container fastapi-docker
```

---

## ブラウザアクセス
`http://localhost:8000/` にアクセスすると「Hello FastAPI」と表示されます。

---

## コンテナ接続＋生成ファイル確認
- main.py と requirements.txt の2ファイルがコンテナ内に存在していることが確認できます。
```bash
docker exec -it fastapi-docker-container bash -c "ls -la"
```

---

## コンテナ停止 + 削除、イメージ削除
```bash
docker stop fastapi-docker-container && \
docker rm fastapi-docker-container && \
docker rmi fastapi-docker
```

---

## 補足
- ENV PYTHONDONTWRITEBYTECODE=1 を指定し、.pycファイルや__pycache__を生成しないようにしています。
- これにより不要なキャッシュを含まないクリーンな本番用イメージを作成できます。
- このDockerイメージはPython 3.13に固定しているため差分は出ませんが、ローカル環境とDockerfileでPythonのバージョンが異なる場合、pip install時に差分が出ることがあります。
