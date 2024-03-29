CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    name TEXT
);

CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories,
    user_id INTEGER REFERENCES users,
    name TEXT
);

CREATE TABLE entries (
    id SERIAL PRIMARY KEY,
    activity_id INTEGER REFERENCES activities,
    start TIMESTAMP,
    stop TIMESTAMP
);
