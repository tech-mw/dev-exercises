# Mysql開発環境はMysql（docker） × SequelAceを想定
## 環境
- Mysql: 8.0
  - Mysqlはバージョンによって認証プラグインが異なるため注意
  - SequelProは8以降に対応していないとの事なので、8以降を使う際はSequelAceを使います
    - 5.7以前：mysql_native_password
    - 8以降：cacing_sha2_password
      - docker-composeに`command: --default-authentication-plugin=mysql_native_password`でmysql_native_passwordをデフォルトにできる
- Docker: 20.10以上

## docker-compose.yml作成
<pre>
services:
  db:
    image: mysql:8.0
    container_name: mysql_container
    environment:
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=sample_db
      - MYSQL_USER=development
      - MYSQL_PASSWORD=password
    ports:
      # ホスト側3306はバッティングする可能性があるため4306指定
      - "4306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
volumes:
  mysql_data:
</pre>

## mysqlコンテナ起動
```bash
docker compose up -d
```

## コンテナ経由でmysql接続
- passwordは`password` 
```bash
docker exec -it mysql_container mysql -u development -p
```

## SequelAceの設定
<pre>
接続方式タブ：TCP/IP
HOST:127.0.0.1
Username：development
Password：password
Database:sample_db（任意）
Port：3306
</pre>

## 注意点
- ローカルで`3306`が使われている場合エラーになります、下記コマンドなどで確認
  - `sudo lsof -nP -iTCP:3306 | grep LISTEN`
  - `brew services list`
    - brewでmysqlが動いている可能性もあるのでその場合は`brew services stop mysql`