Create database bcrypt_user_schema;
Use bcrypt_user_schema;

Create table users (
	id int primary key auto_increment,
    firstname varchar(45),
    lastname varchar(45),
    birthday date,
    gender varchar(100),
    email varchar(100),
    password text,
    created_at datetime,
    updated_at datetime
);