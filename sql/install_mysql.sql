-- *******************************************************************************************
-- **  File:  mysql-preferred.sql
-- **  Description: Creates the preferred database
-- **  Created: 10-03-2020
-- **
-- **  History:
-- **  10-08-2020: Initial version
-- **  24-04-2022: Added drop script
-- **
-- *******************************************************************************************

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS activity_log;
DROP TABLE IF EXISTS album;
DROP TABLE IF EXISTS xxx_album;
DROP TABLE IF EXISTS application;
DROP TABLE IF EXISTS xxx_application;
DROP TABLE IF EXISTS artist;
DROP TABLE IF EXISTS xxx_artist;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS xxx_customer;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS xxx_employee;
DROP TABLE IF EXISTS genre;
DROP TABLE IF EXISTS xxx_genre;
DROP TABLE IF EXISTS invoice;
DROP TABLE IF EXISTS xxx_invoice;
DROP TABLE IF EXISTS invoice_item;
DROP TABLE IF EXISTS xxx_invoice_item;
DROP TABLE IF EXISTS log;
DROP TABLE IF EXISTS media_type;
DROP TABLE IF EXISTS xxx_media_type;
DROP TABLE IF EXISTS playlist;
DROP TABLE IF EXISTS xxx_playlist;
DROP TABLE IF EXISTS playlist_track;
DROP TABLE IF EXISTS xxx_playlist_track;
DROP TABLE IF EXISTS setup;
DROP TABLE IF EXISTS track;
DROP TABLE IF EXISTS xxx_track;
DROP TABLE IF EXISTS user_setup;
DROP TABLE IF EXISTS version;

DROP VIEW IF EXISTS albums;
DROP VIEW IF EXISTS invoices;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE application (
	`ID`                 int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	`key`                char(3)  NOT NULL    ,
	name                 varchar(100)  NOT NULL    ,
	comments             text      ,
	version              tinyint  NOT NULL DEFAULT 1   ,
	created_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	updated_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT uk_application UNIQUE ( `key` )
 );

ALTER TABLE application ADD CONSTRAINT `Cns_application_key` CHECK (`key` IS NOT NULL OR LENGTH(`key`) = 3 );

ALTER TABLE application ADD CONSTRAINT `Cns_application_name` CHECK (name IS NOT NULL OR LENGTH(name) >= 5 );

CREATE TABLE artist (
	`ID`                 int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	name                 varchar(100)  NOT NULL    ,
	name_lower           varchar(100)  NOT NULL    ,
	version              tinyint  NOT NULL DEFAULT 1   ,
	created_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	updated_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT `Uk_artist_name` UNIQUE ( name_lower )
 );

CREATE TABLE employee (
	`ID`                 int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	title                varchar(25)      ,
	first_name           varchar(30)  NOT NULL    ,
	last_name            varchar(60)  NOT NULL    ,
	date_of_birth        date      ,
	hire_date            date  NOT NULL    ,
	address              varchar(50)  NOT NULL    ,
	city                 varchar(30)  NOT NULL    ,
	state                varchar(12)      ,
	country              varchar(25)      ,
	post_code            varchar(12)      ,
	phone                varchar(25)      ,
	fax                  varchar(25)      ,
	email                varchar(50)  NOT NULL    ,
	manager_id           int      ,
	version              tinyint  NOT NULL DEFAULT 1   ,
	created_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	updated_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT `Idx_employee_email` UNIQUE ( email ) ,
	CONSTRAINT `Fk_employee_employee` FOREIGN KEY ( manager_id ) REFERENCES employee( `ID` ) ON DELETE NO ACTION ON UPDATE NO ACTION
 );

CREATE INDEX `Idx_employee_manager_id` ON employee ( manager_id );

CREATE TABLE genre (
	`ID`                 int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	name                 varchar(30)  NOT NULL    ,
	name_lower           varchar(30)  NOT NULL    ,
	version              tinyint  NOT NULL DEFAULT 1   ,
	created_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	updated_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT `Uk_genre_name` UNIQUE ( name_lower )
 );

CREATE TABLE log (
	`ID`                 bigint  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	app_id               int  NOT NULL    ,
	entry_type           varchar(10)  NOT NULL    ,
	logged_at            timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	message              text  NOT NULL    ,
	method_name          varchar(100)      ,
	stack                text      ,
	extra                text      ,
	CONSTRAINT fk_log_application FOREIGN KEY ( app_id ) REFERENCES application( `ID` ) ON DELETE NO ACTION ON UPDATE NO ACTION
 );

ALTER TABLE log ADD CONSTRAINT `Cns_log_entry_type` CHECK ( entry_type IN ('INFO', 'WARNING', 'ERROR', 'FATAL', 'DEBUG') );

CREATE TABLE media_type (
	`ID`                 int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	name                 varchar(40)  NOT NULL    ,
	name_lower           varchar(40)  NOT NULL    ,
	version              tinyint  NOT NULL DEFAULT 1   ,
	created_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	updated_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT `Uk_media_type_name` UNIQUE ( name_lower )
 );

CREATE TABLE playlist (
	`ID`                 int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	name                 varchar(40)  NOT NULL    ,
	name_lower           varchar(40)  NOT NULL    ,
	version              tinyint  NOT NULL DEFAULT 1   ,
	created_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	updated_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT `Uk_playlist_name` UNIQUE ( name_lower )
 );

CREATE TABLE setup (
	`ID`                 int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	`key`                varchar(20)  NOT NULL    ,
	value                varchar(300)  NOT NULL    ,
	data_type            varchar(20)  NOT NULL    ,
	app_id               int  NOT NULL    ,
	version              tinyint  NOT NULL DEFAULT 1   ,
	created_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	updated_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT fk_setup_application FOREIGN KEY ( app_id ) REFERENCES application( `ID` ) ON DELETE CASCADE ON UPDATE CASCADE
 );

CREATE TABLE user_setup (
	`ID`                 int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	`key`                varchar(20)  NOT NULL    ,
	value                varchar(300)  NOT NULL    ,
	data_type            varchar(20)  NOT NULL    ,
	usr                  varchar(30)  NOT NULL    ,
	app_id               int  NOT NULL    ,
	version              tinyint  NOT NULL DEFAULT 1   ,
	created_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	updated_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT fk_setup_application_0 FOREIGN KEY ( app_id ) REFERENCES application( `ID` ) ON DELETE CASCADE ON UPDATE CASCADE
 );

CREATE TABLE version (
	`ID`                 int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	major                tinyint  NOT NULL DEFAULT 1   ,
	minor                smallint  NOT NULL DEFAULT 0   ,
	build                smallint  NOT NULL DEFAULT 1   ,
	started_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	ended_at             timestamp      ,
	status               varchar(10)  NOT NULL DEFAULT 'STARTED'   ,
	comments             text
 );

ALTER TABLE version ADD CONSTRAINT `Cns_version_status` CHECK ( status in ('STARTED', 'RUNNING', 'ENDED', 'FAILED') );

CREATE TABLE xxx_album (
	`ID`                 bigint  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	changed_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	action               char(1)  NOT NULL    ,
	record_id            int  NOT NULL    ,
	version_id           tinyint  NOT NULL    ,
	usr                  varchar(30)      ,
	app                  int      ,
	title                varchar(120)      ,
	title_lower          varchar(120)      ,
	artist_id            int
 );

CREATE TABLE xxx_application (
	`ID`                 bigint  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	changed_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	action               char(1)  NOT NULL    ,
	record_id            int  NOT NULL    ,
	version_id           tinyint  NOT NULL    ,
	usr                  varchar(30)      ,
	app                  int      ,
	`key`                char(3)      ,
	name                 varchar(100)      ,
	comments             text
 );

CREATE TABLE xxx_artist (
	`ID`                 bigint  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	changed_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	action               char(1)  NOT NULL    ,
	record_id            int  NOT NULL    ,
	version_id           tinyint  NOT NULL    ,
	usr                  varchar(30)      ,
	app                  int      ,
	name                 varchar(100)      ,
	name_lower           varchar(100)
 );

CREATE TABLE xxx_customer (
	`ID`                 bigint  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	changed_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	action               char(1)  NOT NULL    ,
	record_id            int  NOT NULL    ,
	version_id           tinyint  NOT NULL    ,
	usr                  varchar(30)      ,
	app                  int      ,
	first_name           varchar(30)      ,
	last_name            varchar(60)      ,
	company              varchar(60)      ,
	address              varchar(50)      ,
	city                 varchar(30)      ,
	state                varchar(12)      ,
	country              varchar(25)      ,
	post_code            varchar(12)      ,
	phone                varchar(25)      ,
	fax                  varchar(25)      ,
	email                varchar(50)      ,
	support_rep_id       int
 );

CREATE TABLE xxx_employee (
	`ID`                 bigint  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	changed_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	action               char(1)  NOT NULL    ,
	record_id            int  NOT NULL    ,
	version_id           tinyint  NOT NULL    ,
	usr                  varchar(30)      ,
	app                  int      ,
	title                varchar(25)      ,
	first_name           varchar(30)      ,
	last_name            varchar(60)      ,
	address              varchar(50)      ,
	city                 varchar(30)      ,
	state                varchar(12)  NOT NULL    ,
	country              varchar(25)      ,
	post_code            varchar(12)      ,
	phone                varchar(25)      ,
	fax                  varchar(25)      ,
	email                varchar(50)      ,
	manager_id           int
 );

CREATE TABLE xxx_genre (
	`ID`                 bigint  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	changed_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	action               char(1)  NOT NULL    ,
	record_id            int  NOT NULL    ,
	version_id           tinyint  NOT NULL    ,
	usr                  varchar(30)      ,
	app                  int      ,
	name                 varchar(30)      ,
	name_lower           varchar(30)
 );

CREATE TABLE xxx_invoice (
	`ID`                 bigint  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	changed_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	action               char(1)  NOT NULL    ,
	record_id            int  NOT NULL    ,
	version_id           tinyint  NOT NULL    ,
	usr                  varchar(30)      ,
	app                  int      ,
	invoice_date         date      ,
	address              varchar(50)      ,
	city                 varchar(25)      ,
	state                varchar(12)      ,
	country              varchar(30)      ,
	post_code            varchar(12)      ,
	total                decimal      ,
	customer_id          int
 );

CREATE TABLE xxx_invoice_item (
	`ID`                 bigint  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	changed_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	action               char(1)  NOT NULL    ,
	record_id            int  NOT NULL    ,
	version_id           tinyint  NOT NULL    ,
	usr                  varchar(30)      ,
	app                  int      ,
	invoice_id           int      ,
	track_id             int      ,
	unit_price           decimal      ,
	quantity             int
 );

CREATE TABLE xxx_media_type (
	`ID`                 bigint  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	changed_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	action               char(1)  NOT NULL    ,
	record_id            int  NOT NULL    ,
	version_id           tinyint  NOT NULL    ,
	usr                  varchar(30)      ,
	app                  int      ,
	name                 varchar(40)      ,
	name_lower           varchar(40)
 );

CREATE TABLE xxx_playlist (
	`ID`                 bigint  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	changed_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	action               char(1)  NOT NULL    ,
	record_id            int  NOT NULL    ,
	version_id           tinyint  NOT NULL    ,
	usr                  varchar(30)      ,
	app                  int      ,
	name                 varchar(40)      ,
	name_lower           varchar(40)
 );

CREATE TABLE xxx_playlist_track (
	`ID`                 bigint  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	changed_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	action               char(1)  NOT NULL    ,
	record_id            int  NOT NULL    ,
	version_id           tinyint  NOT NULL    ,
	usr                  varchar(30)      ,
	app                  int      ,
	playlist_id          int      ,
	track_id             int
 );

CREATE TABLE xxx_track (
	`ID`                 bigint  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	changed_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	action               char(1)  NOT NULL    ,
	record_id            int  NOT NULL    ,
	version_id           tinyint  NOT NULL    ,
	usr                  varchar(30)      ,
	app                  int      ,
	name                 varchar(150)      ,
	composers            varchar(200)      ,
	milliseconds         int      ,
	bytes                int      ,
	unit_price           decimal      ,
	album_id             int      ,
	media_type_id        int      ,
	genre_id             int
 );

CREATE TABLE activity_log (
	`ID`                 bigint  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	app_id               int  NOT NULL    ,
	message              text  NOT NULL    ,
	CONSTRAINT fk_activity_log_application FOREIGN KEY ( app_id ) REFERENCES application( `ID` ) ON DELETE CASCADE ON UPDATE CASCADE
 );

CREATE TABLE album (
	`ID`                 int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	title                varchar(120)  NOT NULL    ,
	title_lower          varchar(120)  NOT NULL    ,
	artist_id            int  NOT NULL    ,
	version              tinyint  NOT NULL DEFAULT 1   ,
	created_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	updated_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT `Uk_album_title` UNIQUE ( title_lower ) ,
	CONSTRAINT `Fk_album_artist` FOREIGN KEY ( artist_id ) REFERENCES artist( `ID` ) ON DELETE NO ACTION ON UPDATE NO ACTION
 );

CREATE INDEX `Idx_album_artist_id` ON album ( artist_id );

CREATE TABLE customer (
	`ID`                 int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	first_name           varchar(30)  NOT NULL    ,
	last_name            varchar(60)  NOT NULL    ,
	company              varchar(60)      ,
	address              varchar(50)  NOT NULL    ,
	city                 varchar(30)  NOT NULL    ,
	state                varchar(12)      ,
	country              varchar(25)  NOT NULL    ,
	post_code            varchar(12)      ,
	phone                varchar(25)      ,
	fax                  varchar(25)      ,
	email                varchar(50)  NOT NULL    ,
	support_rep_id       int      ,
	version              tinyint  NOT NULL DEFAULT 1   ,
	created_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	updated_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT `Uk_customer_email` UNIQUE ( email ) ,
	CONSTRAINT `Fk_customer_employee` FOREIGN KEY ( support_rep_id ) REFERENCES employee( `ID` ) ON DELETE NO ACTION ON UPDATE NO ACTION
 );

CREATE INDEX `Idx_customer_support_rep_id` ON customer ( support_rep_id );

CREATE TABLE invoice (
	`ID`                 int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	invoice_date         datetime  NOT NULL    ,
	address              varchar(50)  NOT NULL    ,
	city                 varchar(25)  NOT NULL    ,
	state                varchar(12)      ,
	country              varchar(30)  NOT NULL    ,
	post_code            varchar(12)      ,
	total                decimal  NOT NULL    ,
	customer_id          int  NOT NULL    ,
	version              tinyint  NOT NULL DEFAULT 1   ,
	created_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	updated_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT `Fk_invoice_customer` FOREIGN KEY ( customer_id ) REFERENCES customer( `ID` ) ON DELETE NO ACTION ON UPDATE NO ACTION
 );

CREATE INDEX `Idx_invoice_customer_id` ON invoice ( customer_id );

CREATE TABLE track (
	`ID`                 int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	name                 varchar(150)  NOT NULL    ,
	composer             varchar(200)      ,
	milliseconds         int      ,
	bytes                int      ,
	unit_price           decimal  NOT NULL    ,
	album_id             int  NOT NULL    ,
	media_type_id        int  NOT NULL    ,
	genre_id             int  NOT NULL    ,
	version              tinyint  NOT NULL DEFAULT 1   ,
	created_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	updated_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT `Fk_track_album` FOREIGN KEY ( album_id ) REFERENCES album( `ID` ) ON DELETE NO ACTION ON UPDATE NO ACTION,
	CONSTRAINT `Fk_track_media_type` FOREIGN KEY ( media_type_id ) REFERENCES media_type( `ID` ) ON DELETE NO ACTION ON UPDATE NO ACTION,
	CONSTRAINT `Fk_track_genre` FOREIGN KEY ( genre_id ) REFERENCES genre( `ID` ) ON DELETE NO ACTION ON UPDATE NO ACTION
 );

CREATE INDEX `Idx_track_album_id` ON track ( album_id );

CREATE INDEX `Idx_track_media_type_id` ON track ( media_type_id );

CREATE INDEX `Idx_track_genre_id` ON track ( genre_id );

CREATE TABLE invoice_item (
	`ID`                 int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	quantity             int  NOT NULL    ,
	unit_price           decimal  NOT NULL    ,
	track_id             int  NOT NULL    ,
	invoice_id           int  NOT NULL    ,
	version              tinyint  NOT NULL DEFAULT 1   ,
	created_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	updated_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT `Fk_invoice_item_track` FOREIGN KEY ( track_id ) REFERENCES track( `ID` ) ON DELETE NO ACTION ON UPDATE NO ACTION,
	CONSTRAINT `Fk_invoice_item_invoice` FOREIGN KEY ( invoice_id ) REFERENCES invoice( `ID` ) ON DELETE NO ACTION ON UPDATE NO ACTION
 );

CREATE INDEX `Idx_invoice_item_track_id` ON invoice_item ( track_id );

CREATE INDEX `Idx_invoice_item_invoice_id` ON invoice_item ( invoice_id );

CREATE TABLE playlist_track (
	`ID`                 int  NOT NULL  AUTO_INCREMENT  PRIMARY KEY,
	playlist_id          int  NOT NULL    ,
	track_id             int  NOT NULL    ,
	version              tinyint  NOT NULL DEFAULT 1   ,
	created_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	updated_at           timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP   ,
	CONSTRAINT `Uk_playlist_track_playlist_id_track_id` UNIQUE ( playlist_id, track_id ) ,
	CONSTRAINT `Fk_playlist_track_playlist` FOREIGN KEY ( playlist_id ) REFERENCES playlist( `ID` ) ON DELETE NO ACTION ON UPDATE NO ACTION,
	CONSTRAINT `Fk_playlist_track_track` FOREIGN KEY ( track_id ) REFERENCES track( `ID` ) ON DELETE NO ACTION ON UPDATE NO ACTION
 );

CREATE INDEX `Idx_playlist_track_playlist_id` ON playlist_track ( playlist_id );

CREATE INDEX `Idx_playlist_track_track_id` ON playlist_track ( track_id );

CREATE VIEW albums AS
    SELECT a.id, a.title, a.title_lower, a.artist_id, ar.name
        FROM album AS a JOIN artist AS ar on a.artist_id = ar.ID;

CREATE VIEW invoices AS
    SELECT i.id, i.invoice_date, i.customer_id, CONCAT(c.last_name, ' ', c.first_name) AS name,
           i.address, i.city, i.state, i.country, i.post_code, i.total
        FROM invoice AS i JOIN customer c on c.ID = i.customer_id;
