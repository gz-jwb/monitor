-- 本地管理员用户（全权）
CREATE USER IF NOT EXISTS 'admin_local'@'localhost' IDENTIFIED BY 'u04t3fxg0imusvi7';
GRANT ALL PRIVILEGES ON *.* TO 'admin_local'@'localhost' WITH GRANT OPTION;

-- 本地编辑用户（仅限数据写操作）
CREATE USER IF NOT EXISTS 'editor_local'@'localhost' IDENTIFIED BY '82onxbxpm5jr4ne0';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER ON *.* TO 'editor_local'@'localhost';

-- 本地只读用户
CREATE USER IF NOT EXISTS 'readonly_local'@'localhost' IDENTIFIED BY 'kdVtahdYbPY9YGmt';
GRANT SELECT ON *.* TO 'readonly_local'@'localhost';

-- 远程管理员用户（全权）
CREATE USER IF NOT EXISTS 'admin_remote'@'%' IDENTIFIED BY '96qb2r6j5nuaao6a';
GRANT ALL PRIVILEGES ON *.* TO 'admin_remote'@'%' WITH GRANT OPTION;

-- 远程编辑用户（仅限数据写操作）
CREATE USER IF NOT EXISTS 'editor_remote'@'%' IDENTIFIED BY 'furmehwonubeb2ld';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER ON *.* TO 'editor_remote'@'%';

-- 远程只读用户
CREATE USER IF NOT EXISTS 'readonly_remote'@'%' IDENTIFIED BY 'eEEjbJ6HreBqUA3w';
GRANT SELECT ON *.* TO 'readonly_remote'@'%';

-- 刷新权限使其生效
FLUSH PRIVILEGES;