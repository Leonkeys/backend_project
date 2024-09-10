
CREATE TABLE tbl_user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(64) UNIQUE,
    nickname VARCHAR(128),
    is_super BOOLEAN NOT NULL DEFAULT FALSE,
    mobile VARCHAR(32),
    email VARCHAR(64) UNIQUE,
    password VARCHAR(128) NOT NULL,
    avatar VARCHAR(256) NULL
);

CREATE TABLE tbl_role (
    id INTEGER PRIMARY KEY,
    name VARCHAR(32) DEFAULT NULL,
    nick_name VARCHAR(64) DEFAULT NULL,
    description VARCHAR(256) DEFAULT NULL
);


CREATE TABLE tbl_menu (
    id PRIMARY INT AUTO_INCREMENT,
    title  VARCHAR(127) NOT NULL,
    name VARCHAR (31) NOT NULL,
    path VARCHAR(64) NOT NULL,
    method VARCHAR(16) NOT NULL,
    action VARCHAR(32) NOT NULL,
    is_menu BOOLEAN NOT NULL DEFAULT TRUE,
    parent_id INT NULL,
    meta JSON NULL
);
