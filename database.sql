CREATE TABLE movies(
    id INT PRIMARY KEY,
    title VARCHAR(100),
    status VARCHAR(50),
    runtime INT,
    revenue BIGINT,
    release_date DATE,
    popularity DECIMAL,
    overview TEXT,
    original_title VARCHAR(100),
    original_language VARCHAR(50),
    budget BIGINT,
    adult BOOLEAN,
    vote_count INT,
    vote_average DECIMAL
);


CREATE TABLE reviews (
	id VARCHAR(50) PRIMARY KEY,
 	author VARCHAR(100),
 	content TEXT,
  	rating INT CHECK (rating >= 0 AND rating <= 10),
 	movieId INT NOT NULL,
  	FOREIGN KEY (movieId) REFERENCES movies(id) ON DELETE CASCADE
);

CREATE TABLE genres (
 	id INT PRIMARY KEY,
 	name VARCHAR(50) NOT NULL
);

CREATE TABLE movies_genres (
 	movieId INT NOT NULL,
 	genreId INT NOT NULL,
 	FOREIGN KEY (movieId) REFERENCES movies(id) ON DELETE CASCADE,
 	FOREIGN KEY (genreId) REFERENCES genres(id) ON DELETE CASCADE,
 	PRIMARY KEY (movieId, genreId)
);

CREATE TABLE companies (
 	id INT PRIMARY KEY,
 	name VARCHAR(100),
 	homepage VARCHAR(100),
 	origin_country VARCHAR(50),
 	headquarters VARCHAR(100)
);

CREATE TABLE movies_companies (
 	movieId INT NOT NULL,
 	companyId INT NOT NULL,
 	FOREIGN KEY (movieId) REFERENCES movies(id) ON DELETE CASCADE,
 	FOREIGN KEY (companyId) REFERENCES companies(id) ON DELETE CASCADE,
 	PRIMARY KEY (movieId, companyId)
);

CREATE TABLE people (
	id INT PRIMARY KEY,
 	name VARCHAR(100),
  	gender INT CHECK(gender >=0 AND gender <= 3) DEFAULT 0,
  	popularity DECIMAL
);


CREATE TABLE tcast (
	id VARCHAR(50) PRIMARY KEY,
  	character VARCHAR(100),
	department VARCHAR(100),
	personId INT NOT NULL,
	movieId INT NOT NULL,
  	FOREIGN KEY (personId) REFERENCES people(id) ON DELETE CASCADE,
	FOREIGN KEY (movieId) REFERENCES movies(id) ON DELETE CASCADE
);


CREATE TABLE crew (
	id VARCHAR(50) PRIMARY KEY,
 	job VARCHAR(100),
	department VARCHAR(100),
	personId INT NOT NULL,
	movieId INT NOT NULL,
  	FOREIGN KEY (personId) REFERENCES people(id) ON DELETE CASCADE,
	FOREIGN KEY (movieId) REFERENCES movies(id) ON DELETE CASCADE
);