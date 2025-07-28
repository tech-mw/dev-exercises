# 2024年以降に登録されたユーザーを新しい順に一覧表示
```sql
SELECT *
FROM users
WHERE created_at >= '2024-01-01'
ORDER BY created_at DESC;
```
```
+----+-----------------+--------------------+---------------------+---------------------+
| id | indication_name | email              | created_at          | updated_at          |
+----+-----------------+--------------------+---------------------+---------------------+
|  7 | 渡辺 光         | 渡辺@example.com   | 2024-05-21 20:11:00 | 2024-05-21 20:11:00 |
|  8 | 加藤 愛         | 加藤@example.com   | 2024-04-02 22:08:00 | 2024-04-02 22:08:00 |
|  9 | 小林 誠         | 小林@example.com   | 2024-03-09 01:15:00 | 2024-03-09 01:15:00 |
|  6 | 高橋 涼         | 高橋@example.com   | 2024-03-01 19:51:00 | 2024-03-01 19:51:00 |
|  5 | 伊藤 彩         | 伊藤@example.com   | 2024-02-11 15:43:00 | 2024-02-11 15:43:00 |
| 10 | 斎藤 陽         | 斎藤@example.com   | 2024-01-20 16:34:00 | 2024-01-20 16:34:00 |
+----+-----------------+--------------------+---------------------+---------------------+
```

# 名前に「田」が含まれるユーザーを五十音順で抽出
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

# 最も注文金額が高かったユーザーの氏名/メールアドレス/合計購入金額を取得
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
| 山田 太郎     | yamada@example.com    |               4391 |
+---------------+-----------------------+--------------------+
```

# 2024年3月以降に注文をしたユーザーの名前一覧を重複なく表示
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
| 渡辺 光       |
| 加藤 愛       |
| 小林 誠       |
| 斎藤 陽       |
+---------------+
```

# ユーザー事の累計購入金額を計算、上位3名の名前と合計金額を表示
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
| 山田 太郎     |               4391 |
| 田中 花子     |               3513 |
| 佐藤 健       |               1463 |
+---------------+--------------------+
```

# 期間内に特定の出版社を書籍を購入した累計額をユーザー毎に集計
- 条件
  - 期間：2024年3月1日00:00 〜 2024年4月30日23:59 
  - 出版社：SBクリエイティブ
```sql
SELECT
    bp.user_id,
    SUM(bp.amount) AS total
FROM book_purchases AS bp
JOIN (
    SELECT *
    FROM books
    WHERE publisher = 'SBクリエイティブ') AS b ON b.id = bp.book_id
WHERE bp.purchased_at BETWEEN '2024-03-01' AND '2024-04-30'
GROUP BY bp.user_id
ORDER BY total DESC;
```
```
+---------+-------+
| user_id | total |
+---------+-------+
|       4 |  1029 |
+---------+-------+
```
# 期間内に特定ユーザーが何ページ読んでいるか、1000ページ超えている場合ポイント付与対象
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
# 直近30日間に1冊も購入していないユーザー一覧
```sql
-- purchased_at >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH); の場合実行日時によって結果が異なるため日時を固定
SELECT u.*
FROM users u
LEFT JOIN book_purchases bp
  ON u.id = bp.user_id
  AND bp.purchased_at BETWEEN '2024-02-11' AND '2024-03-11'
WHERE bp.user_id IS NULL;
```
```
+----+-----------------+--------------------+---------------------+---------------------+
| id | indication_name | email              | created_at          | updated_at          |
+----+-----------------+--------------------+---------------------+---------------------+
|  1 | 山田 太郎       | yamada@example.com | 2001-01-01 10:00:00 | 2024-01-01 10:00:00 |
|  3 | 佐藤 健         | 佐藤@example.com   | 2010-01-20 02:01:00 | 2024-01-20 02:01:00 |
|  4 | 中村 仁         | 中村@example.com   | 2005-02-20 11:00:00 | 2024-02-20 11:00:00 |
|  6 | 高橋 涼         | 高橋@example.com   | 2024-03-01 19:51:00 | 2024-03-01 19:51:00 |
|  7 | 渡辺 光         | 渡辺@example.com   | 2024-05-21 20:11:00 | 2024-05-21 20:11:00 |
|  8 | 加藤 愛         | 加藤@example.com   | 2024-04-02 22:08:00 | 2024-04-02 22:08:00 |
|  9 | 小林 誠         | 小林@example.com   | 2024-03-09 01:15:00 | 2024-03-09 01:15:00 |
| 10 | 斎藤 陽         | 斎藤@example.com   | 2024-01-20 16:34:00 | 2024-01-20 16:34:00 |
+----+-----------------+--------------------+---------------------+---------------------+
```

### 各ユーザーの合計購入金額と合計ページ閲覧数を並べて表示
```sql
SELECT
    u.indication_name AS '名前',
    (SELECT SUM(amount) FROM book_purchases WHERE user_id = u.id) AS '購入合計金額',
    (SELECT SUM(pages_viewed) FROM book_views WHERE user_id = u.id) AS '累計ページ閲覧数'
FROM users AS u;
```
```
+---------------+--------------------+--------------------------+
| 名前          | 購入合計金額       | 累計ページ閲覧数         |
+---------------+--------------------+--------------------------+
| 山田 太郎     |               4391 |                      208 |
| 田中 花子     |               3513 |                      107 |
| 佐藤 健       |               1463 |                      107 |
| 中村 仁       |               1029 |                      230 |
| 伊藤 彩       |               2347 |                     1146 |
| 高橋 涼       |               1122 |                      116 |
| 渡辺 光       |               2564 |                      103 |
| 加藤 愛       |               1196 |                     NULL |
| 小林 誠       |               3655 |                      164 |
| 斎藤 陽       |               2564 |                       65 |
+---------------+--------------------+--------------------------+
```

### 出版社毎の売上ランキング（上位3社）
```sql
-- 出版社毎の売上ランキング（上位3社）
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
| 翔泳社                  |               6781 |
| マイナビ出版            |               6362 |
| SBクリエイティブ        |               5575 |
+-------------------------+--------------------+
```

### 過去に1度でも SBクリエイティブ の書籍を買ったユーザー一覧
```sql
-- 過去に1度でも SBクリエイティブ の書籍を買ったユーザー一覧

SELECT DISTINCT *
FROM(
    SELECT bp.user_id
    FROM book_purchases AS bp
    JOIN books AS b ON b.id = bp.book_id
    WHERE b.publisher = "SBクリエイティブ"
) AS pu
JOIN users AS u ON u.id = pu.user_id;
```
```
+---------+----+-----------------+--------------------+---------------------+---------------------+
| user_id | id | indication_name | email              | created_at          | updated_at          |
+---------+----+-----------------+--------------------+---------------------+---------------------+
|       4 |  4 | 中村 仁         | 中村@example.com   | 2005-02-20 11:00:00 | 2024-02-20 11:00:00 |
|       5 |  5 | 伊藤 彩         | 伊藤@example.com   | 2024-02-11 15:43:00 | 2024-02-11 15:43:00 |
|       6 |  6 | 高橋 涼         | 高橋@example.com   | 2024-03-01 19:51:00 | 2024-03-01 19:51:00 |
|       1 |  1 | 山田 太郎       | yamada@example.com | 2001-01-01 10:00:00 | 2024-01-01 10:00:00 |
|       2 |  2 | 田中 花子       | 田中@example.com   | 2002-02-14 09:10:00 | 2024-02-14 09:10:00 |
+---------+----+-----------------+--------------------+---------------------+---------------------+
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
| 佐藤 健    | 佐藤@example.com      |               1463 |
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

```
2024年4月に「ページを100ページ以上読んだユーザー」のうち、
累計購入金額が全体の平均未満のユーザーを抽出し、
名前・メールアドレス・合計閲覧ページ数・合計購入金額を表示

使用テーブル：users, book_views, book_purchases
期間条件：
- 閲覧：2024-04-01 〜 2024-04-30（viewed_at）
- 購入：2024-04-01 〜 2024-04-30（purchased_at）
ロジック条件：
- ユーザー単位で SUM(pages_viewed) が100以上
- かつ、SUM(amount) が「全ユーザーの平均購入金額」よりも少ない
表示カラム：
- indication_name（名前）
- email
- 累計閲覧ページ数
- 合計購入金額
```
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
    HAVING SUM(pages_viewed) > 100
) AS bv
JOIN book_purchases AS bp ON bp.user_id = bv.user_id
JOIN users AS u ON u.id = bv.user_id
GROUP BY u.id, u.indication_name, u.email, bv.total_view_cnt
HAVING AVG(bp.amount) < (
    SELECT AVG(amount)
    FROM book_purchases
    WHERE purchased_at BETWEEN '2024-04-01' AND '2024-04-30'
);
```
```
+------------+-----------------------+--------------------------+--------------------+
| 名前       | メールアドレス        | 累計閲覧ページ数         | 累計購入金額       |
+------------+-----------------------+--------------------------+--------------------+
| 中村 仁    | 中村@example.com      |                      104 |               1029 |
+------------+-----------------------+--------------------------+--------------------+
```