DROP TABLE IF EXISTS courses;


CREATE TABLE courses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  place TEXT,
  date TEXT,
  distance TEXT
  );