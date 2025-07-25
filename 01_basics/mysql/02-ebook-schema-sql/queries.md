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
SELECT *
FROM users
WHERE id NOT IN(
    SELECT DISTINCT user_id
    FROM book_purchases
    WHERE purchased_at BETWEEN '2024-02-11' AND '2024-03-11'
);
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
