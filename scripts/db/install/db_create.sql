
DROP DATABASE IF EXISTS `cantor`;
CREATE DATABASE IF NOT EXISTS `cantor`;

-- GRANT ALL PRIVILEGES ON `cantor`.* TO 'cantor'@'localhost' identified by 'cantor';
-- FLUSH PRIVILEGES;

use `cantor`;

DROP TABLE IF EXISTS `status`;
CREATE TABLE IF NOT EXISTS `status` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_name`(`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `combo`;
CREATE TABLE IF NOT EXISTS `combo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `uuid` binary(16) NOT NULL,
  `name` varchar(1000) NOT NULL,
  `description` text NULL,
  `status_id` int NOT NULL DEFAULT 0,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_updated_ts`(`updated_ts`),
  KEY `idx_updated_ts_status_id`(`updated_ts`, `status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `combo_media`;
CREATE TABLE IF NOT EXISTS `combo_media` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `combo_id` bigint NOT NULL,
  `media_id` binary(16) NOT NULL,
  `display_order` int NOT NULL DEFAULT 0,
  `status_id` bigint NOT NULL DEFAULT 0,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_updated_ts`(`updated_ts`),
  KEY `idx_combo_id`(`combo_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `entity_combo`;
CREATE TABLE IF NOT EXISTS `entity_combo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `entity_id` bigint NOT NULL,
  `entity_type` ENUM('product', 'variant', 'subscription') NOT NULL,
  `combo_id` bigint NOT NULL,
  `quantity` int NOT NULL DEFAULT 1,
  `display_order` int NOT NULL DEFAULT 0,
  `status_id` bigint NOT NULL DEFAULT 0,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_updated_ts`(`updated_ts`),
  KEY `idx_combo_id`(`combo_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `product`;
CREATE TABLE IF NOT EXISTS `product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `uuid` binary(16) NOT NULL,
  `name` varchar(1000) NOT NULL,
  `description` text NULL,
  `category_id` bigint NOT NULL,
  `status_id` int NOT NULL DEFAULT 0,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_updated_ts`(`updated_ts`),
  KEY `idx_updated_ts_status_id`(`updated_ts`, `status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `product_media`;
CREATE TABLE IF NOT EXISTS `product_media` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_id` bigint NOT NULL,
  `media_id` binary(16) NOT NULL,
  `display_order` int NOT NULL DEFAULT 0,
  `status_id` bigint NOT NULL DEFAULT 0,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_updated_ts`(`updated_ts`),
  KEY `idx_product_id`(`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `category`;
CREATE TABLE IF NOT EXISTS `category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `parent_id` bigint NOT NULL,
  `name` varchar(1000) NOT NULL,
  `description` text NULL,
  `status_id` bigint NOT NULL DEFAULT 0,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `category_media`;
CREATE TABLE IF NOT EXISTS `category_media` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `category_id` bigint NOT NULL,
  `media_id` binary(16) NOT NULL,
  `display_order` int NOT NULL DEFAULT 0,
  `status_id` bigint NOT NULL DEFAULT 0,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_updated_ts`(`updated_ts`),
  KEY `idx_category_id`(`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `attribute`;
CREATE TABLE IF NOT EXISTS `attribute` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `value_type` ENUM('varchar', 'int', 'bigint', 'char', 'float', 'double', 'decimal', 'date', 'time', 'datetime') NOT NULL,
  `constraint` varchar(100) NULL,
  `cardinality` ENUM('one', 'many') NOT NULL DEFAULT 'one',
  `description` varchar(1000) NULL,
  `validation` ENUM('strict', 'free'),
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `attribute_media`;
CREATE TABLE IF NOT EXISTS `attribute_media` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `attribute_id` bigint NOT NULL,
  `media_id` binary(16) NOT NULL,
  `display_order` int NOT NULL DEFAULT 0,
  `status_id` bigint NOT NULL DEFAULT 0,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_updated_ts`(`updated_ts`),
  KEY `idx_attribute_id`(`attribute_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `unit`;
CREATE TABLE IF NOT EXISTS `unit` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `unit_synonym`;
CREATE TABLE IF NOT EXISTS `unit_synonym` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `unit_id` bigint NOT NULL,
  `synonym` varchar(100) NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `unit_conversion`;
CREATE TABLE IF NOT EXISTS `unit_conversion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `from_unit_id` bigint NOT NULL,
  `to_unit_id` bigint NOT NULL,
  `slope` float NOT NULL DEFAULT 1,
  `intercept` float NOT NULL DEFAULT 0,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `attribute_group`;
CREATE TABLE IF NOT EXISTS `attribute_group` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `seperator` varchar(5) NOT NULL DEFAULT ' x ',
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `attribute_group_media`;
CREATE TABLE IF NOT EXISTS `attribute_group_media` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `attribute_group_id` bigint NOT NULL,
  `media_id` binary(16) NOT NULL,
  `display_order` int NOT NULL DEFAULT 0,
  `status_id` bigint NOT NULL DEFAULT 0,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `attribute_attribute_group`;
CREATE TABLE IF NOT EXISTS `attribute_attribute_group` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `attribute_id` bigint NOT NULL,
  `attribute_group_id` bigint NOT NULL,
  `display_order` bigint NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `category_attribute`;
CREATE TABLE IF NOT EXISTS `category_attribute` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `category_id` bigint NOT NULL,
  `attribute_id` bigint NOT NULL,
  `required` bit NOT NULL DEFAULT 0,
  `filter_enabled` bit NOT NULL DEFAULT 0,
  `display_order` int NOT NULL DEFAULT 0,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `attribute_unit`;
CREATE TABLE IF NOT EXISTS `attribute_unit` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `attribute_id` bigint NOT NULL,
  `unit_id` bigint NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
 
DROP TABLE IF EXISTS `product_attribute_value`;
CREATE TABLE IF NOT EXISTS `product_attribute_value` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_id` bigint NOT NULL,
  `attribute_id` bigint NOT NULL,
  `value_id` bigint NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `value_varchar`;
CREATE TABLE IF NOT EXISTS `value_varchar` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `value` varchar(1000) NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `value_int`;
CREATE TABLE IF NOT EXISTS `value_int` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `value` int NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `value_bigint`;
CREATE TABLE IF NOT EXISTS `value_bigint` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `value` bigint NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `value_char`;
CREATE TABLE IF NOT EXISTS `value_char` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `value` char NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `value_float`;
CREATE TABLE IF NOT EXISTS `value_float` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `value` float NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `value_double`;
CREATE TABLE IF NOT EXISTS `value_double` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `value` double NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `value_decimal`;
CREATE TABLE IF NOT EXISTS `value_decimal` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `value` decimal NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `value_date`;
CREATE TABLE IF NOT EXISTS `value_date` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `value` date NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `value_time`;
CREATE TABLE IF NOT EXISTS `value_time` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `value` time NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `value_datetime`;
CREATE TABLE IF NOT EXISTS `value_datetime` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `value` datetime NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `product_attribute_value_unit`;
CREATE TABLE IF NOT EXISTS `product_attribute_value_unit` (
  `product_attribute_value_id` bigint NOT NULL,
  `unit_id` bigint NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`product_attribute_value_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `variant`;
CREATE TABLE IF NOT EXISTS `variant` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `uuid` binary(16) NOT NULL,
  `product_id` bigint NOT NULL,
  `name` varchar(1000) NULL,
  `description` text NULL,
  `display_order` int NOT NULL DEFAULT 0,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `entity_similar`;
CREATE TABLE IF NOT EXISTS `entity_similar` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `entity_id` bigint NOT NULL,
  `entity_type` ENUM('subscription', 'variant', 'product', 'combo') NOT NULL,
  `similar_entity_id` bigint NOT NULL,
  `similar_entity_type` ENUM('subscription', 'variant', 'product', 'combo') NOT NULL,
  `affinity` float NOT NULL DEFAULT 1,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `variant_media`;
CREATE TABLE IF NOT EXISTS `variant_media` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `variant_id` bigint NOT NULL,
  `media_id` binary(16) NOT NULL,
  `display_order` int NOT NULL DEFAULT 0,
  `status_id` bigint NOT NULL DEFAULT 0,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_updated_ts`(`updated_ts`),
  KEY `idx_variant_id`(`variant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `variant_product_attribute_value`;
CREATE TABLE IF NOT EXISTS `variant_product_attribute_value` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `variant_id` bigint NOT NULL,
  `product_attribute_value_id` bigint NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `seller`;
CREATE TABLE IF NOT EXISTS `seller` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(1000) NOT NULL,
  `description` text NULL,
  `address` text NOT NULL,
  `voice_contact` varchar(50) NOT NULL,
  `email` varchar(50) NULL,
  `status_id` int NOT NULL DEFAULT 0,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_updated_ts`(`updated_ts`),
  KEY `idx_updated_ts_status_id`(`updated_ts`, `status_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `subscription`;
CREATE TABLE IF NOT EXISTS `subscription` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `uuid` binary(16) NOT NULL,
  `variant_id` bigint NOT NULL,
  `seller_id` bigint NOT NULL,
  `transfer_price` float NOT NULL,
  `take_rate` float NOT NULL,
  `seller_indicated_price` float NOT NULL,
  `quantity_available` int NOT NULL DEFAULT 0,
  `valid_from` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `valid_thru` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `condition`;
CREATE TABLE IF NOT EXISTS `condition` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `status_id` bigint NOT NULL DEFAULT 0,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `subscription_condition`;
CREATE TABLE IF NOT EXISTS `subscription_condition` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subscription_id` bigint NOT NULL,
  `condition_id` bigint NOT NULL,
  `status_id` bigint NOT NULL DEFAULT 0,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `subscription_geo`;
CREATE TABLE IF NOT EXISTS `subscription_geo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subscription_id` bigint NOT NULL,
  `geo_id` bigint NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `subscription_geo_condition`;
CREATE TABLE IF NOT EXISTS `subscription_geocondition` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subscription_geo_id` bigint NOT NULL,
  `condition_id` bigint NOT NULL,
  `status_id` bigint NOT NULL DEFAULT 0,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `shipping_type`;
CREATE TABLE IF NOT EXISTS `shipping_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `shipping_type_media`;
CREATE TABLE IF NOT EXISTS `shipping_type_media` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `shipping_type_id` bigint NOT NULL,
  `media_id` binary(16) NOT NULL,
  `display_order` int NOT NULL DEFAULT 0,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `subscription_geo_shipping`;
CREATE TABLE IF NOT EXISTS `subscription_geo_shipping` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subscription_geo_id` bigint NOT NULL,
  `shipping_type_id` bigint NOT NULL,
  `shipping_charge` float NOT NULL DEFAULT 0,
  `valid_from` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `valid_thru` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `offer`;
CREATE TABLE IF NOT EXISTS `offer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `discount_percent` float NOT NULL DEFAULT 0,
  `valid_from` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `valid_thru` datetime NOT NULL DEFAULT '1970-01-01 00:00:00',
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `offer_subscription`;
CREATE TABLE IF NOT EXISTS `offer_subscription` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subscription_id` bigint NOT NULL,
  `offer_id` bigint NOT NULL DEFAULT 0,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `offer_media`;
CREATE TABLE IF NOT EXISTS `offer_media` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `offer_id` bigint NOT NULL,
  `media_id` binary(16) NOT NULL,
  `display_order` int NOT NULL DEFAULT 0,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `store_front`;
CREATE TABLE IF NOT EXISTS `store_front` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(1000) NOT NULL,
  `description` text NULL,
  `meta_tags` text NULL,
  `template` varchar(100) NULL,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `store_front_media`;
CREATE TABLE IF NOT EXISTS `store_front_media` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `store_front_id` bigint NOT NULL,
  `media_id` binary(16) NOT NULL,
  `media_role` varchar(100) NULL,
  `display_order` int NOT NULL DEFAULT 0,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `store_front_entity`;
CREATE TABLE IF NOT EXISTS `store_front_entity` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `store_front_id` bigint NOT NULL,
  `entity_id` bigint NOT NULL,
  `entity_type` ENUM('product', 'variant', 'subscription', 'combo') NOT NULL,
  `display_order` int NOT NULL DEFAULT 0,
  `status_id` bigint NOT NULL,
  `created_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by_id` bigint NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

