BEGIN TRANSACTION;
PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS "TableImg";
CREATE TABLE IF NOT EXISTS "TableImg" (
	"TIID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"url"	TEXT,
	"id"	integer,
	"name"	TEXT,
	"src"	TEXT,
	"text"	TEXT,
	"altText"	TEXT,
	"width"	integer,
	"height"	integer,
	"x"	integer,
	"y"	integer,
	"displayed"	TEXT,
	"download"	BLOB,
	"image"	BLOB
);
DROP TABLE IF EXISTS "TableUrl";
CREATE TABLE IF NOT EXISTS "TableUrl" (
	"TUID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"url"	TEXT NOT NULL,
	"screenShot"	BLOB
);
DROP TABLE IF EXISTS "ElementTableRef";
CREATE TABLE IF NOT EXISTS "ElementTableRef" (
	"ETRID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"SSID"	INTEGER,
	"UrlTable"	TEXT UNIQUE,
	"ImgTable"	TEXT UNIQUE,
	"BtnTable"	TEXT UNIQUE,
	FOREIGN KEY("SSID") REFERENCES "ScrapSetting"("SSID")
);
DROP TABLE IF EXISTS "ScrapSetting";
CREATE TABLE IF NOT EXISTS "ScrapSetting" (
	"SSID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"EMID"	INTEGER,
	"HASHKEY"	TEXT,
	"driver"	TEXT NOT NULL,
	"targetPlatform"	TEXT NOT NULL,
	"navDepth"	INTEGER,
	"date"	datetime,
	FOREIGN KEY("EMID") REFERENCES "Entry"("EMID")
);
DROP TABLE IF EXISTS "Entry";
CREATE TABLE IF NOT EXISTS "Entry" (
	"EMID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"url"	TEXT NOT NULL UNIQUE,
	"status"	TEXT NOT NULL,
	"description"	TEXT
);
COMMIT;