DROP TABLE IF EXISTS neighbours;
CREATE TABLE neighbours (
    ip char(55) PRIMARY KEY,
    port char(5) NOT NULL
);

DROP TABLE IF EXISTS files;
CREATE TABLE files (
    file_md5 char(32) PRIMARY KEY,
    file_name char(100) NOT NULL,
    dim integer DEFAULT 0
);

DROP TABLE IF EXISTS packets;
CREATE TABLE packets (
    pktid_id char(16) PRIMARY KEY,
    ip char(55) NOT NULL
);