DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS usersPasswords;

CREATE TABLE users(
   user_id integer primary key not null, 
   userName text not NULL, 
   pass_hash text not NULL,
   salt BLOB
);

CREATE TABLE usersPasswords(
   pass_id integer primary key not null,
   user text key not null,
   passwordWebsite text not NULL, --the website associated with the password being stored in the database
   passwordText text not NULL, --the actual password text value
   passwordKey text not NULL, --encrypted key to unlock encrypted plaintext password
   passwordUsername text not NULL --username connected to password
);