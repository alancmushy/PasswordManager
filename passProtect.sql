DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS usersPasswords;

CREATE TABLE users(
   user_id integer primary key not null, 
   userName text not NULL, 
   pass_word text not NULL
);

CREATE TABLE usersPasswords(
   pass_id integer primary key not null,
   user text key not null,
   passwordWebsite text not NULL, --the website associated with the password being stored in the database
   passwordText text not NULL, --the actual password text value
   passwordUsername text not NULL --the user name of the user that the password is attached to
);