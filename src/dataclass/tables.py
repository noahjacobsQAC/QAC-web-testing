# -*- coding: utf-8 -*-

TableImb = "CREATE TABLE IF NOT EXISTS %s (\
	TIID	INTEGER PRIMARY KEY AUTOINCREMENT,\
	url	TEXT,\
	id	integer,\
	name	TEXT,\
	src	TEXT,\
	text	TEXT,\
	altText	TEXT,\
	width	integer,\
	height	integer,\
	x	integer,\
	y	integer,\
	displayed	TEXT,\
	download	TEXT,\
	image	BLOB\
);"

TableUrl = "CREATE TABLE IF NOT EXISTS %s (\
	TUID	INTEGER PRIMARY KEY AUTOINCREMENT,\
	url	TEXT NOT NULL,\
	screenShot	BLOB\
);"

siteElements = 'CREATE TABLE %s (\
	"elemID" INTEGER, \
	"type"	TEXT,\
	"url"	TEXT,\
	"xPath"	TEXT,\
	"nonText"	TEXT,\
	"decorative"	TEXT,\
	"class"	TEXT,\
	"name"	TEXT,\
	"id"	TEXT,\
	"alt"	TEXT,\
	"arialabel"	TEXT,\
	"src"	TEXT,\
	"errors"	TEXT\
);'
