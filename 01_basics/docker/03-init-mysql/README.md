# Init-Mysql Docker 最小サンプル

Mysqlを公式イメージでDocker化する最小構成例です。
（初期データを流し込みます）

---

## 環境
- Mysql: latest（開発用例。実際はバージョン固定推奨：例 mysql:8.0）
- Docker: 20.10以上

---

## ファイル構成
<pre>
PJ
├── README.md
├── docker-compose.yml
└── initdb.d
    └── init_data.sql
</pre>

---
## イメージ作成+コンテナ起動
```bash
docker compose up
```
## コンテナ側のマウント対象ディレクトリ+ファイル確認
- mysqlのデータ保存場所は`/var/lib/mysql` 
```bash
docker exec -it test_mysql_container bash -c "cd /docker-entrypoint-initdb.d && cat init_data.sql"
```

## コンテナ接続＋mysql接続
- passwordはcomposeで指定したroot
```bash
docker exec -it test_mysql_container mysql -u root -p
```
## （mysql）DB一覧確認
- 初期データで作成したsampleが存在している事が確認できる
```bash
show databases;
```

## （mysql）DB切替
```bash
use sample;
```

## （mysql）データ一覧確認
- 初期データで作成した2件のデータが存在している事が確認できる
```bash
select * from employee;
```

## コンテナ停止/削除+イメージ削除
- 既存のDBデータも削除して初期化したい場合
  - init_data.sqlを修正後に反映させたい場合は、既存のDBデータを削除する必要があります
  - initdb.dに置いたSQLは初回起動時にのみ実行され、既存のデータがある場合はスキップされます
  - 既存のDBデータを残したい場合は`-v`不要です
```bash
docker compose down -v && docker rmi mysql
```