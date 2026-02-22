CREATE TABLE IF NOT EXISTS users (
    user_id serial PRIMARY KEY,
    email text NOT NULL UNIQUE,
    display_name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS user_prefs (
    user_id int PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE, -- PRIMARY KEY + FOREIGN KEY -> USER
    prefs jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS comment (
    comment_id serial PRIMARY KEY,
    user_id int NOT NULL REFERENCES users(user_id) ON DELETE CASCADE, -- FOREIGN KEY -> USER
    text text NOT NULL,
    geom geometry(Point,4326) NOT NULL, -- LAT/LON POINT
    created_at timestamptz NOT NULL DEFAULT now()
);



-- SPATIAL INDEX FOR SPATIAL QUERIES
CREATE INDEX IF NOT EXISTS idx_comment_geom_gist ON comment USING GIST (geom);



-- EXAMPLE USER 1
INSERT INTO users (email, display_name)
VALUES
    ('1@example.test', 'Sarah_B')
ON CONFLICT (user_id) DO NOTHING;

-- PREFS FOR USER 1
INSERT INTO user_prefs (user_id, prefs)
VALUES
    (1, '{"TODO":"todo"}'::jsonb)
ON CONFLICT (user_id) DO NOTHING;



-- EXAMPLE USER 2
INSERT INTO users (email, display_name)
VALUES
    ('2@example.test', 'Thomas_K')
ON CONFLICT (user_id) DO NOTHING;

-- PREFS FOR USER 2
INSERT INTO user_prefs (user_id, prefs)
VALUES
    (2, '{"TODO":"todo"}'::jsonb)
ON CONFLICT (user_id) DO NOTHING;



-- EXAMPLE USER 3
INSERT INTO users (email, display_name)
VALUES
    ('3@example.test', 'Anna_M')
ON CONFLICT (user_id) DO NOTHING;

-- PREFS FOR USER 3
INSERT INTO user_prefs (user_id, prefs)
VALUES
    (3, '{"TODO":"todo"}'::jsonb)
ON CONFLICT (user_id) DO NOTHING;



-- EXAMPLE COMMENTS
INSERT INTO comment (user_id, text, geom)
VALUES
    (1, 'Rampe ist zu steil, schwer zu erklimmen.', ST_SetSRID(ST_MakePoint(10.021971, 53.556073), 4326)),
    (1, 'Ich bin hier hingefallen', ST_SetSRID(ST_MakePoint(10.022068, 53.556458), 4326)),
    (2, 'Der Besitzer hat mich komisch angestarrt', ST_SetSRID(ST_MakePoint(10.021971, 53.556073), 4326)),
    (2, 'Bei Regen sehr glatt :(', ST_SetSRID(ST_MakePoint(10.020262, 53.555697), 4326)),
    (2, 'Hervorragende Zugänglichkeit und hilfreiche Mitarbeiter!', ST_SetSRID(ST_MakePoint(10.022068, 53.556458), 4326)),
    (3, 'Kostenlose Parkplätze für Menschen mit Behinderung', ST_SetSRID(ST_MakePoint(10.020262, 53.555697), 4326)),
    (3, 'Aufzug funktioniert, sehr sauber', ST_SetSRID(ST_MakePoint(10.021500, 53.556700), 4326))
ON CONFLICT (comment_id) DO NOTHING;
