-- ============================================
-- 广西六堡茶大宗交易市场价格发布系统 - 数据库Schema
-- ============================================

-- 设置字符集
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================
-- 1. 产品类别字典
-- ============================================
DROP TABLE IF EXISTS `product_categories`;
CREATE TABLE `product_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL COMMENT '类别名称',
  `code` varchar(20) NOT NULL COMMENT '类别代码',
  `sort_order` int DEFAULT 0 COMMENT '排序',
  `status` tinyint DEFAULT 1 COMMENT '状态: 0-停用 1-正常',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='产品类别';

-- 插入默认数据
INSERT INTO `product_categories` (`name`, `code`, `sort_order`) VALUES
('散茶', 'sancha', 1),
('紧压茶', 'jincha', 2),
('年份茶', 'niancha', 3),
('陈皮普洱', 'chenpicha', 4);

-- ============================================
-- 2. 产品等级字典
-- ============================================
DROP TABLE IF EXISTS `product_grades`;
CREATE TABLE `product_grades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL COMMENT '等级名称',
  `code` varchar(20) NOT NULL COMMENT '等级代码',
  `sort_order` int DEFAULT 0 COMMENT '排序',
  `status` tinyint DEFAULT 1 COMMENT '状态',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='产品等级';

INSERT INTO `product_grades` (`name`, `code`, `sort_order`) VALUES
('特级', 'teji', 1),
('一级', 'yiji', 2),
('二级', 'erji', 3),
('三级', 'sanji', 4);

-- ============================================
-- 3. 产地字典
-- ============================================
DROP TABLE IF EXISTS `product_origins`;
CREATE TABLE `product_origins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL COMMENT '产地名称',
  `code` varchar(20) NOT NULL COMMENT '产地代码',
  `region` varchar(50) DEFAULT NULL COMMENT '产区',
  `sort_order` int DEFAULT 0 COMMENT '排序',
  `status` tinyint DEFAULT 1 COMMENT '状态',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='产地';

INSERT INTO `product_origins` (`name`, `code`, `region`) VALUES
('梧州', 'wuzhou', '广西'),
('横州', 'hengzhou', '广西'),
('桂林', 'guilin', '广西'),
('柳州', 'liuzhou', '广西');

-- ============================================
-- 4. 规格字典
-- ============================================
DROP TABLE IF EXISTS `product_specs`;
CREATE TABLE `product_specs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL COMMENT '规格名称',
  `unit` varchar(20) DEFAULT NULL COMMENT '单位',
  `weight` decimal(10,3) DEFAULT NULL COMMENT '净重(kg)',
  `sort_order` int DEFAULT 0 COMMENT '排序',
  `status` tinyint DEFAULT 1 COMMENT '状态',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='规格';

INSERT INTO `product_specs` (`name`, `unit`, `weight`) VALUES
('100g', 'g', 0.100),
('357g', 'g', 0.357),
('1kg', 'kg', 1.000),
('10kg', 'kg', 10.000),
('件', '件', NULL);

-- ============================================
-- 5. 品牌/厂商
-- ============================================
DROP TABLE IF EXISTS `product_brands`;
CREATE TABLE `product_brands` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '品牌名称',
  `code` varchar(30) NOT NULL COMMENT '品牌代码',
  `contact` varchar(100) DEFAULT NULL COMMENT '联系方式',
  `address` text COMMENT '地址',
  `status` tinyint DEFAULT 1 COMMENT '状态',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='品牌';

-- ============================================
-- 6. 产品基础信息表
-- ============================================
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(30) NOT NULL COMMENT '产品编码',
  `name` varchar(100) NOT NULL COMMENT '品名',
  `category_id` int DEFAULT NULL COMMENT '类别ID',
  `grade_id` int DEFAULT NULL COMMENT '等级ID',
  `year` int DEFAULT NULL COMMENT '年份',
  `origin_id` int DEFAULT NULL COMMENT '产地ID',
  `spec_id` int DEFAULT NULL COMMENT '规格ID',
  `brand_id` int DEFAULT NULL COMMENT '品牌ID',
  `storage_type` varchar(20) DEFAULT NULL COMMENT '存储方式',
  `description` text COMMENT '产品描述',
  `image_url` varchar(500) DEFAULT NULL COMMENT '产品图片',
  `status` tinyint DEFAULT 1 COMMENT '状态: 0-停用 1-正常',
  `sort_order` int DEFAULT 0 COMMENT '排序',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_code` (`code`),
  KEY `idx_category` (`category_id`),
  KEY `idx_grade` (`grade_id`),
  KEY `idx_year` (`year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='产品';

-- ============================================
-- 7. 数据来源配置表
-- ============================================
DROP TABLE IF EXISTS `data_sources`;
CREATE TABLE `data_sources` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '来源名称',
  `type` varchar(20) NOT NULL COMMENT '类型: api/manual/crawler',
  `api_url` varchar(500) DEFAULT NULL COMMENT 'API地址',
  `api_key` varchar(255) DEFAULT NULL COMMENT 'API密钥',
  `api_secret` varchar(255) DEFAULT NULL COMMENT 'API密钥',
  `auth_type` varchar(20) DEFAULT 'none' COMMENT '认证方式',
  `selector_config` text COMMENT '爬虫选择器配置(JSON)',
  `field_mapping` text COMMENT '字段映射(JSON)',
  `crawl_schedule` varchar(50) DEFAULT NULL COMMENT 'Cron调度表达式',
  `retry_times` int DEFAULT 3 COMMENT '重试次数',
  `retry_interval` int DEFAULT 300 COMMENT '重试间隔(秒)',
  `status` tinyint DEFAULT 1 COMMENT '状态: 0-停用 1-启用',
  `last_run_at` datetime DEFAULT NULL,
  `last_success_at` datetime DEFAULT NULL,
  `error_message` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数据来源';

-- ============================================
-- 8. 每日价格表
-- ============================================
DROP TABLE IF EXISTS `daily_prices`;
CREATE TABLE `daily_prices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL COMMENT '产品ID',
  `price_date` date NOT NULL COMMENT '报价日期',
  `price_buy` decimal(12,2) DEFAULT NULL COMMENT '买入价',
  `price_sell` decimal(12,2) DEFAULT NULL COMMENT '卖出价',
  `price_avg` decimal(12,2) DEFAULT NULL COMMENT '均价',
  `price_change` decimal(12,2) DEFAULT NULL COMMENT '涨跌额',
  `price_change_percent` decimal(8,4) DEFAULT NULL COMMENT '涨跌幅%',
  `volume` int DEFAULT NULL COMMENT '成交量',
  `turnover` decimal(15,2) DEFAULT NULL COMMENT '成交额',
  `volume_unit` varchar(20) DEFAULT NULL COMMENT '成交量单位',
  `source_id` int DEFAULT NULL COMMENT '来源ID',
  `source_type` varchar(20) DEFAULT 'manual' COMMENT '来源类型',
  `source_remark` varchar(200) DEFAULT NULL COMMENT '来源备注',
  `status` tinyint DEFAULT 1 COMMENT '状态: 0-待审核 1-已发布 2-已驳回',
  `category_id` int DEFAULT NULL COMMENT '冗余字段-品类ID',
  `grade_id` int DEFAULT NULL COMMENT '冗余字段-等级ID',
  `year` int DEFAULT NULL COMMENT '冗余字段-年份',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `verified_by` int DEFAULT NULL COMMENT '审核人ID',
  `verified_at` datetime DEFAULT NULL COMMENT '审核时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_product_date` (`product_id`, `price_date`),
  KEY `idx_date` (`price_date`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='每日价格';

-- ============================================
-- 9. 日统计数据表
-- ============================================
DROP TABLE IF EXISTS `daily_statistics`;
CREATE TABLE `daily_statistics` (
  `id` int NOT NULL AUTO_INCREMENT,
  `stat_date` date NOT NULL COMMENT '统计日期',
  `total_products` int DEFAULT 0 COMMENT '报价品种数',
  `rising_count` int DEFAULT 0 COMMENT '上涨数',
  `falling_count` int DEFAULT 0 COMMENT '下跌数',
  `flat_count` int DEFAULT 0 COMMENT '持平数',
  `rising_percent` decimal(5,2) DEFAULT NULL COMMENT '上涨比例',
  `avg_price` decimal(12,2) DEFAULT NULL COMMENT '整体均价',
  `max_price` decimal(12,2) DEFAULT NULL COMMENT '最高价',
  `min_price` decimal(12,2) DEFAULT NULL COMMENT '最低价',
  `price_index` decimal(10,2) DEFAULT NULL COMMENT '价格指数',
  `total_volume` int DEFAULT 0 COMMENT '总成交量',
  `total_turnover` decimal(18,2) DEFAULT 0 COMMENT '总成交额',
  `avg_daily_volume` decimal(15,2) DEFAULT 0 COMMENT '日均成交量',
  `avg_daily_turnover` decimal(18,2) DEFAULT 0 COMMENT '日均成交额',
  `category_stats` text COMMENT '品类统计(JSON)',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_date` (`stat_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='日统计';

-- ============================================
-- 10. 用户表
-- ============================================
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(255) NOT NULL COMMENT '密码',
  `real_name` varchar(50) DEFAULT NULL COMMENT '真实姓名',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `email` varchar(100) DEFAULT NULL COMMENT '邮箱',
  `role` varchar(20) NOT NULL DEFAULT 'viewer' COMMENT '角色: admin/manager/operator/viewer',
  `status` tinyint DEFAULT 1 COMMENT '状态: 0-禁用 1-启用',
  `last_login_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户';

-- 插入管理员账户 (密码: admin123)
INSERT INTO `users` (`username`, `password`, `real_name`, `role`) VALUES
('admin', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iAt6Z5EH', '系统管理员', 'admin');

-- ============================================
-- 11. 操作日志表
-- ============================================
DROP TABLE IF EXISTS `operation_logs`;
CREATE TABLE `operation_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL COMMENT '用户ID',
  `action` varchar(50) NOT NULL COMMENT '操作类型',
  `module` varchar(50) NOT NULL COMMENT '模块',
  `content` text COMMENT '操作内容',
  `ip` varchar(50) DEFAULT NULL COMMENT 'IP地址',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user` (`user_id`),
  KEY `idx_action` (`action`),
  KEY `idx_created` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志';

-- ============================================
-- 12. 系统配置表
-- ============================================
DROP TABLE IF EXISTS `system_config`;
CREATE TABLE `system_config` (
  `id` int NOT NULL AUTO_INCREMENT,
  `key` varchar(100) NOT NULL COMMENT '配置键',
  `value` text COMMENT '配置值',
  `type` varchar(20) DEFAULT 'string' COMMENT '类型: string/json/number/boolean',
  `description` varchar(200) DEFAULT NULL COMMENT '描述',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_key` (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统配置';

INSERT INTO `system_config` (`key`, `value`, `type`, `description`) VALUES
('market_name', '广西六堡茶大宗交易市场', 'string', '市场名称'),
('price_update_time', '09:30', 'string', '价格更新时间'),
('price_publish_time', '10:00', 'string', '价格发布时间'),
('timezone', 'Asia/Shanghai', 'string', '时区'),
('currency', 'CNY', 'string', '货币');

SET FOREIGN_KEY_CHECKS = 1;
