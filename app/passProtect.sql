CREATE TABLE IF NOT EXISTS users(
   user_id integer primary key not null, 
   userName text not NULL, 
   pass_hash text not NULL
);

CREATE TABLE IF NOT EXISTS usersPasswords(
   pass_id integer primary key not null,
   user text key not null,
   passwordUsername text not NULL, --username connected to password
   passwordWebsite text not NULL, --the website associated with the password being stored in the database
   passwordData BLOB, -- encrypted data that is stored in the database 
   wrappedKey BLOB --wrapped key
);

