DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    prenom TEXT NOT NULL,
    club TEXT NOT NULL,
    sexe TEXT,
    courses TEXT,
    vma TEXT,
    pma TEXT,
    ftp TEXT,
    fcmax TEXT,
    is_admin INTEGER DEFAULT 0
); 
 
