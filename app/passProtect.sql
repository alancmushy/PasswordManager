CREATE TABLE IF NOT EXISTS users(
   user_id SERIAL PRIMARY KEY, 
   userName TEXT NOT NULL UNIQUE, 
   pass_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS usersPasswords(
   pass_id SERIAL PRIMARY KEY,
   masterUsername TEXT NOT NULL,
   passwordUsername TEXT NOT NULL, --username connected to password
   passwordWebsite TEXT NOT NULL, --the website associated with the password being stored in the database
   passwordData BYTEA, -- encrypted data that is stored in the database 
   wrappedKey BYTEA --wrapped key
);

