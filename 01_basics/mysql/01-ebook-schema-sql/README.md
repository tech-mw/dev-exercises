# Ebook-Schema Mysql Docker

MySQL の公式イメージを用いて Docker 上に構築した、簡易的な電子書籍アプリを想定したデータモデルと SQL サンプルです。  
初期データも自動で流し込まれ、すぐに演習・検証が行えます。

---

## 概要
- MySQL（公式イメージ）を使用し、Docker で即起動できる構成
- 電子書籍アプリを想定した4つのテーブル：
  - ユーザー情報（users）
  - 書籍情報（books）
  - 書籍購入履歴（book_purchases）
  - 書籍閲覧履歴（book_views）
- 初期データを流し込み済み
- 実務的な SQL 演習付き
  - 例：**「期間内に特定の出版社の書籍を購入したユーザーごとの合計金額」**など

---

## 環境
- Mysql: 8.0
- Docker: 20.10以上
- SequelACE： Version 5.0.9

---

### SequelAceの設定
<pre>
接続方式タブ：TCP/IP
HOST:127.0.0.1
Username：development
Password：password
Database:（任意）
Port：4306

Preferences > 一般 > Default Encoding：UTF-8 Full Unicode(utf8mb4)
</pre>

---

### mysqlコンテナ起動
```bash
docker compose up -d
```
### mysql接続
### コンテナ経由
```bash
docker exec -it mysql_container mysql -u development -p --default-character-set=utf8mb4
```
### ホストOSから(brewなど)
```bash
mysql -h 127.0.0.1 -P 4036 -u root -p
```

## pumlファイル表示方法
- pycharm上でプラグイン拡張でのリアルタイムプレビュー もしくは draw.io上でコード埋込の2パターンがあります

### pycharm上でプラグイン拡張でのリアルタイムプレビュー
- 必要なものは①PlantUML Integration②graphviz
1. pycharm > settings > Plugins で **PlantUML Integration**をインストール+有効化
2. `$ brew install graphviz`（brewが入っている事前提）
3. `$ dot -V`でインストールが完了したか確認
4. `.puml`形式ファイル作成（画面分割でプレビューが表示）
![pycharm_uml01](images/pycharm_uml01.png)

### draw.io上でコード埋込
- [drawio](https://www.drawio.com/) > 配置 > 挿入 > 高度な設定 > UMLを埋め込む
  - draw.io の UMLエンジンは一部構文にしか対応していないため、pycharmではエラーなく表示されるにも関わらずdrawio上ではエラーになる事があります
  - 上記理由のためpycharmなどでリアルタイムプレビューが良さそうです。導入も簡単なので。
![drawio_uml01](images/drawio_uml01.png)
![drawio_uml02](images/drawio_uml02.png)


## 補足
  - Mysqlはバージョンによって認証プラグインが異なるため注意
  - SequelProは8以降に対応していないとの事なので、8以降を使う際はSequelAceを使います
    - 5.7以前：mysql_native_password
    - 8以降：cacing_sha2_password
      - docker-composeに`command: --default-authentication-plugin=mysql_native_password`でmysql_native_passwordをデフォルトにできる
  - plugin確認：`SELECT User, Host, plugin FROM mysql.user;`
  - plugin変更：`ALTER USER '[user]'@'%' IDENTIFIED WITH [認証方法] BY '[password]';`
  - ホスト側で3306が空いているか確認
    - ローカルで`3306`が使われている場合エラーになります、下記コマンドなどで確認
    - brewでmysqlが動いている可能性（`brew services list`）もあるのでその場合は`brew services stop mysql`
    - `sudo lsof -nP -iTCP:3306 | grep LISTEN`