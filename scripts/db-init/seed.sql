CREATE TABLE IF NOT EXISTS user (
  user_id serial PRIMARY KEY DEFAULT,
  email text NOT NULL UNIQUE,
  display_name text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS user_prefs (
  user_id int PRIMARY KEY REFERENCES user(user_id) ON DELETE CASCADE, -- PRIMARY KEY + FOREIGN KEY -> USER
  prefs jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS comment (
  comment_id serial PRIMARY KEY,
  user_id int NOT NULL REFERENCES user(user_id) ON DELETE CASCADE, -- FOREIGN KEY -> USER
  text text NOT NULL,
  geom geometry(Point,4326), -- LAT/LON POINT
  created_at timestamptz NOT NULL DEFAULT now()
);



-- SPATIAL INDEX FOR SPATIAL QUERIES
CREATE INDEX IF NOT EXISTS idx_comment_geom_gist ON comment USING GIST (geom);



-- EXAMPLE USER 1
INSERT INTO user (email, display_name)
VALUES
  ('1@example.test', 'ExampleUser1')
ON CONFLICT (user_id) DO NOTHING;

-- PREFS FOR USER 1
INSERT INTO user_prefs (user_id, prefs)
VALUES
  (1, '{"TODO":"todo"}'::jsonb)
ON CONFLICT (user_id) DO NOTHING;



-- EXAMPLE USER 2
INSERT INTO user (user_id, email, display_name)
VALUES
  ('2@example.test', 'ExampleUser2')
ON CONFLICT (user_id) DO NOTHING;

-- PREFS FOR USER 2
INSERT INTO user_prefs (user_id, prefs)
VALUES
  (2, '{"TODO":"todo"}'::jsonb)
ON CONFLICT (user_id) DO NOTHING;



-- EXAMPLE COMMENTS
INSERT INTO comment (comment_id, user_id, text, geom)
VALUES
  (1, 1, 'Example comment from 1', ST_SetSRID(ST_MakePoint(53.556458, 10.022068), 4326)),
  (2, 2, 'Example comment 1 from 2', ST_SetSRID(ST_MakePoint(53.556073, 10.021971), 4326)),
  (3, 2, 'Example comment 2 from 2', ST_SetSRID(ST_MakePoint(53.555697, 10.020262), 4326))
ON CONFLICT (comment_id) DO NOTHING;
