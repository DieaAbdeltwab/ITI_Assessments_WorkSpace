-- Create anime table
CREATE TABLE IF NOT EXISTS anime (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    episodes INTEGER,
    rating REAL,
    release_year INTEGER,
    image TEXT
);

-- Insert sample anime data
INSERT INTO anime (title, genre, episodes, rating, release_year, image) VALUES
('Attack on Titan', 'Action', 79, 9.0, 2013, 'attack_on_titan.jpg'),
('One Piece', 'Adventure', 1000, 8.8, 1999, 'one_piece.jpg'),
('Fullmetal Alchemist: Brotherhood', 'Action', 64, 9.2, 2009, 'fullmetal_alchemist.jpg'),
('Death Note', 'Mystery', 37, 8.9, 2006, 'death_note.jpg'),
('Demon Slayer', 'Action', 26, 9.1, 2019, 'demon_slayer.jpg'),
('Steins;Gate', 'Sci-Fi', 24, 9.1, 2011, 'steins_gate.jpg'),
('Your Lie in April', 'Drama', 22, 9.0, 2014, 'your_lie_in_april.jpg'),
('Hunter x Hunter', 'Adventure', 148, 9.0, 2011, 'hunter_x_hunter.jpg'),
('Tokyo Ghoul', 'Horror', 12, 8.8, 2014, 'tokyo_ghoul.jpg'),
('Kaguya-sama: Love is War', 'Romance', 24, 8.9, 2019, 'kaguya-sama.jpg'),
('Mob Psycho 100', 'Action', 26, 8.8, 2016, 'mob_psycho_100.jpg'),
('One Punch Man', 'Comedy', 12, 9.0, 2015, 'one_punch_man.jpg'),
('Made in Abyss', 'Action', 13, 9.2, 2017, 'made_in_abyss.jpg'),
('Vinland Saga', 'Action', 24, 8.9, 2019, 'vinland_saga.jpg'),
('Black Clover', 'Action', 170, 8.2, 2017, 'black_clover.jpg'),
('Darling in the Franxx', 'Action', 24, 8.8, 2018, 'darling_in_the_franxx.jpg'),
('Kakegurui', 'Action', 12, 8.7, 2017, 'kakegurui.jpg'),
('Soul Eater', 'Action', 51, 8.5, 2008, 'soul_eater.jpg'),
('Black Bullet', 'Action', 12, 8.4, 2014, 'black_bullet.jpg'),
('Gintama', 'Comedy', 366, 8.9, 2006, 'gintama.jpg'),
('Noragami', 'Action', 12, 8.7, 2014, 'noragami.jpg'),
('Demon Slayer: Swordsmith Village Arc', 'Action', 1, 9.2, 2023, 'demon_slayer_swordsmith.jpg');

-- Create best series table
CREATE TABLE IF NOT EXISTS best_series (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,  -- anime or series
    genre TEXT NOT NULL,
    episodes INTEGER,
    rating REAL,
    release_year INTEGER,
    image TEXT,
    description TEXT
);

-- Insert best series data
INSERT INTO best_series (title, type, genre, episodes, rating, release_year, image, description) VALUES
('Breaking Bad', 'series', 'Crime', 62, 9.5, 2008, 'breaking_bad.jpg', 'A high school chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine to secure his family''s future.'),
('Game of Thrones', 'series', 'Drama', 73, 9.2, 2011, 'game_of_thrones.jpg', 'Nine noble families fight for control over the mythical lands of Westeros, while an ancient enemy returns after being dormant for millennia.'),
('The Sopranos', 'series', 'Crime', 86, 9.2, 1999, 'the_sopranos.jpg', 'New Jersey mob boss Tony Soprano deals with personal and professional issues in his home and business life.'),
('The Wire', 'series', 'Crime', 60, 9.3, 2002, 'the_wire.jpg', 'The Baltimore drug trade from the perspectives of police, drug dealers, and city officials.'),
('The Twilight Zone', 'series', 'Sci-Fi', 156, 9.1, 1959, 'twilight_zone.jpg', 'A weekly anthology series exploring provocative storylines of fantasy, mystery, suspense, and horror.'),
('The Office (US)', 'series', 'Comedy', 201, 9.3, 2005, 'the_office.jpg', 'A mockumentary on a group of typical office workers, where the workday consists of ego clashes, inappropriate behavior, and tedium.'),
('The Crown', 'series', 'Drama', 40, 9.2, 2016, 'the_crown.jpg', 'A look at the reign of Queen Elizabeth II from the 1940s to modern times.'),
('The Marvelous Mrs. Maisel', 'series', 'Comedy', 42, 9.1, 2017, 'mrs_maisel.jpg', 'A 1950s housewife starts a career as a stand-up comedian in New York City.'),
('Stranger Things', 'series', 'Sci-Fi', 34, 9.1, 2016, 'stranger_things.jpg', 'When a young boy vanishes, his mother, a police chief, and his friends must confront terrifying supernatural forces and a sinister experiment.'),
('The Mandalorian', 'series', 'Sci-Fi', 22, 9.0, 2019, 'the_mandalorian.jpg', 'The travels of a lone bounty hunter in the outer reaches of the galaxy, far from the authority of the New Republic.');

-- Create movies table
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    genre TEXT NOT NULL,
    rating REAL,
    release_year INTEGER,
    image TEXT,
    runtime INTEGER
);

-- Insert sample movies data
INSERT INTO movies (title, genre, rating, release_year, image, runtime) VALUES
('The Shawshank Redemption', 'Drama', 9.3, 1994, 'shawshank_redemption.jpg', 142),
('The Godfather', 'Crime', 9.2, 1972, 'godfather.jpg', 175),
('The Godfather: Part II', 'Crime', 9.0, 1974, 'godfather_ii.jpg', 202),
('The Dark Knight', 'Action', 9.0, 2008, 'dark_knight.jpg', 152),
('12 Angry Men', 'Drama', 9.0, 1957, '12_angry_men.jpg', 96),
('Schindler''s List', 'Drama', 8.9, 1993, 'schindlers_list.jpg', 195),
('The Lord of the Rings: Return of the King', 'Adventure', 8.9, 2003, 'lotr_return.jpg', 201),
('Pulp Fiction', 'Crime', 8.9, 1994, 'pulp_fiction.jpg', 154),
('The Good, the Bad and the Ugly', 'Western', 8.8, 1966, 'good_bad_ugly.jpg', 178),
('Fight Club', 'Drama', 8.8, 1999, 'fight_club.jpg', 139),
('Forrest Gump', 'Drama', 8.8, 1994, 'forrest_gump.jpg', 142),
('Inception', 'Sci-Fi', 8.8, 2010, 'inception.jpg', 148),
('The Lord of the Rings: Fellowship of the Ring', 'Adventure', 8.8, 2001, 'lotr_fellowship.jpg', 178),
('Star Wars: Episode V - The Empire Strikes Back', 'Sci-Fi', 8.8, 1980, 'empire_strikes_back.jpg', 124),
('The Lord of the Rings: The Two Towers', 'Adventure', 8.8, 2002, 'lotr_towers.jpg', 179),
('Interstellar', 'Sci-Fi', 8.7, 2014, 'interstellar.jpg', 169),
('The Matrix', 'Sci-Fi', 8.7, 1999, 'matrix.jpg', 136),
('Goodfellas', 'Crime', 8.7, 1990, 'goodfellas.jpg', 146),
('Seven Samurai', 'Adventure', 8.7, 1954, 'seven_samurai.jpg', 207),
('One Flew Over the Cuckoo''s Nest', 'Drama', 8.7, 1975, 'cuckoos_nest.jpg', 133);


