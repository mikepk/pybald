

CREATE TABLE IF NOT EXISTS `versions` (
    `version_id` mediumint(4) unsigned NOT NULL auto_increment,
    `subversion` mediumint(4) unsigned NOT NULL default 0,
    PRIMARY KEY (`version_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- MK v 0.0
-- Versions table
SET @max_version = (SELECT MAX(version_id) FROM versions);
UPDATE versions SET subversion = subversion + 1 WHERE version_id = @max_version; 


-- MK sessions table
DROP TABLE IF EXISTS `sessions`;
CREATE TABLE `sessions` (
    `session_id` char(128) NOT NULL default '',
    `cache` varchar(8192) NOT NULL default '',
    `user_id` mediumint(4) unsigned NOT NULL default 0,
    `date_modified` timestamp NOT NULL default CURRENT_TIMESTAMP,
    PRIMARY KEY (`session_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- The users table
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `user_id` mediumint(4) unsigned NOT NULL auto_increment,
    `email` varchar(40) NOT NULL default '',
    `username` varchar(40) NOT NULL default '',
    `password` varchar(16) NOT NULL default '',
    `main_card_id` mediumint(4) unsigned NOT NULL default 0,
    `status` varchar(4) NOT NULL default 'OK',
    `date_created` timestamp NOT NULL default '0000-00-00 00:00:00',
    `date_modified` timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
    PRIMARY KEY (`user_id`),
    UNIQUE KEY `email` (`email`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
