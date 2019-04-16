DROP DATABASE IF EXISTS db;
CREATE DATABASE db;
USE db;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS video;
CREATE TABLE users(
	UserID INTEGER NOT NULL AUTO_INCREMENT,
	Username VARCHAR(30) NOT NULL,
	EncryptedPass VARCHAR(128) NOT NULL,
	TotalVideoCount INTEGER,
	DateCreated DATE,
	Email VARCHAR(50),
	CONSTRAINT users_pk PRIMARY KEY(UserID)
);

CREATE TABLE video(
	VideoID INTEGER NOT NULL AUTO_INCREMENT,
	UserID INTEGER NOT NULL,
	VideoUser VARCHAR(30) NOT NULL,
	VideoTitle VARCHAR(100),
	VideoURL VARCHAR(2000),
	DateUploaded DATE,
	CONSTRAINT Video_pk PRIMARY KEY(VideoID),
	CONSTRAINT Video_fk FOREIGN KEY (UserID) 
		REFERENCES users(UserID)
			ON DELETE CASCADE
			ON UPDATE CASCADE
);
