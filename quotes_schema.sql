-- 1. one table for author information (name, born , description)
CREATE TABLE author_info (
author_id INT Primary Key Not Null,
name VARCHAR NOT NULL,
born VARCHAR NOT NULL,
description VARCHAR NOT NULL);
--2.
CREATE TABLE quotes (quote_id INT Primary key NOT NULL,
quote_text VARCHAR NOT NULL,
author_id INT NOT NULL,
foreign key(author_id) references author_info(author_id));
--3. tags table to store unique tags
CREATE TABLE tags(
tag_id INT Primary Key not null,
tag_name varchar not null);
--4. one table to store quote and tag relation (quote_id , tag)
CREATE TABLE quote_tag_relation (
quote_id INT NOT NULL,
foreign key (quote_id) references quotes(quote_id),
tag_id Int NOT NULL,
foreign key (tag_id) references tags(tag_id));