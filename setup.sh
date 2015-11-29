# Create DB
sqlite3 santa.db "create table secret_santa (id INTEGER PRIMARY KEY, name TEXT, password TEXT, match INTEGER, FOREIGN KEY(match) REFERENCES secret_santa(id));"
