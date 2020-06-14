from flask_wtf import FlaskForm
from flask import Flask, session,request
from flask_wtf import validators
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField 
from wtforms.validators import DataRequired, Length, Email,EqualTo, ValidationError
from flask_mysqldb import MySQL,MySQLdb
import MySQLdb.cursors
from flask_wtf.file import FileField, FileAllowed


app = Flask(__name__)
app.config['SECRET_KEY']='c07639e9610bfe52a8d3e0e6ac297368c521'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testpy3'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Intialize MySQL
mysql = MySQL(app)




class SignupForm(FlaskForm):
    username= StringField('Username', validators=[DataRequired(), Length(min=8, max= 50)])
    email= StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])

    submit= SubmitField('Sign Up')

    def validate_email(self,email):
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM signup WHERE email=%s",(email.data,))
        data = curl.fetchone()
        #print(data)
        curl.close()
        if data:
            raise ValidationError('This email is already taken !!!')
    def validate_username(self,username):
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM signup WHERE username=%s",(username.data,))
        data = curl.fetchone()
        #print(data['username'])
        curl.close()
        if data:
            raise ValidationError('This username is already taken !!!')


class LoginForm(FlaskForm):
   
    email= StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember= BooleanField('Remember Me')
    submit= SubmitField('Login')

class UserForm(FlaskForm):
   
    firstname= StringField('Firstname', validators=[DataRequired(), Length(min=2, max= 50)])
    lastname= StringField('Lastname', validators=[DataRequired(), Length(min=2, max= 50)])
    about= StringField('About', validators=[DataRequired(), Length(min=5, max= 255)])
    telephone= StringField('Telephone', validators=[DataRequired(), Length(min=10, max= 15)])
    city= StringField('City', validators=[DataRequired(), Length(min=3, max= 50)])
    country= StringField('Country', validators=[DataRequired(), Length(min=2, max= 50)])
    street= StringField('Street', validators=[DataRequired(), Length(min=5, max= 50)])
    submit= SubmitField('Create User')



class UpdateUserForm(FlaskForm):

    username= StringField('Username', validators=[DataRequired(), Length(min=8, max= 50)])
    email= StringField('Email', validators=[DataRequired(), Email()])
    firstname= StringField('Firstname', validators=[DataRequired(), Length(min=2, max= 50)])
    lastname= StringField('Lastname', validators=[DataRequired(), Length(min=2, max= 50)])
    about= StringField('About', validators=[DataRequired(), Length(min=5, max= 255)])
    telephone= StringField('Telephone', validators=[DataRequired(), Length(min=10, max= 15)])
    city= StringField('City', validators=[DataRequired(), Length(min=3, max= 50)])
    country= StringField('Country', validators=[DataRequired(), Length(min=2, max= 50)])
    street= StringField('Street', validators=[DataRequired(), Length(min=5, max= 50)])
    submit= SubmitField('Update User')

    

    def validate_username(self,username):
        if username.data != session['username']:
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute("SELECT * FROM User WHERE username=%s",(username.data,))
            data = curl.fetchone()
            print(data)
            print(username.data)
            curl.close()
            if data:
                
                raise ValidationError('This username already taken !!!')
       


    def validate_email(self,email):
        if email.data != session['email']:
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute("SELECT * FROM User WHERE email=%s",(email.data,))
            data = curl.fetchone()
            print(data)
            curl.close()
            if data:
                raise ValidationError('This email already taken !!!')
       

class PictureForm(FlaskForm):
    photo_name=StringField('Photo Name', validators=[DataRequired(), Length(min=4, max= 50)])
    description=StringField('Description', validators=[DataRequired(), Length(min=4, max= 255)])
    profile_pic=BooleanField('Set as profile picture')
    picture= FileField('Upload picture', validators=[FileAllowed(['jpg','png'])])
    submit= SubmitField('Upload')



class PostForm(FlaskForm):
   
    Title= StringField('Title', validators=[DataRequired(), Length(min=3, max= 100)])
    Content= TextAreaField('Content', validators=[DataRequired()])
    Description= StringField('Description')
    picture= FileField('Upload picture', validators=[FileAllowed(['jpg','png'])])
    submit= SubmitField('Post')

class FriendForm(FlaskForm):
   
    friend_username= StringField('Friend Username', validators=[DataRequired(), Length(min=3, max= 100)])
    friend_type= StringField('Friend Type', validators=[DataRequired(),Length(min=3, max= 20)])
    submit= SubmitField('Friend')

    def validate_friend_username(self,friend_username):
        if friend_username.data== session['username']:
            raise ValidationError('Cant be friends with yourself !!!')
        else:
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute("SELECT * FROM User WHERE username=%s",(friend_username.data,))
            data = curl.fetchone()
            curl.close()
            if data==None:
                raise ValidationError('This friend username does not exist in the database!!!')
        


class GroupForm(FlaskForm):

    group_id= StringField('Group ID', validators=[DataRequired(), Length(min=3, max= 50)])
    group_name= StringField('Group Name', validators=[DataRequired(), Length(min=5, max= 50)])
    group_topic= StringField('Group Topic', validators=[DataRequired(), Length(min=5, max= 100)])
    group_context_editor= StringField('Context Editors', validators=[DataRequired()])
    submit= SubmitField('Create Group')

    def validate_group_id(self,group_id):
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute("SELECT * FROM Groups WHERE group_id=%s",(group_id.data,))
            data = curl.fetchone()
            curl.close()
            if data:
                raise ValidationError('This group id already taken, choose another!!!')
        



class CommentForm(FlaskForm):
   
    Comment= TextAreaField('Comment',validators=[DataRequired(),Length(min=8, max= 1000)])
    submit= SubmitField('Comment')


class AdminForm(FlaskForm):
   
    search= StringField('Search User',validators=[DataRequired(),Length(min=5, max= 51)])
    submit= SubmitField('Search')

    def validate_search(self,search):
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM User WHERE username=%s",(search.data,))
        data = curl.fetchone()

        curl.close()
        if data==None:
            
            raise ValidationError('This username does not not exist !!!')



class JoinForm(FlaskForm):
       
    group_id= StringField('Group Name',validators=[DataRequired(),Length(min=1, max= 255)])
    submit= SubmitField('JOIN')

    def validate_group_id(self,group_id):
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM Groups WHERE group_id=%s",(group_id.data,))
        data = curl.fetchone()
        
        curl.close()
        if data==None:
            
            raise ValidationError('This Group ID does not not exist !!!')