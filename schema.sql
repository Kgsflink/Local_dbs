DROP TABLE IF EXISTS uploads;
CREATE TABLE uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    path TEXT NOT NULL
);