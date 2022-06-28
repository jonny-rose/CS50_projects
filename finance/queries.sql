CREATE TABLE stocks(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    person_id INTEGER NOT NULL,
    symbol TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    shares INTEGER NOT NULL,
    price NUMERIC NOT NULL,
    total_amount NUMERIC NOT NULL,
    FOREIGN KEY (person_id) REFERENCES users(id)
);


CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    person_id INTEGER NOT NULL,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    shares INTEGER NOT NULL,
    price NUMERIC NOT NULL,
    date TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    FOREIGN KEY (person_id) REFERENCES users(id)
);