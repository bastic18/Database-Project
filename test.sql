




-- -- LOAD DATA INFILE'signup_new.csv' INTO TABLE signup FIELDS TERMINATED BY ',' ENCLOSED BY '' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
-- -- LOAD DATA INFILE'user.csv' INTO TABLE User FIELDS TERMINATED BY ',' ENCLOSED BY '' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
-- -- LOAD DATA INFILE'friend.csv' INTO TABLE Friends FIELDS TERMINATED BY ',' ENCLOSED BY '' LINES TERMINATED BY '\n' IGNORE 1 ROWS;




-- -- /* clean up old tables;
-- --    must drop tables with foreign keys first
-- --    due to referential integrity constraints
-- --  */


-- drop database testpy3;
-- create database testpy3;
--      use testpy3;
-- drop table IF EXISTS signup;
-- drop table IF EXISTS User;
-- drop table IF EXISTS Friends;
-- drop table IF EXISTS createuser;
-- drop table IF EXISTS UserProfile;
-- drop table IF EXISTS Photos;
-- drop table IF EXISTS manage_photo;
-- drop table IF EXISTS Posts;
-- drop table IF EXISTS Create_Post;
-- drop table IF EXISTS Groups;
-- drop table IF EXISTS Comment;

-- drop table IF EXISTS Create_Group;
--  drop table IF EXISTS join_group;


-- DROP TRIGGER IF EXISTS new_user_trigger;
-- DROP TRIGGER IF EXISTS new_post_trigger;
-- DROP TRIGGER IF EXISTS new_photo_trigger;

-- DROP TRIGGER IF EXISTS update_user_trigger;



-- DROP PROCEDURE IF EXISTS GETPOST_BY_USERNAME;
-- DROP PROCEDURE IF EXISTS GETPOST_BY_ID;
-- DROP PROCEDURE IF EXISTS DELETEPOST_BY_ID;
-- DROP PROCEDURE IF EXISTS GETPROFILE_PICTURE_BY_USERNAME;
-- DROP PROCEDURE IF EXISTS INSERT_INTO_PHOTOS;
-- DROP PROCEDURE IF EXISTS INSERT_INTO_FRIENDS;
-- DROP PROCEDURE IF EXISTS UPDATE_POSTS;
-- DROP PROCEDURE IF EXISTS GETFRIENDS_BY_USERNAME;
-- DROP PROCEDURE IF EXISTS GETFRIENDS_INFO_BY_USERNAME;
-- DROP PROCEDURE IF EXISTS GETCOMMENT_BY_ID;
-- DROP PROCEDURE IF EXISTS MAKECOMMENT;
-- DROP PROCEDURE IF EXISTS GETUSER_ADMIN_BY_USERNAME;
-- DROP PROCEDURE IF EXISTS GETFRIEND_ADMIN_BY_USERNAME;
-- DROP PROCEDURE IF EXISTS GETPOST_ADMIN_BY_USERNAME;
-- DROP PROCEDURE IF EXISTS GETCOMMENT_ADMIN_BY_USERNAME;
-- DROP PROCEDURE IF EXISTS Changeinfo;
-- DROP PROCEDURE IF EXISTS MAKEGROUP;
-- DROP PROCEDURE IF EXISTS GROUPCREATE;
-- DROP PROCEDURE IF EXISTS GETGROUP_BY_USERNAME;
DROP PROCEDURE IF EXISTS JOINGROUP;
DROP PROCEDURE IF EXISTS GETGROUP_INFO;
DROP PROCEDURE IF EXISTS GETGROUP_ADMIN_BY_USERNAME;


-- DELIMITER //
-- CREATE PROCEDURE Changeinfo(IN usernam varchar (50),IN fname varchar (50),
-- IN lname varchar (50),IN abt varchar (255),IN tele varchar (50), IN streetc varchar (50),
-- IN ct varchar (50), IN ctry varchar (50))
-- BEGIN
-- Update User set firstname=fname,lastname=lname,about=abt,telephone=tele,street=streetc,city=ct,country=ctry where username=usernam;
-- END//
-- DELIMITER ;


-- create table signup
--    (username 	varchar(50)	not null unique,
--     email		varchar(50)	not null unique,
--     password 		varchar(100)	not null,
 
--     primary key(username,email));


-- -- relationship


-- create table createuser
--    (username 	varchar(50)	not null, 
--     email		varchar(50)	not null,
--     date 		datetime	not null,
 
--     primary key(username,email),
--     foreign key(username) references signup(username) on update cascade on delete cascade,
-- 	foreign key(email) references signup(email) on update cascade on delete cascade);


-- create table User
--    (username 	varchar(50)	not null unique,
--     email		varchar(50)	not null unique,
--      firstname  varchar(50) not null,
-- 	lastname  varchar(50) not null,
--     about  varchar(255) not null,
--      telephone  varchar(15) not null,
--     street  varchar(100) not null,
-- 	city  varchar(100) not null,
-- 	country  varchar(100) not null,
--     primary key(username,email));



-- Delimiter $$
-- CREATE TRIGGER new_user_trigger
-- AFTER insert ON signup
-- FOR EACH ROW
-- BEGIN
-- insert into createuser(username,email,date) values(new.username,new.email,UTC_TIMESTAMP());
-- END $$
-- delimiter ;


-- -- relationship

-- create table Friends
--    (username 	varchar(50)	not null, 
--     friend_id		varchar(50)	not null,
--     friend_type 	varchar(20)		not null,
 
--     primary key(username,friend_id),
--     foreign key(username) references User(username) on update cascade on delete cascade);


-- DELIMITER //
-- CREATE PROCEDURE INSERT_INTO_FRIENDS(IN curr_username varchar(50), curr_friend varchar(50), curr_friend_type varchar(20))
-- BEGIN
-- INSERT INTO Friends (username,friend_id,friend_type) VALUES (curr_username,curr_friend,curr_friend_type);
-- END //
-- DELIMITER ;







-- DELIMITER //
-- CREATE PROCEDURE GETFRIENDS_BY_USERNAME(IN c_username varchar(50))
-- BEGIN
-- Select User.username,User.firstname,User.lastname,User.about,User.city, Friends.friend_id, Friends.friend_type from User join Friends on User.username=Friends.username where Friends.username=c_username; 
-- END //
-- DELIMITER ;








-- Create table Posts(
-- post_id  varchar(50)	not null unique,
-- title  varchar(50) not null,
-- content varchar(1000) not null,
-- post_description varchar(255) not null,
-- picture  varchar(50)	not null,
-- primary key(post_id));

-- -- relationship

-- create table Create_Post
--    (username 	varchar(50)	not null, 
--     post_id		varchar(50)	not null,
--     date 		datetime	not null,
 
--     primary key(username,post_id),
--     foreign key(username) references User(username) on update cascade on delete cascade,
-- 	foreign key(post_id) references Posts(post_id) on update cascade on delete cascade);








-- Create table Photos(


-- photo_id  varchar(50)	not null unique,
-- photo_name 	varchar(50)	not null ,
-- photo_description varchar(255) not null,
-- profile_picture boolean not null,

-- primary key(photo_id));

-- -- relationship for photos


-- create table manage_photo
--    (username 	varchar(50)	not null, 
--     photo_id		varchar(50)	not null,
--     date 		datetime	not null,
 
--     primary key(username,photo_id),
--     foreign key(username) references User(username) on update cascade on delete cascade,
-- 	foreign key(photo_id) references Photos(photo_id) on update cascade on delete cascade);



-- Create table Groups
-- (group_id varchar(50) not null unique,
-- group_name varchar(50) not null,
-- group_topic varchar(255) not null,
-- content_editors varchar(1000) not null,

-- primary key(group_id));

-- -- relationship for groups


-- create table Create_Group
--    (username 	varchar(50) not null, 
--     group_id		varchar(50) not null,
--     date 		datetime	not null,
 
--     primary key(username,group_id),
--     foreign key(username) references User(username) on update cascade on delete cascade,
-- 	foreign key(group_id) references Groups(group_id) on update cascade on delete cascade);


-- create table join_group
--    (username 	varchar(50) not null, 
--     group_id		varchar(50) not null,
--     date 		datetime	not null,
 
--     primary key(username,group_id),
--     foreign key(username) references User(username) on update cascade on delete cascade,
-- 	foreign key(group_id) references Groups(group_id) on update cascade on delete cascade);



-- create table Comment
--    (username 	varchar(50) not null, 
--     post_id		varchar(50) not null,
--     comment		varchar(255) not null unique	,
--     date datetime not null,
 
--     primary key(username,post_id,comment),
--     foreign key(username) references User(username) on update cascade on delete cascade,
--      foreign key(post_id) references Posts(post_id) on update cascade on delete cascade);


-- DELIMITER //
-- CREATE PROCEDURE GETCOMMENT_BY_ID(IN c_post_id varchar(50))
-- BEGIN
-- Select Posts.post_id,Posts.title,Posts.content,Posts.post_description,Posts.picture, Comment.username, Comment.comment, Comment.date from Posts join Comment on Posts.post_id=Comment.post_id where Posts.post_id=c_post_id ORDER BY UNIX_TIMESTAMP(date) DESC; 
-- END //
-- DELIMITER ;


-- DELIMITER //
-- CREATE PROCEDURE MAKECOMMENT(IN c_username varchar(50),c_post_id varchar(50), c_comment varchar(1000), c_date datetime)
-- BEGIN
-- INSERT INTO Comment(username,post_id,comment,date) VALUES(c_username,c_post_id,c_comment,c_date); 
-- END //
-- DELIMITER ;

-- DELIMITER //
-- CREATE PROCEDURE GROUPCREATE(IN c_username varchar(50),c_group_id varchar(50),  c_date datetime)
-- BEGIN
-- INSERT INTO Create_Group(username,group_id,date) VALUES(c_username,c_group_id,c_date); 
-- END //
-- DELIMITER ;

DELIMITER //
CREATE PROCEDURE JOINGROUP(IN c_username varchar(50),c_group_id varchar(50),  c_date datetime)
BEGIN
INSERT INTO join_group(username,group_id,date) VALUES(c_username,c_group_id,c_date); 
END //
DELIMITER ;



-- DELIMITER //
-- CREATE PROCEDURE MAKEGROUP(IN c_group_id varchar(50),c_name varchar(50), c_topic varchar(255), c_editor varchar(1000))
-- BEGIN
-- INSERT INTO Groups(group_id,group_name,group_topic,content_editors) VALUES(c_group_id,c_name,c_topic,c_editor); 
-- END //
-- DELIMITER ;





-- DELIMITER //
-- CREATE PROCEDURE GETGROUP_BY_USERNAME(IN c_username varchar(50))
-- BEGIN
-- Select Groups.group_id,Groups.group_name,Groups.group_topic,Groups.content_editors, Create_Group.username, Create_Group.date from Groups join Create_Group on Groups.group_id=Create_Group.group_id where Create_Group.username=c_username ORDER BY UNIX_TIMESTAMP(date) DESC; 
-- END //
-- DELIMITER ;





-- DELIMITER //
-- CREATE PROCEDURE GETFRIENDS_INFO_BY_USERNAME(IN c_username varchar(50))
-- BEGIN
-- Select* FROM User where username=c_username; 
-- END //
-- DELIMITER ;



-- DELIMITER //
-- CREATE PROCEDURE GETPOST_BY_USERNAME(IN c_username varchar(50))
-- BEGIN
-- Select Posts.post_id,Posts.title,Posts.content,Posts.post_description,Posts.picture, Create_Post.username, Create_Post.date from Posts join Create_Post on Posts.post_id=Create_Post.post_id where Create_Post.username=c_username ORDER BY UNIX_TIMESTAMP(date) DESC; 
-- END //
-- DELIMITER ;


-- DELIMITER //
-- CREATE PROCEDURE GETPOST_BY_ID(IN c_post_id varchar(50))
-- BEGIN
-- Select Posts.post_id,Posts.title,Posts.content,Posts.post_description,Posts.picture, Create_Post.username, Create_Post.date from Posts join Create_Post on Posts.post_id=Create_Post.post_id where Posts.post_id=c_post_id; 
-- END //
-- DELIMITER ;



-- DELIMITER //
-- CREATE PROCEDURE DELETEPOST_BY_ID(IN c_post_id varchar(50))
-- BEGIN


-- Delete from Posts where post_id=c_post_id;
-- Delete from Create_Post where post_id=c_post_id;
 
-- END //
-- DELIMITER ;




-- DELIMITER //
-- CREATE PROCEDURE GETPROFILE_PICTURE_BY_USERNAME(IN c_username varchar(50))
-- BEGIN
-- Select Photos.photo_id,Photos.profile_picture, manage_photo.username, manage_photo.date from Photos join manage_photo on Photos.photo_id=manage_photo.photo_id where manage_photo.username=c_username and Photos.profile_picture=1 ORDER BY UNIX_TIMESTAMP(date) DESC limit 1;
-- END //
-- DELIMITER ;





-- DELIMITER //
-- CREATE PROCEDURE INSERT_INTO_PHOTOS(IN pic_file varchar(50), photo_name varchar(50),pic_description varchar(255),profile_pic boolean )
-- BEGIN
-- INSERT INTO Photos (photo_id,photo_name,photo_description,profile_picture) VALUES (pic_file,photo_name,pic_description,profile_pic);
-- END //
-- DELIMITER ;


-- DELIMITER //
-- CREATE PROCEDURE UPDATE_POSTS(IN c_post_id varchar(50), c_title varchar(50),c_content varchar(1000),c_post_description varchar(255) )
-- BEGIN
-- UPDATE POSTS SET title=c_title, content=c_content, post_description=C_post_description where post_id=c_post_id;
-- END //
-- DELIMITER ;





-- ADMIN PROCEDURES 


-- DELIMITER //
-- CREATE PROCEDURE GETUSER_ADMIN_BY_USERNAME(IN c_username varchar(50))
-- BEGIN
-- Select* FROM User where username=c_username; 
-- END //
-- DELIMITER ;


-- DELIMITER //
-- CREATE PROCEDURE GETFRIEND_ADMIN_BY_USERNAME(IN c_username varchar(50))
-- BEGIN
-- Select Friends.username, Friends.friend_id, Friends.friend_type, User.firstname, User.lastname, User.about, User.telephone, User.street, User.country, User.city from Friends join User on Friends.friend_id=User.username where Friends.username=c_username; 
-- END //
-- DELIMITER ;

-- DELIMITER //
-- CREATE PROCEDURE GETPOST_ADMIN_BY_USERNAME(IN c_username varchar(50))
-- BEGIN
-- Select Posts.post_id, Posts.title, Posts.content,Posts.post_description, Posts.picture, Create_Post.username, Create_Post.post_id, Create_Post.date  FROM Posts JOIN Create_Post on Posts.post_id=Create_Post.post_id where Create_Post.username=c_username; 
-- END //
-- DELIMITER ;


-- DELIMITER //
-- CREATE PROCEDURE GETCOMMENT_ADMIN_BY_USERNAME(IN c_username varchar(50))
-- BEGIN
-- Select Posts.post_id, Posts.title, Posts.content,Posts.post_description, Posts.picture, Comment.username, Comment.post_id, Comment.comment ,Comment.date, Create_Post.username as creator,Create_Post.date as creation, Create_Post.post_id  FROM Posts JOIN Comment on Posts.post_id=Comment.post_id  join Create_Post on Posts.post_id=Create_Post.post_id where Comment.username=c_username ORDER BY UNIX_TIMESTAMP(Comment.date) DESC; 
-- END //
-- DELIMITER ;




-- Create table Groups
-- (group_id varchar(50) not null unique,
-- group_name varchar(50) not null,
-- group_topic varchar(255) not null,
-- content_editors varchar(1000) not null,

-- primary key(group_id));

-- -- relationship for groups


-- create table Create_Group
--    (username 	varchar(50) not null, 
--     group_id		varchar(50) not null,
--     date 		datetime	not null,
 
--     primary key(username,group_id),
--     foreign key(username) references User(username) on update cascade on delete cascade,
-- 	foreign key(group_id) references Groups(group_id) on update cascade on delete cascade);







DELIMITER //
CREATE PROCEDURE GETGROUP_ADMIN_BY_USERNAME(IN c_username varchar(50))
BEGIN
Select Groups.group_id, Groups.group_name, Groups.group_topic,   Groups.content_editors,  Create_Group.username, Create_Group.date FROM Groups JOIN Create_Group on Groups.group_id=Create_Group.group_id where Create_Group.username=c_username ORDER BY UNIX_TIMESTAMP(Create_Group.date) DESC; 
END //
DELIMITER ;




DELIMITER //
CREATE PROCEDURE GETGROUP_INFO(IN c_username varchar(50))
BEGIN
Select Groups.group_id, Groups.group_name, Groups.group_topic, Groups.content_editors, 
join_group.username as user, join_group.date as joindate, Create_Group.username as creator, 
Create_Group.date as createdate FROM Groups JOIN join_group on Groups.group_id=join_group.group_id join 
Create_Group on Groups.group_id=Create_Group.group_id where join_group.username=c_username ORDER BY UNIX_TIMESTAMP(join_group.date) DESC; 
END //
DELIMITER ;











