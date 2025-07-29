### 2024年以降に登録されたユーザーを新しい順に一覧表示
```sql
SELECT *
FROM users
WHERE created_at >= '2024-01-01'
ORDER BY created_at DESC;
```
```
+----+-----------------+-----------------------+---------------------+---------------------+
| id | indication_name | email                 | created_at          | updated_at          |
+----+-----------------+-----------------------+---------------------+---------------------+
|  7 | 渡辺 光         | watanabe@example.com  | 2024-05-21 20:11:00 | 2024-05-21 20:11:00 |
|  8 | 加藤 愛         | kato@example.com      | 2024-04-02 22:08:00 | 2024-04-02 22:08:00 |
|  9 | 小林 誠         | kobayashi@example.com | 2024-03-09 01:15:00 | 2024-03-09 01:15:00 |
|  6 | 高橋 涼         | takahashi@example.com | 2024-03-01 19:51:00 | 2024-03-01 19:51:00 |
|  5 | 伊藤 彩         | ito@example.com       | 2024-02-11 15:43:00 | 2024-02-11 15:43:00 |
| 10 | 斎藤 陽         | saito@example.com     | 2024-01-20 16:34:00 | 2024-01-20 16:34:00 |
+----+-----------------+-----------------------+---------------------+---------------------+
```

### 名前に「田」が含まれるユーザーを五十音順で抽出
```sql
SELECT indication_name AS '名前'
FROM users
WHERE indication_name LIKE '%田%';
```
```
+---------------+
| 名前          |
+---------------+
| 山田 太郎     |
| 田中 花子     |
+---------------+
```

### 最も注文金額が高かったユーザーの氏名/メールアドレス/合計購入金額を取得
```sql
SELECT
    indication_name AS '名前',
    email AS 'メールアドレス',
    total_amount AS '合計購入金額'
FROM(
    SELECT
        user_id,
        SUM(amount) AS total_amount
    FROM book_purchases
    GROUP BY user_id
    ORDER BY total_amount DESC
    LIMIT 1
) AS bp
JOIN users AS u
ON u.id = bp.user_id;
```
```
+---------------+-----------------------+--------------------+
| 名前          | メールアドレス        | 合計購入金額       |
+---------------+-----------------------+--------------------+
| 田中 花子     | tanaka@example.com    |               7086 |
+---------------+-----------------------+--------------------+
```

### 2024年3月以降に注文をしたユーザーの名前一覧を重複なく表示
```sql
SELECT
    indication_name AS '名前'
FROM(
    SELECT DISTINCT user_id
    FROM book_purchases
    WHERE purchased_at > '2024-03-01 00:00:00'
) AS bp
JOIN users AS u
ON u.id = bp.user_id;
```
```
+---------------+
| 名前          |
+---------------+
| 田中 花子     |
| 中村 仁       |
| 伊藤 彩       |
| 高橋 涼       |
| 渡辺 光       |
| 加藤 愛       |
| 小林 誠       |
| 斎藤 陽       |
+---------------+
```

### ユーザー事の累計購入金額を計算、上位3名の名前と合計金額を表示
```sql
SELECT
    u.indication_name AS '名前',
    pb.total_amount AS '合計購入金額'
FROM(
    SELECT
        user_id,
        SUM(amount) AS total_amount
    FROM book_purchases
    GROUP BY user_id
    LIMIT 3
) AS pb
JOIN users AS u
ON u.id = pb.user_id;
```
```
+---------------+--------------------+
| 名前          | 合計購入金額       |
+---------------+--------------------+
| 山田 太郎     |               5669 |
| 田中 花子     |               7086 |
| 佐藤 健       |               1463 |
+---------------+--------------------+
```

### 期間内に特定の出版社を書籍を購入した累計購入金額をユーザー毎に集計
- 条件
  - 期間：2024年3月1日00:00 〜 2024年4月30日23:59 
  - 出版社：SBクリエイティブ
```sql
SELECT
    bp.user_id AS 'ユーザーID',
    SUM(bp.amount) AS '累計購入金額'
FROM book_purchases AS bp
JOIN (
    SELECT *
    FROM books
    WHERE publisher = 'SBクリエイティブ') AS b ON b.id = bp.book_id
WHERE bp.purchased_at BETWEEN '2024-03-01' AND '2024-04-30'
GROUP BY bp.user_id
ORDER BY SUM(bp.amount) DESC;
```
```
+----------------+--------------------+
| ユーザーID     | 累計購入金額       |
+----------------+--------------------+
|              4 |               1029 |
+----------------+--------------------+
```
### 期間内に特定ユーザーが何ページ読んでいるか、1000ページ超えている場合ポイント付与対象
- 条件
  - 期間：2024年3月1日00:00 〜 2024年3月31日23:59

```sql
SELECT
    u.indication_name AS '名前',
    pv.total_cnt AS '累計ページ閲覧数',
    CASE
        WHEN pv.total_cnt >= 1000 THEN 100
        ELSE 0
    END AS '付与ポイント'
FROM(
     SELECT
         user_id,
         SUM(pages_viewed) AS total_cnt
     FROM book_views
     WHERE viewed_at BETWEEN '2024-03-01' AND '2024-04-01'
     GROUP BY user_id
) AS pv
    JOIN users AS u
    ON u.id = pv.user_id;
```
```
+------------+--------------------------+--------------------+
| 名前       | 累計ページ閲覧数         | 付与ポイント       |
+------------+--------------------------+--------------------+
| 伊藤 彩    |                     1146 |                100 |
| 小林 誠    |                       85 |                  0 |
+------------+--------------------------+--------------------+
```
### 直近30日間に1冊も購入していないユーザー一覧
- purchased_at >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH); の場合実行日時によって結果が異なるため日時を固定
```sql
SELECT u.*
FROM users u
LEFT JOIN book_purchases bp
  ON u.id = bp.user_id
  AND bp.purchased_at BETWEEN '2024-02-11' AND '2024-03-11'
WHERE bp.user_id IS NULL;
```
```
+----+-----------------+-----------------------+---------------------+---------------------+
| id | indication_name | email                 | created_at          | updated_at          |
+----+-----------------+-----------------------+---------------------+---------------------+
|  1 | 山田 太郎       | yamada@example.com    | 2001-01-01 10:00:00 | 2024-01-01 10:00:00 |
|  3 | 佐藤 健         | sato@example.com      | 2010-01-20 02:01:00 | 2024-01-20 02:01:00 |
|  4 | 中村 仁         | nakamura@example.com  | 2005-02-20 11:00:00 | 2024-02-20 11:00:00 |
|  6 | 高橋 涼         | takahashi@example.com | 2024-03-01 19:51:00 | 2024-03-01 19:51:00 |
|  7 | 渡辺 光         | watanabe@example.com  | 2024-05-21 20:11:00 | 2024-05-21 20:11:00 |
|  8 | 加藤 愛         | kato@example.com      | 2024-04-02 22:08:00 | 2024-04-02 22:08:00 |
|  9 | 小林 誠         | kobayashi@example.com | 2024-03-09 01:15:00 | 2024-03-09 01:15:00 |
| 10 | 斎藤 陽         | saito@example.com     | 2024-01-20 16:34:00 | 2024-01-20 16:34:00 |
| 11 | 佐々木 守       | sasaki@example.com    | 2001-01-01 15:53:00 | 2024-01-10 21:10:00 |
+----+-----------------+-----------------------+---------------------+---------------------+
```

### 各ユーザーの合計購入金額と合計ページ閲覧数を並べて表示
```sql
SELECT
    u.indication_name AS '名前',
    IFNULL((SELECT SUM(amount) FROM book_purchases WHERE user_id = u.id), 0) AS '購入合計金額',
    IFNULL((SELECT SUM(pages_viewed) FROM book_views WHERE user_id = u.id), 0) AS '累計ページ閲覧数'
FROM users AS u;
```
```
+---------------+--------------------+--------------------------+
| 名前          | 購入合計金額       | 累計ページ閲覧数         |
+---------------+--------------------+--------------------------+
| 山田 太郎     |               5669 |                      208 |
| 田中 花子     |               7086 |                      107 |
| 佐藤 健       |               1463 |                      107 |
| 中村 仁       |               2679 |                      230 |
| 伊藤 彩       |               3261 |                     1146 |
| 高橋 涼       |               2014 |                      116 |
| 渡辺 光       |               3686 |                      103 |
| 加藤 愛       |               1196 |                        0 |
| 小林 誠       |               3655 |                      164 |
| 斎藤 陽       |               4919 |                       65 |
| 佐々木 守     |                  0 |                        0 |
+---------------+--------------------+--------------------------+
```

### 出版社毎の売上ランキング（上位3社）
```sql
SELECT
    b.publisher AS '出版社',
    SUM(bp.amount) AS '合計売上金額'
FROM book_purchases AS bp
JOIN books AS b ON b.id = bp.book_id
GROUP BY b.publisher
ORDER BY SUM(bp.amount) DESC
LIMIT 3;
```
```
+-------------------------+--------------------+
| 出版社                  | 合計売上金額       |
+-------------------------+--------------------+
| マイナビ出版            |              11074 |
| 翔泳社                  |              10903 |
| SBクリエイティブ        |               6697 |
+-------------------------+--------------------+
```

### 過去に1度でも SBクリエイティブ の書籍を買ったユーザー一覧
```sql
SELECT DISTINCT
    u.indication_name AS '名前',
    u.email AS 'メールアドレス',
    u.created_at AS '登録日時'
FROM(
    SELECT bp.user_id
    FROM book_purchases AS bp
    JOIN books AS b ON b.id = bp.book_id
    WHERE b.publisher = "SBクリエイティブ"
) AS pu
JOIN users AS u ON u.id = pu.user_id;
```
```
+---------------+-----------------------+---------------------+
| 名前          | メールアドレス        | 登録日時            |
+---------------+-----------------------+---------------------+
| 中村 仁       | nakamura@example.com  | 2005-02-20 11:00:00 |
| 伊藤 彩       | ito@example.com       | 2024-02-11 15:43:00 |
| 高橋 涼       | takahashi@example.com | 2024-03-01 19:51:00 |
| 渡辺 光       | watanabe@example.com  | 2024-05-21 20:11:00 |
| 山田 太郎     | yamada@example.com    | 2001-01-01 10:00:00 |
| 田中 花子     | tanaka@example.com    | 2002-02-14 09:10:00 |
+---------------+-----------------------+---------------------+
```

### 平均購入金額が1400円以上のユーザー一覧
```sql
SELECT
    u.indication_name AS '名前',
    u.email AS 'メールアドレス',
    tu.avg_amount AS '平均購入金額'
FROM(
SELECT
    user_id,
    CAST(AVG(amount) AS SIGNED) AS avg_amount
FROM book_purchases
GROUP BY user_id
HAVING avg_amount > 1400)
AS tu
JOIN users AS u ON u.id = tu.user_id;
```
```
+------------+-----------------------+--------------------+
| 名前       | メールアドレス        | 平均購入金額       |
+------------+-----------------------+--------------------+
| 佐藤 健    | sato@example.com      |               1463 |
+------------+-----------------------+--------------------+
```

### 2024年3月に購入金額が最も高かったユーザーの名前と金額
```sql
SELECT
    u.indication_name AS '名前',
    totals.total AS '期間内合計購入金額'
FROM(
    SELECT DISTINCT
        user_id,
        SUM(amount) AS total
    FROM book_purchases
    WHERE purchased_at BETWEEN '2024-04-01 00:00:00' AND '2024-04-30 23:59:59'
    GROUP BY user_id) AS totals
JOIN users AS u ON u.id = totals.user_id
ORDER BY total DESC
LIMIT 1;
```
```
+------------+-----------------------------+
| 名前       | 期間内合計購入金額          |
+------------+-----------------------------+
| 小林 誠    |                        2377 |
+------------+-----------------------------+
```

### 2024年4月に「ページを50ページ以上読んだユーザー」のうち、累計購入金額が全体の平均以上のユーザーを抽出、名前・メールアドレス・合計閲覧ページ数・合計購入金額を表示
```sql
SELECT
    u.indication_name AS '名前',
    u.email AS 'メールアドレス',
    bv.total_view_cnt AS '累計閲覧ページ数',
    SUM(bp.amount) AS '累計購入金額'
FROM (
    SELECT
        user_id,
        SUM(pages_viewed) AS total_view_cnt
    FROM book_views
    WHERE viewed_at BETWEEN '2024-04-01' AND '2024-04-30'
    GROUP BY user_id
    HAVING SUM(pages_viewed) > 50
) AS bv
JOIN book_purchases AS bp ON bp.user_id = bv.user_id
JOIN users AS u ON u.id = bv.user_id
GROUP BY u.id, u.indication_name, u.email, bv.total_view_cnt
HAVING SUM(bp.amount) > (
    SELECT AVG(amount)
    FROM book_purchases
    WHERE purchased_at BETWEEN '2024-04-01' AND '2024-04-30'
);
```
```
+------------+-----------------------+--------------------------+--------------------+
| 名前       | メールアドレス        | 累計閲覧ページ数         | 累計購入金額       |
+------------+-----------------------+--------------------------+--------------------+
| 中村 仁    | nakamura@example.com  |                      104 |               2679 |
| 小林 誠    | kobayashi@example.com |                       79 |               3655 |
| 斎藤 陽    | saito@example.com     |                       65 |               4919 |
+------------+-----------------------+--------------------------+--------------------+
```

### 出版社別売上に対するユーザーの累計合計金額を抽出

```sql
SELECT
    u.indication_name AS '名前',
    b.publisher AS '出版社',
    SUM(bp.total_amount) AS '累計購入金額'
FROM (
    SELECT
        user_id,
        book_id,
        SUM(amount) AS total_amount
    FROM book_purchases
    GROUP BY user_id, book_id
) AS bp
JOIN books AS b ON bp.book_id = b.id
JOIN users AS u ON u.id = bp.user_id
GROUP BY u.id, u.indication_name, b.publisher;
```
```
+---------------+-------------------------+--------------------+
| 名前          | 出版社                  | 累計購入金額       |
+---------------+-------------------------+--------------------+
| 中村 仁       | マイナビ出版            |               1650 |
| 斎藤 陽       | マイナビ出版            |               2542 |
| 渡辺 光       | マイナビ出版            |               1650 |
| 山田 太郎     | マイナビ出版            |               2170 |
| 小林 誠       | マイナビ出版            |               1278 |
| 加藤 愛       | 翔泳社                  |               1196 |
| 伊藤 彩       | 翔泳社                  |               1196 |
| 田中 花子     | 翔泳社                  |               2659 |
| 渡辺 光       | インプレス              |                914 |
| 伊藤 彩       | インプレス              |                914 |
| 田中 花子     | インプレス              |                914 |
| 山田 太郎     | インプレス              |                914 |
| 小林 誠       | インプレス              |                914 |
| 斎藤 陽       | インプレス              |                914 |
| 高橋 涼       | SBクリエイティブ        |               1122 |
| 渡辺 光       | SBクリエイティブ        |               1122 |
| 山田 太郎     | SBクリエイティブ        |               1122 |
| 伊藤 彩       | SBクリエイティブ        |               1151 |
| 田中 花子     | SBクリエイティブ        |               1151 |
| 中村 仁       | SBクリエイティブ        |               1029 |
| 佐藤 健       | 翔泳社                  |               1463 |
| 小林 誠       | 翔泳社                  |               1463 |
| 斎藤 陽       | 翔泳社                  |               1463 |
| 山田 太郎     | 翔泳社                  |               1463 |
| 田中 花子     | 技術評論社              |               1470 |
| 高橋 涼       | マイナビ出版            |                892 |
| 田中 花子     | マイナビ出版            |                892 |
+---------------+-------------------------+--------------------+
```

### 各ユーザーの**最新の購入日時（purchased_at）**を抽出し、そのユーザー情報とともに一覧表示
```sql
SELECT
    u.indication_name AS '名前',
    u.email AS 'メールアドレス',
    bp.latest_purchase AS '最新購入日時'
FROM(
SELECT
    user_id,
    MAX(purchased_at) AS latest_purchase
FROM book_purchases
GROUP BY user_id) AS bp
JOIN users AS u ON u.id = bp.user_id;
```
```
+---------------+-----------------------+---------------------+
| 名前          | メールアドレス        | 最新購入日時        |
+---------------+-----------------------+---------------------+
| 山田 太郎     | yamada@example.com    | 2011-11-11 07:56:51 |
| 田中 花子     | tanaka@example.com    | 2024-11-21 19:36:12 |
| 佐藤 健       | sato@example.com      | 2020-03-05 15:34:01 |
| 中村 仁       | nakamura@example.com  | 2024-05-01 10:11:19 |
| 伊藤 彩       | ito@example.com       | 2024-04-11 01:39:42 |
| 高橋 涼       | takahashi@example.com | 2024-03-20 22:55:12 |
| 渡辺 光       | watanabe@example.com  | 2024-06-11 17:33:12 |
| 加藤 愛       | kato@example.com      | 2024-04-13 20:01:11 |
| 小林 誠       | kobayashi@example.com | 2024-04-19 11:56:21 |
| 斎藤 陽       | saito@example.com     | 2024-04-11 22:11:40 |
+---------------+-----------------------+---------------------+
```

### ユーザーの中で「最も多くの本を購入した人（冊数ベース）」を抽出し、そのユーザーの情報（名前・メールアドレス・冊数）を表示
```sql
SELECT
    u.indication_name AS '名前',
    u.email AS 'メールアドレス',
    bp.purchase_quantity AS '購入札数'
FROM(
SELECT
    user_id,
    COUNT(*) AS purchase_quantity
FROM book_purchases
GROUP BY user_id
ORDER BY purchase_quantity DESC
LIMIT 1) AS bp
JOIN users AS u ON u.id = bp.user_id;
```
```
+---------------+-----------------------+--------------+
| 名前          | メールアドレス        | 購入札数     |
+---------------+-----------------------+--------------+
| 田中 花子     | tanaka@example.com    |            6 |
+---------------+-----------------------+--------------+
```

### 購入回数が3回以上のユーザーをすべて表示し、回数の多い順に並べる
```sql
SELECT
    u.indication_name AS '名前',
    u.email AS 'メールアドレス',
    bp.purchase_quantity AS '購入回数'
FROM (
    SELECT
        user_id,
        COUNT(*) AS purchase_quantity
    FROM book_purchases
    GROUP BY user_id
    HAVING COUNT(*) > 3
) AS bp
JOIN users AS u ON u.id = bp.user_id
ORDER BY bp.purchase_quantity DESC;
```
```
+---------------+-----------------------+--------------+
| 名前          | メールアドレス        | 購入回数     |
+---------------+-----------------------+--------------+
| 田中 花子     | tanaka@example.com    |            6 |
| 山田 太郎     | yamada@example.com    |            5 |
| 斎藤 陽       | saito@example.com     |            4 |
+---------------+-----------------------+--------------+
```

### 2024年4月中に「書籍を購入した」又は「書籍を閲覧した」ユーザーのアクション履歴
```sql
SELECT
    user_id,
    book_id,
    '購入' AS event_type,
    purchased_at AS event_date
FROM book_purchases
WHERE purchased_at BETWEEN '2024-04-01 00:00:00' AND '2024-04-30 23:59:59'
UNION
SELECT
    user_id,
    book_id,
    '閲覧' AS event_type,
    viewed_at AS event_date
FROM book_views
WHERE viewed_at BETWEEN '2024-04-01' AND '2024-04-30'
ORDER BY event_date ASC;
```
```
+---------+---------+------------+---------------------+
| user_id | book_id | event_type | event_date          |
+---------+---------+------------+---------------------+
|       9 |       9 | 閲覧       | 2024-04-05 00:00:00 |
|       4 |       2 | 閲覧       | 2024-04-10 00:00:00 |
|      10 |       5 | 閲覧       | 2024-04-10 00:00:00 |
|       9 |       4 | 購入       | 2024-04-10 10:56:11 |
|       6 |      10 | 閲覧       | 2024-04-11 00:00:00 |
|       5 |       3 | 購入       | 2024-04-11 01:39:42 |
|      10 |       1 | 購入       | 2024-04-11 22:11:40 |
|       8 |       3 | 購入       | 2024-04-13 20:01:11 |
|       4 |       7 | 閲覧       | 2024-04-18 00:00:00 |
|       4 |       7 | 購入       | 2024-04-18 20:01:19 |
|       9 |       8 | 購入       | 2024-04-19 11:56:21 |
+---------+---------+------------+---------------------+
```

### 書籍の中で、一度も購入されたことのない書籍
```sql
SELECT
    b.title AS 'タイトル',
    b.publisher AS '出版社'
FROM books AS b LEFT OUTER JOIN book_purchases AS bp
ON b.id = bp.book_id
WHERE bp.book_id IS NULL;
```
```
+------------------------------------------+--------------------+
| タイトル                                 | 出版社             |
+------------------------------------------+--------------------+
| ビジネス活用のためのSQL分析2             | マイナビ出版       |
+------------------------------------------+--------------------+
```

### 購入書籍の「出版社別」内訳をすべて表示（未購入も含む）
- 全ての出版社毎に、ユーザーがその出版社から購入した金額の合計を表示する。ただし、一度も購入していない出版社も表示対象とする
```sql
SELECT
    pub_user.publisher AS '出版社',
    pub_user.user_id AS 'ユーザーID',
    IFNULL(SUM(bp.amount), 0) AS '合計購入金額'
FROM (
    SELECT DISTINCT b.publisher, u.id AS user_id
    FROM books AS b
    CROSS JOIN users AS u
) AS pub_user
LEFT JOIN books AS b ON b.publisher = pub_user.publisher
LEFT JOIN book_purchases AS bp ON bp.book_id = b.id AND bp.user_id = pub_user.user_id
GROUP BY pub_user.publisher, pub_user.user_id
ORDER BY pub_user.publisher, pub_user.user_id;
```
```
+-------------------------+----------------+--------------------+
| 出版社                  | ユーザーID     | 合計購入金額       |
+-------------------------+----------------+--------------------+
| SBクリエイティブ        |              1 |               1122 |
| SBクリエイティブ        |              2 |               1151 |
| SBクリエイティブ        |              3 |                  0 |
| SBクリエイティブ        |              4 |               1029 |
| SBクリエイティブ        |              5 |               1151 |
| SBクリエイティブ        |              6 |               1122 |
| SBクリエイティブ        |              7 |               1122 |
| SBクリエイティブ        |              8 |                  0 |
| SBクリエイティブ        |              9 |                  0 |
| SBクリエイティブ        |             10 |                  0 |
| SBクリエイティブ        |             11 |                  0 |
| インプレス              |              1 |                914 |
| インプレス              |              2 |                914 |
| インプレス              |              3 |                  0 |
| インプレス              |              4 |                  0 |
| インプレス              |              5 |                914 |
| インプレス              |              6 |                  0 |
| インプレス              |              7 |                914 |
| インプレス              |              8 |                  0 |
| インプレス              |              9 |                914 |
| インプレス              |             10 |                914 |
| インプレス              |             11 |                  0 |
| マイナビ出版            |              1 |               2170 |
| マイナビ出版            |              2 |                892 |
| マイナビ出版            |              3 |                  0 |
| マイナビ出版            |              4 |               1650 |
| マイナビ出版            |              5 |                  0 |
| マイナビ出版            |              6 |                892 |
| マイナビ出版            |              7 |               1650 |
| マイナビ出版            |              8 |                  0 |
| マイナビ出版            |              9 |               1278 |
| マイナビ出版            |             10 |               2542 |
| マイナビ出版            |             11 |                  0 |
| 技術評論社              |              1 |                  0 |
| 技術評論社              |              2 |               1470 |
| 技術評論社              |              3 |                  0 |
| 技術評論社              |              4 |                  0 |
| 技術評論社              |              5 |                  0 |
| 技術評論社              |              6 |                  0 |
| 技術評論社              |              7 |                  0 |
| 技術評論社              |              8 |                  0 |
| 技術評論社              |              9 |                  0 |
| 技術評論社              |             10 |                  0 |
| 技術評論社              |             11 |                  0 |
| 翔泳社                  |              1 |               1463 |
| 翔泳社                  |              2 |               2659 |
| 翔泳社                  |              3 |               1463 |
| 翔泳社                  |              4 |                  0 |
| 翔泳社                  |              5 |               1196 |
| 翔泳社                  |              6 |                  0 |
| 翔泳社                  |              7 |                  0 |
| 翔泳社                  |              8 |               1196 |
| 翔泳社                  |              9 |               1463 |
| 翔泳社                  |             10 |               1463 |
| 翔泳社                  |             11 |                  0 |
+-------------------------+----------------+--------------------+
```

### 購入履歴があるユーザーの「名前」と「書籍タイトル」を一覧表示
```sql
SELECT
    u.indication_name AS '購入ユーザー',
    b.title AS '購入書籍タイトル'
FROM book_purchases AS bp
INNER JOIN users AS u ON u.id = bp.user_id
INNER JOIN books AS b ON b.id = bp.book_id
ORDER BY u.indication_name;
```
```
+--------------------+--------------------------------------------+
| 購入ユーザー       | 購入書籍タイトル                           |
+--------------------+--------------------------------------------+
| 中村 仁            | プロフェッショナルSQLガイド                |
| 中村 仁            | 達人に学ぶSQLパフォーマンス                |
| 伊藤 彩            | はじめてのリレーショナルDB                 |
| 伊藤 彩            | SQLレシピ集：問題解決の実践例              |
| 伊藤 彩            | 現場で役立つSQLチューニング                |
| 佐藤 健            | 失敗しないDB設計の教科書                   |
| 加藤 愛            | 現場で役立つSQLチューニング                |
| 小林 誠            | 失敗しないDB設計の教科書                   |
| 小林 誠            | SQLレシピ集：問題解決の実践例              |
| 小林 誠            | 基礎からのMySQL実践入門                    |
| 山田 太郎          | 失敗しないDB設計の教科書                   |
| 山田 太郎          | ビジネス活用のためのSQL分析                |
| 山田 太郎          | 実践で使えるデータベース設計               |
| 山田 太郎          | SQLレシピ集：問題解決の実践例              |
| 山田 太郎          | 基礎からのMySQL実践入門                    |
| 斎藤 陽            | 達人に学ぶSQLパフォーマンス                |
| 斎藤 陽            | ビジネス活用のためのSQL分析                |
| 斎藤 陽            | SQLレシピ集：問題解決の実践例              |
| 斎藤 陽            | 失敗しないDB設計の教科書                   |
| 渡辺 光            | SQLレシピ集：問題解決の実践例              |
| 渡辺 光            | 達人に学ぶSQLパフォーマンス                |
| 渡辺 光            | 実践で使えるデータベース設計               |
| 田中 花子          | 失敗しないDB設計の教科書                   |
| 田中 花子          | SQLレシピ集：問題解決の実践例              |
| 田中 花子          | ビジネス活用のためのSQL分析                |
| 田中 花子          | 効率的なクエリの書き方                     |
| 田中 花子          | はじめてのリレーショナルDB                 |
| 田中 花子          | 現場で役立つSQLチューニング                |
| 高橋 涼            | ビジネス活用のためのSQL分析                |
| 高橋 涼            | 実践で使えるデータベース設計               |
+--------------------+--------------------------------------------+
```

### 全てのユーザーについて「直近30日間に購入した書籍のタイトル」があれば表示、なければNULLを表示
- 期間は 2024-04-01 00:00:00 〜 2024-04-30 23:59:59 で固定とする
```sql
SELECT
    u.indication_name AS '名前',
    IFNULL(bp.title, NULL) AS '書籍タイトル'
FROM users AS u
LEFT OUTER JOIN book_purchases AS bp
    ON u.id = bp.user_id
    AND bp.purchased_at BETWEEN '2024-04-01 00:00:00' AND '2024-04-30 23:59:59';
```
```
+---------------+--------------------------------------------+
| 名前          | 書籍タイトル                               |
+---------------+--------------------------------------------+
| 山田 太郎     | NULL                                       |
| 田中 花子     | NULL                                       |
| 佐藤 健       | NULL                                       |
| 中村 仁       | プロフェッショナルSQLガイド                |
| 伊藤 彩       | 現場で役立つSQLチューニング                |
| 高橋 涼       | NULL                                       |
| 渡辺 光       | NULL                                       |
| 加藤 愛       | 現場で役立つSQLチューニング                |
| 小林 誠       | 失敗しないDB設計の教科書                   |
| 小林 誠       | SQLレシピ集：問題解決の実践例              |
| 斎藤 陽       | 達人に学ぶSQLパフォーマンス                |
| 佐々木 守     | NULL                                       |
+---------------+--------------------------------------------+
```

### 一度も書籍を閲覧したことがないユーザー」の名前とメールアドレスを一覧表示
```sql
SELECT
    u.indication_name AS '名前',
    u.email AS 'メールアドレス'
FROM users AS u
LEFT OUTER JOIN book_views AS bv
    ON u.id = bv.user_id
WHERE bv.book_id IS NULL;
```
```
+---------------+-----------------------+
| 名前          | メールアドレス        |
+---------------+-----------------------+
| 加藤 愛       | kato@example.com      |
| 佐々木 守     | sasaki@example.com    |
+---------------+-----------------------+
```

### 各出版社毎の購入者数
```sql
SELECT
    b.publisher AS '出版社',
    COUNT(DISTINCT bp.user_id) AS '購入ユーザー数'
FROM books AS b INNER JOIN book_purchases AS bp
ON b.id = bp.book_id
GROUP BY b.publisher;
```
```
+-------------------------+-----------------------+
| 出版社                  | 購入ユーザー数        |
+-------------------------+-----------------------+
| SBクリエイティブ        |                     6 |
| インプレス              |                     6 |
| マイナビ出版            |                     7 |
| 技術評論社              |                     1 |
| 翔泳社                  |                     7 |
+-------------------------+-----------------------+
```

### 2024年4月に出版社「SBクリエイティブ」の書籍を購入したユーザーの名前と合計金額を表示
```
SELECT
    b.publisher AS '出版社',
    u.indication_name AS '名前',
    SUM(bp.amount) AS '合計金額'
FROM users AS u
INNER JOIN book_purchases AS bp ON u.id = bp.user_id
INNER JOIN books AS b ON b.id = bp.book_id
WHERE bp.purchased_at BETWEEN '2024-04-01 00:00:00' AND '2024-04-30 23:59:59'
AND b.publisher = 'SBクリエイティブ'
GROUP BY u.id, b.publisher, u.indication_name;
```
```
+-------------------------+------------+--------------+
| 出版社                  | 名前       | 合計金額     |
+-------------------------+------------+--------------+
| SBクリエイティブ        | 中村 仁    |         1029 |
+-------------------------+------------+--------------+
```