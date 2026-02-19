DROP DATABASE IF EXISTS snsapp;

DROP USER IF EXISTS 'testuser'@'%';


CREATE USER 'testuser'@'%' IDENTIFIED BY 'testuser';

CREATE DATABASE IF NOT EXISTS snsapp
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;


GRANT ALL PRIVILEGES ON snsapp.* TO 'testuser'@'%';

FLUSH PRIVILEGES;

USE snsapp;

CREATE TABLE
    users (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
	introduce TEXT NULL,
	icon_file_name VARCHAR(255) NULL,
        updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        PRIMARY KEY (id),
        UNIQUE KEY uq_users_email (email)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    posts (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id BIGINT UNSIGNED NOT NULL,
        content TEXT NOT NULL,
        created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        deleted_at DATETIME (6) DEFAULT NULL,
        PRIMARY KEY (id),
        KEY idx_posts_user_id (user_id),
        CONSTRAINT fk_posts_user FOREIGN KEY (user_id) REFERENCES users (id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    comments (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id BIGINT UNSIGNED NOT NULL,
        post_id BIGINT UNSIGNED NOT NULL,
        content TEXT NOT NULL,
        created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        PRIMARY KEY (id),
        KEY idx_comments_user_id (user_id),
        KEY idx_comments_post_id (post_id),
        CONSTRAINT fk_comments_user FOREIGN KEY (user_id) REFERENCES users (id),
        CONSTRAINT fk_comments_post FOREIGN KEY (post_id) REFERENCES posts (id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;


CREATE TABLE
    likes (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id BIGINT UNSIGNED NOT NULL,
        post_id BIGINT UNSIGNED NULL,
	comment_id BIGINT UNSIGNED NULL,
        PRIMARY KEY (id),
        KEY idx_likes_user_id (user_id),
        KEY idx_likes_post_id (post_id),
        KEY idx_likes_comment_id (comment_id),
        CONSTRAINT fk_likes_user FOREIGN KEY (user_id) REFERENCES users (id),
        CONSTRAINT fk_likes_post FOREIGN KEY (post_id) REFERENCES posts (id),
        CONSTRAINT fk_likes_comment FOREIGN KEY (comment_id) REFERENCES comments (id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    medias (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id BIGINT UNSIGNED NOT NULL,
        post_id BIGINT UNSIGNED NOT NULL,
	file_name VARCHAR(255) NULL,
        created_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
        updated_at DATETIME (6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
        PRIMARY KEY (id),
        KEY idx_medias_user_id (user_id),
        KEY idx_medias_post_id (post_id),
        CONSTRAINT fk_medias_user FOREIGN KEY (user_id) REFERENCES users (id),
        CONSTRAINT fk_medias_post FOREIGN KEY (post_id) REFERENCES posts (id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE
    post_medias (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id BIGINT UNSIGNED NOT NULL,
        post_id BIGINT UNSIGNED NOT NULL,
	media_id BIGINT UNSIGNED NOT NULL,
        PRIMARY KEY (id),
        KEY idx_post_medias_conn_user_id (user_id),
        KEY idx_post_medias_conn_post_id (post_id),
        KEY idx_post_medias_conn_media_id (media_id),
        CONSTRAINT fk_post_medias_user FOREIGN KEY (user_id) REFERENCES users (id),
        CONSTRAINT fk_post_medias_post FOREIGN KEY (post_id) REFERENCES posts (id),
        CONSTRAINT fk_post_medias_media FOREIGN KEY (media_id) REFERENCES medias (id)
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE follows (
    follower_id BIGINT UNSIGNED NOT NULL,
    followed_id BIGINT UNSIGNED NOT NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (follower_id, followed_id),
    KEY idx_followed (followed_id),
    CONSTRAINT fk_follows_follower FOREIGN KEY (follower_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_follows_followed FOREIGN KEY (followed_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

INSERT INTO users (name, email, password)
VALUES 
  ('山田太郎', 'taro@example.com', '$argon2id$v=19$m=65536,t=3,p=4$TuRgOIrd3A2HL6daX6kYdg$4iZGaBeVSzkORfmPawS5NXCFgf8ZoXPvETqA0OgqM7M'),
  ('鈴木二郎', 'jiro@example.com', '$argon2id$v=19$m=65536,t=3,p=4$TuRgOIrd3A2HL6daX6kYdg$4iZGaBeVSzkORfmPawS5NXCFgf8ZoXPvETqA0OgqM7M');

INSERT INTO posts (user_id, content)
VALUES
  (1, 'こんにちは！初めての投稿です。'),
  (1, '今日はとても良い天気ですね。'),
  (1, '今日も勉強頑張ります！'),
  (2, 'おはよう！初めての投稿です。'),
  (2, '今日は晴れそうですね。'),
  (2, '今日から勉強頑張ります！');



INSERT INTO comments (user_id, post_id, content)
VALUES
    (2, 1, '応援しています！頑張ってください。');
