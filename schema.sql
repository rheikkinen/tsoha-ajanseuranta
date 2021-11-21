CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories,
    name TEXT,
    totaltime INTERVAL
);

CREATE TABLE entries (
    id SERIAL PRIMARY KEY,
    activity_id INTEGER REFERENCES activities,
    start TIMESTAMP,
    stop TIMESTAMP
);
