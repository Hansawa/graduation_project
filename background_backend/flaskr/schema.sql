DROP TABLE IF EXISTS admin;

CREATE TABLE admin (
    adminId INTEGER PRIMARY KEY AUTOINCREMENT,
    adminName TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

insert into admin (adminName, password)
values ('admin', '123456');