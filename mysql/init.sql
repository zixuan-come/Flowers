CREATE DATABASE IF NOT EXISTS flowers CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE flowers;

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    icon VARCHAR(50) DEFAULT '📁',
    sort_order INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scripts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    language VARCHAR(20) NOT NULL DEFAULT 'python',
    code LONGTEXT NOT NULL,
    category_id INT,
    tags VARCHAR(200) DEFAULT '',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- 插入一些默认分类
INSERT INTO categories (name, icon, sort_order) VALUES
('爬虫', '🕷️', 1),
('自动化', '⚙️', 2),
('数据处理', '📊', 3),
('网络工具', '🌐', 4),
('文件操作', '📂', 5),
('其他', '🔧', 6);
