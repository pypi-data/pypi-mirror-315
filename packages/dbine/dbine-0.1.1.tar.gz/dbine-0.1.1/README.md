# dbine
Auxiliary tools related to databases

## Supported database types
- PostgreSQL
- MySQL

## Versions

|Version|Summary|
|:--|:--|
|0.1.1|Release dbine|

## Installation
### dbine
`pip install dbine`

### [Dependency of graspgraph](https://github.com/mskz-3110/graspgraph)

## Image
### MySQL
```sql
DROP DATABASE IF EXISTS dbine;
CREATE DATABASE dbine;

DROP USER IF EXISTS reader;
CREATE USER reader IDENTIFIED BY 'READER';

GRANT ALL ON dbine.* TO reader;

DROP TABLE IF EXISTS no_comments;
CREATE TABLE no_comments (
  id INT PRIMARY KEY,
  name VARCHAR(10)
) COMMENT 'コメントなしテーブル';

DROP TABLE IF EXISTS with_comments;
CREATE TABLE with_comments (
  id INT PRIMARY KEY COMMENT 'ID',
  name VARCHAR(10) COMMENT '名前'
) COMMENT 'コメントつきテーブル';

DROP TABLE IF EXISTS relations;
CREATE TABLE relations (
  id INT PRIMARY KEY COMMENT 'ID',
  no_comment_id INT COMMENT 'コメントなしテーブルのID',
  with_comment_id INT COMMENT 'コメントつきテーブルのID'
);
```

### PNG
![](./images/database_mysql.png)

## CLI
### pdf write
Write database table definition to PDF

`dbine pdf write database.yaml database.pdf`

#### [database.yaml]
```yaml
Type: PostgreSQL
DatabaseName: database
UserName: user
Password: password
Host: localhost
Port: ''
```

### pdf convert
Convert PDF to image

`dbine pdf convert database.pdf database.png`
