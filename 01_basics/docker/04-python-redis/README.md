# Python-Redis Docker 最小サンプル
Python+Redis公式イメージでDocker化する最小構成例です。
（pythonで初期データをredisに登録します）

---

## 環境
- Python: 3.10
- Mysql: latest（開発用例。実際はバージョン固定推奨：例 mysql:8.0）
- Docker: 20.10以上

---

## ファイル構成
<pre>
PJ
├── README.md
├── app
│    ├── Dockerfile
│    └── sample_redis.py
└── docker-compose.yml
</pre>

## コンテナ起動
```bash
docker compose up
```

## redis接続
```bash
redis-cli -p 6379 --raw
```

### （redis）key確認
```bash
keys *
```

### （redis）データ確認
```bash
hgetall りんご
```

### （redis）停止
```bash
shutdown
```

###  コンテナ停止+削除
```bash
docker compose down
```

###  イメージ削除
```bash
docker rmi build_app redis
```