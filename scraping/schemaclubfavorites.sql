DROP TABLE IF EXISTS club_favorites;

CREATE TABLE club_favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    club_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    FOREIGN KEY(club_id) REFERENCES clubs(id),
    FOREIGN KEY(course_id) REFERENCES courses(id)
);