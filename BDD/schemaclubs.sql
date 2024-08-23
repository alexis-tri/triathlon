DROP TABLE IF EXISTS clubs;

CREATE TABLE clubs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clubname TEXT NOT NULL,
    adresse TEXT NOT NULL,
    coursesclub TEXT
);
