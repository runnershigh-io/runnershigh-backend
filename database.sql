CREATE TABLE roles (
  roles_id SERIAL PRIMARY KEY,
  name VARCHAR
);

INSERT INTO roles (name) VALUES ('admin');
INSERT INTO roles (name) VALUES ('user');

CREATE TABLE users (
  users_id SERIAL PRIMARY KEY,
  roles_id INTEGER REFERENCES roles(roles_id),
  username VARCHAR (100) UNIQUE,
  email VARCHAR UNIQUE,
  password VARCHAR,
  age INTEGER,
  location VARCHAR,
  authenticated BOOLEAN,
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE login (
  login_id SERIAL PRIMARY KEY,
  users_id INTEGER REFERENCES users(users_id) ON DELETE CASCADE,
  last_login_ip VARCHAR,
  last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE banned (
  banned_id SERIAL PRIMARY KEY,
  users_id INTEGER REFERENCES users(users_id),
  banned_by_users_id INTEGER REFERENCES users(users_id) ON DELETE CASCADE,
  reason VARCHAR (150),
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE blocked (
  blocked_id SERIAL PRIMARY KEY,
  users_id INTEGER REFERENCES users(users_id),
  blocked_users_id INTEGER REFERENCES users(users_id)
);

CREATE TABLE paths (
    paths_id SERIAL PRIMARY KEY,
    users_id INTEGER REFERENCES users(users_id),
    active BOOLEAN DEFAULT TRUE,
    geom GEOMETRY(POINT, 4326),
    created TIMESTAMP
);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO runnershigh_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO runnershigh_user;
