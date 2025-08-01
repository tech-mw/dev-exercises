SET NAMES utf8mb4;

-- ユーザー情報
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    indication_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME
);

-- 書籍情報
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    publisher VARCHAR(100) NOT NULL,
    is_published INT NOT NULL,
    read_direction INT NOT NULL,
    price INT NOT NULL,
    price_tax_inc INT NOT NULL,
    delivery_start DATETIME NOT NULL,
    delivery_end DATETIME NOT NULL,
    page INT NOT NULL
);


-- 書籍購入履歴
CREATE TABLE book_purchases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    purchased_at DATETIME NOT NULL,
    amount INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- 書籍閲覧履歴
CREATE TABLE book_views (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    viewed_at DATE NOT NULL,
    pages_viewed INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);


START TRANSACTION;

INSERT INTO users (indication_name, email, created_at, updated_at) VALUES
('山田 太郎', 'yamada@example.com', '2001-01-01 10:00:00', '2024-01-01 10:00:00'),
('田中 花子', 'tanaka@example.com', '2002-02-14 09:10:00', '2024-02-14 09:10:00'),
('佐藤 健', 'sato@example.com', '2010-01-20 02:01:00', '2024-01-20 02:01:00'),
('中村 仁', 'nakamura@example.com', '2005-02-20 11:00:00', '2024-02-20 11:00:00'),
('伊藤 彩', 'ito@example.com', '2024-02-11 15:43:00', '2024-02-11 15:43:00'),
('高橋 涼', 'takahashi@example.com', '2024-03-01 19:51:00', '2024-03-01 19:51:00'),
('渡辺 光', 'watanabe@example.com', '2024-05-21 20:11:00', '2024-05-21 20:11:00'),
('加藤 愛', 'kato@example.com', '2024-04-02 22:08:00', '2024-04-02 22:08:00'),
('小林 誠', 'kobayashi@example.com', '2024-03-09 01:15:00', '2024-03-09 01:15:00'),
('斎藤 陽', 'saito@example.com', '2024-01-20 16:34:00', '2024-01-20 16:34:00'),
('佐々木 守', 'sasaki@example.com', '2001-01-01 15:53:00', '2024-01-10 21:10:00');


INSERT INTO books (title, publisher, is_published, read_direction, price, price_tax_inc, delivery_start, delivery_end, page) VALUES
('達人に学ぶSQLパフォーマンス', 'マイナビ出版', 2, 2, 1500, 1650, '2000-01-01 00:00:00', '2999-12-31 23:59:59', 352),
('基礎からのMySQL実践入門', 'マイナビ出版', 1, 1, 1162, 1278, '2000-01-01 00:00:00', '2999-12-31 23:59:59', 341),
('現場で役立つSQLチューニング', '翔泳社', 1, 2, 1088, 1196, '2000-01-01 00:00:00', '2999-12-31 23:59:59', 163),
('SQLレシピ集：問題解決の実践例', 'インプレス', 2, 1, 831, 914, '2000-01-01 00:00:00', '2999-12-31 23:59:59', 370),
('実践で使えるデータベース設計', 'SBクリエイティブ', 1, 1, 1020, 1122, '2000-01-01 00:00:00', '2999-12-31 23:59:59', 192),
('はじめてのリレーショナルDB', 'SBクリエイティブ', 1, 1, 1047, 1151, '2000-01-01 00:00:00', '2999-12-31 23:59:59', 387),
('プロフェッショナルSQLガイド', 'SBクリエイティブ', 1, 1, 936, 1029, '2000-01-01 00:00:00', '2999-12-31 23:59:59', 151),
('失敗しないDB設計の教科書', '翔泳社', 2, 1, 1330, 1463, '2000-01-01 00:00:00', '2999-12-31 23:59:59', 359),
('効率的なクエリの書き方', '技術評論社', 1, 2, 1337, 1470, '2000-01-01 00:00:00', '2999-12-31 23:59:59', 188),
('ビジネス活用のためのSQL分析', 'マイナビ出版', 1, 1, 811, 892, '2000-01-01 00:00:00', '2999-12-31 23:59:59', 389)
('ビジネス活用のためのSQL分析2', 'マイナビ出版', 1, 1, 811, 892, '2001-01-01 00:00:00', '2999-12-31 23:59:59', 999);

INSERT INTO book_purchases (user_id, book_id, title, purchased_at, amount) VALUES
(1, 10, 'ビジネス活用のためのSQL分析', '2010-02-05 11:49:45', 892),
(1, 2, '基礎からのMySQL実践入門', '2003-12-10 23:49:41', 1278),
(2, 9, '効率的なクエリの書き方', '2024-02-26 09:23:22', 1470),
(3, 8, '失敗しないDB設計の教科書', '2020-03-05 15:34:01', 1463),
(4, 7, 'プロフェッショナルSQLガイド', '2024-04-18 20:01:19', 1029),
(4, 1, '達人に学ぶSQLパフォーマンス', '2024-05-01 10:11:19', 1650),
(5, 6, 'はじめてのリレーショナルDB', '2024-02-26 02:01:02', 1151),
(6, 5, '実践で使えるデータベース設計', '2002-03-02 19:30:12', 1122),
(6, 10, 'ビジネス活用のためのSQL分析', '2024-03-20 22:55:12', 892),
(7, 4, 'SQLレシピ集：問題解決の実践例', '2011-05-22 15:11:42', 914),
(8, 3, '現場で役立つSQLチューニング', '2024-04-13 20:01:11', 1196),
(9, 2, '基礎からのMySQL実践入門', '2024-03-29 23:59:42', 1278),
(10, 10, 'ビジネス活用のためのSQL分析', '2024-02-07 02:13:10', 892),
(10, 1, '達人に学ぶSQLパフォーマンス', '2024-04-11 22:11:40', 1650),
(5, 3, '現場で役立つSQLチューニング', '2024-04-11 01:39:42', 1196),
(5, 4, 'SQLレシピ集：問題解決の実践例', '2024-3-02 10:22:55', 914),
(2, 8, '失敗しないDB設計の教科書', '2024-10-21 19:33:12', 1463),
(2, 4, 'SQLレシピ集：問題解決の実践例', '2024-11-21 19:36:12', 914),
(2, 10, 'ビジネス活用のためのSQL分析', '2024-10-10 10:19:42', 892),
(1, 4, 'SQLレシピ集：問題解決の実践例', '2011-10-01 16:11:33', 914),
(9, 4, 'SQLレシピ集：問題解決の実践例', '2024-04-10 10:56:11', 914),
(9, 8, '失敗しないDB設計の教科書', '2024-04-19 11:56:21', 1463),
(7, 1, '達人に学ぶSQLパフォーマンス', '2024-06-11 17:33:12', 1650),
(7, 5, '実践で使えるデータベース設計', '2024-05-25 03:11:12', 1122),
(10, 4, 'SQLレシピ集：問題解決の実践例', '2024-01-25 10:33:00', 914),
(10, 8, '失敗しないDB設計の教科書', '2024-03-25 05:22:12', 1463),
(1, 5, '実践で使えるデータベース設計', '2011-11-11 07:56:51', 1122),
(2, 6, 'はじめてのリレーショナルDB', '2005-03-23 06:22:53', 1151),
(2, 3, '現場で役立つSQLチューニング', '2023-10-10 12:43:52', 1196),
(1, 8, '失敗しないDB設計の教科書', '2002-06-23 07:54:21', 1463);

INSERT INTO book_views (user_id, book_id, title, viewed_at, pages_viewed) VALUES
(4, 7, 'プロフェッショナルSQLガイド', '2024-04-18', 86),
(4, 2, '基礎からのMySQL実践入門', '2024-04-10', 18),
(9, 2, '基礎からのMySQL実践入門', '2024-03-11', 85),
(4, 6, 'はじめてのリレーショナルDB', '2024-01-01', 33),
(7, 7, 'プロフェッショナルSQLガイド', '2024-06-10', 93),
(6, 10, 'はじめてのリレーショナルDB', '2024-04-11', 22),
(1, 4, 'SQLレシピ集：問題解決の実践例', '2020-12-10', 40),
(2, 1, '達人に学ぶSQLパフォーマンス', '2020-05-01', 40),
(6, 2, '基礎からのMySQL実践入門', '2024-06-11', 94),
(1, 10, 'ビジネス活用のためのSQL分析', '2024-01-01', 73),
(5, 6, 'はじめてのリレーショナルDB', '2024-03-21', 35),
(5, 10, 'ビジネス活用のためのSQL分析', '2024-03-22', 389),
(5, 4, 'SQLレシピ集：問題解決の実践例', '2024-03-23', 370),
(5, 1, '達人に学ぶSQLパフォーマンス', '2024-03-23', 352),
(2, 9, '効率的なクエリの書き方', '2019-08-29', 67),
(3, 6, 'はじめてのリレーショナルDB', '2013-06-06', 6),
(4, 8, '失敗しないDB設計の教科書', '2010-11-01', 93),
(1, 8, '失敗しないDB設計の教科書', '2002-01-01', 95),
(9, 9, '効率的なクエリの書き方', '2024-04-05', 79),
(3, 2, '基礎からのMySQL実践入門', '2011-07-03', 78),
(10, 5, '実践で使えるデータベース設計', '2024-04-10', 65),
(3, 3, '現場で役立つSQLチューニング', '2018-03-01', 23),
(7, 3, '現場で役立つSQLチューニング', '2024-06-22', 10);

COMMIT;
