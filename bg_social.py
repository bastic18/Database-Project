#set FLASK_APP=bg_social.py 
#set FLASK_DEBUG=1
#flask run
# dbproject/Scripts/activate.bat dbproject\Scripts\Activate.ps1
from flask import Flask, url_for,render_template, flash, redirect, session, request,abort
from forms import SignupForm,LoginForm,UserForm,UpdateUserForm, PictureForm,PostForm,FriendForm, GroupForm, CommentForm, AdminForm,JoinForm
from flask_mysqldb import MySQL,MySQLdb
from datetime import datetime
# from flask_login import LoginManager, login_required, login_user, current_user, logout_user
import MySQLdb.cursors
import re
import bcrypt
import os
import secrets
from PIL import Image
from operator import itemgetter


app = Flask(__name__)

app.config['SECRET_KEY']='c07639e9610bfe52a8d3e0e6ac297368c521'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'testpy3'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Intialize MySQL
mysql = MySQL(app)

# login_manager=LoginManager(app)
# login_manager.login_view='login'

images_folder = os.path.join('static', 'images')

app.config['UPLOAD_FOLDER'] = images_folder


@app.route('/')
@app.route('/home')
def home():
    dt=[]
    post_from_friends=[]
    combination=[]
    if session['username']:
        #print('sesssion',session['username'])
        cur = mysql.connection.cursor()
        cur.callproc("GETFRIENDS_BY_USERNAME",[session['username']])
        friends=cur.fetchall()
        print('friends',friends)
        cur.close()
        for i in friends:
            dt.append(i['friend_id'])
        #print('friend list of usernames:',dt)
        for r in dt:
            cur = mysql.connection.cursor()
            cur.callproc('GETPOST_BY_USERNAME',[r])
            all_friend_posts = cur.fetchall()
            post_from_friends.append(all_friend_posts)
            cur.close()
        #print('friends list of posts:', post_from_friends)
        for r in post_from_friends:
            for a in r:
                combination.append(a)
        #print('format friends list of posts:', combination)
        cur = mysql.connection.cursor()
        cur.callproc('GETPOST_BY_USERNAME',[session['username']])
        user_posts = cur.fetchall()
        l_user=len(user_posts)
        cur.close()
        print('user posts',user_posts)
        for t in user_posts:
            combination.append(t)
        #print('format friends list of posts:', combination)
        newlist = sorted(combination, key=itemgetter('date'), reverse=True) 
        print('new',newlist)
        l_post=len(newlist)
        return render_template("home.html",posts=newlist,l_user=l_user, l_post=l_post)
    else:
        return redirect(url_for('login'))


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form= SignupForm()
    if form.validate_on_submit():
        name = request.form['username']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        print('paasword:', hash_password)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO signup (username, email, password) VALUES (%s,%s,%s)",(name,email,hash_password,))
        mysql.connection.commit()
        session['username'] = request.form['username']
        session['email'] = request.form['email']
        flash(f' {form.username.data} Account created successfully','success')
        return redirect(url_for('createUser'))
    return render_template('register.html',title='Register', form=form, front_image= os.path.join(app.config['UPLOAD_FOLDER'], 'luis.gif'))



@app.route('/createUser', methods=['GET','POST'])
def createUser():
    form= UserForm()

    form2= SignupForm()
    print(session['username'])
    print(session['email'])
    if form.validate_on_submit():
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        about = request.form['about']
        telephone = request.form['telephone']
        street = request.form['street']
        city= request.form['city']
        country = request.form['country']

        email = session['email']
        username = session['username']
    

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO User (username, email, firstname,lastname,about,telephone,street,city,country) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(username,email,firstname,lastname,about,telephone,street,city,country))
        mysql.connection.commit()
        # session['username'] = request.form['username']
        # session['email'] = request.form['email']
        session['loggedin'] = True
        flash(f' {username} Account created and details successfully provided','success')
        return redirect(url_for('home'))
    return render_template('User.html',title='CreateUser', form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    form= LoginForm()
    if form.validate_on_submit():
            
        # if form.email.data=="admin@gmail.com" and form.password.data=="password":
        #     flash('Successfully logged in','success')
        #     return redirect(url_for('home'))
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password'].encode('utf-8')
            print("password entered:", password)
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute("SELECT * FROM signup WHERE email=%s",(email,))
            user = curl.fetchone()
            print("passs:    ",bcrypt.hashpw(password, user["password"].encode('utf-8')))
            print("pass from db:   ",user["password"].encode('utf-8') )
            strip= str(user["password"].encode('utf-8'))
            x=strip[2:-3]
            print(x)
            print(x.encode('utf-8'))
            curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == x.encode('utf-8'):
                session['username'] = user['username']
                session['email'] = user['email']
                session['loggedin'] = True
                flash('Successfully logged in','success')
                return redirect(url_for('home'))
        else:
            flash('Error logging in','danger')
    return render_template('login.html',title='Login', form=form, front_image = os.path.join(app.config['UPLOAD_FOLDER'], 'willian.gif'))






@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("logout.html", title='Logout')


@app.route('/profile', methods=["GET", "POST"])
# @login_required
def profile():
    form= UpdateUserForm()
    
    if form.validate_on_submit():
        username = request.form['username']
        
        email = request.form['email']
        firstname = request.form['firstname']
        
        lastname = request.form['lastname']
        
        about = request.form['about']
        
        telephone = request.form['telephone']
        
        street = request.form['street']
        
        city= request.form['city']
        
        country = request.form['country']
        
    
        
        cur = mysql.connection.cursor()
        cur.execute("Update User set username=%s, email=%s, firstname=%s,lastname=%s, about=%s, telephone=%s,street=%s,city=%s,country=%s where username=%s ",(username,email,firstname,lastname,about,telephone,street,city,country,session['username'],))
        mysql.connection.commit()
        cur.close()
        session['loggedin'] = True
        session['username'] = request.form['username']
        session['email'] = request.form['email']
        flash(f' {username} Account successfully updated','success')
        return redirect(url_for('profile'))
    elif request.method=='GET':
        pass
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curl.execute("SELECT * FROM User WHERE username=%s",(session['username'] ,))
    data = curl.fetchone()
    curl.close()
    default_image = os.path.join(app.config['UPLOAD_FOLDER'], 'default-picture.png')

    cur = mysql.connection.cursor()
    cur.callproc("GETPROFILE_PICTURE_BY_USERNAME",[session['username']])
    user_profile_pic = cur.fetchone()
    cur.close()
    print(user_profile_pic)
    return render_template("profile.html",title='Profile',default=default_image, form=form, pro_info=data,user_profile_pic=user_profile_pic)


def save_picture(form_picture):
    random_hex= secrets.token_hex(8)
    f_name,f_ext= os.path.splitext(form_picture.filename)
    picture_fn= random_hex+ f_ext
    picture_path= os.path.join(app.root_path,'static/photos',picture_fn)
    output_size=(650,760)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn




@app.route('/photo', methods=["GET", "POST"])
def photo():
    form=PictureForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            print(picture_file)
            print(form.profile_pic.data)
            cur = mysql.connection.cursor()
            cur.callproc("INSERT_INTO_PHOTOS",[picture_file,form.photo_name.data,form.description.data,form.profile_pic.data])
            cur.execute("INSERT INTO manage_photo (username,photo_id,date) VALUES (%s,%s,%s)",(session['username'],picture_file,datetime.now()))
            mysql.connection.commit()
        flash(f' {form.photo_name.data} picture upload successfully','success')
        return redirect(url_for('photo'))
    cur = mysql.connection.cursor()
    cur.execute("Select * from Photos where photo_id in (Select photo_id from manage_photo where username=%s)",(session['username'],))
    data = cur.fetchall()
    cur.close()
    print(data)
    return render_template('photo.html', title='Photos',form=form, pictures=data)


def save_picture_post(form_picture):
    random_hex= secrets.token_hex(10)
    f_name,f_ext= os.path.splitext(form_picture.filename)
    picture_fn= random_hex+ f_ext
    picture_path= os.path.join(app.root_path,'static/posts',picture_fn)
    output_size=(650,760)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route('/posts/new',methods=["GET", "POST"])
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post_hex= secrets.token_hex(40)
        if form.picture.data:
            pic=save_picture_post(form.picture.data)
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Posts (post_id,title,content,post_description,picture) VALUES (%s,%s,%s,%s,%s)",(post_hex,form.Title.data,form.Content.data,form.Description.data,pic))
            cur.execute("INSERT INTO Create_Post (username,post_id,date) VALUES (%s,%s,%s)",(session['username'],post_hex,datetime.now()))
           
            mysql.connection.commit()
            cur.close()
            
            flash(f' {form.Title.data} post created successfully','success')
            return redirect(url_for('home'))
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Posts (post_id,title,content,post_description) VALUES (%s,%s,%s,%s)",(post_hex,form.Title.data,form.Content.data,form.Description.data))
            cur.execute("INSERT INTO Create_Post (username,post_id,date) VALUES (%s,%s,%s)",(session['username'],post_hex,datetime.now()))

            mysql.connection.commit()
            cur.close()
            flash(f' {form.Title.data} post created successfully','success')
            return redirect(url_for('home'))

    return render_template('Create_post.html', title='Create Post',form=form, legend='Create Post')


@app.route('/posts/<string:post_id>', methods=["GET", "POST"])
def post(post_id):
    form = CommentForm()
    cur = mysql.connection.cursor()
    cur.callproc("GETPOST_BY_ID",[post_id])
    post=cur.fetchone()
    cur.close()
    print(post)
    cur = mysql.connection.cursor()
    cur.callproc("GETCOMMENT_BY_ID",[post_id])
    comments=cur.fetchall()
    cur.close()
    print('comments',comments)

    if request.method=='POST':
        print(session['username'],post_id,form.Comment.data, datetime.now())
        cur = mysql.connection.cursor()
        cur.callproc("MAKECOMMENT",[session['username'],post_id,form.Comment.data, datetime.now() ])
        
        mysql.connection.commit()
        cur.close()
        flash(f'Comment made successfully','success')
        #return redirect(url_for('home'))
        return redirect(url_for('post', post_id=post['post_id']))
    return render_template('post.html', title=post['title'],post=post, current_user=session['username'],form=form,comments=comments)

@app.route('/posts/<string:post_id>/update',methods=["GET", "POST"])
def update_post(post_id):
    cur = mysql.connection.cursor()
    cur.callproc("GETPOST_BY_ID",[post_id])
    post=cur.fetchone()
    cur.close()
    if post['username']!= session['username']:
        abort(403)
    form= PostForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.callproc("UPDATE_POSTS",[post['post_id'],form.Title.data,form.Content.data,form.Description.data])
        #cur.stored_results()
        mysql.connection.commit()
        # cur.close()
        flash(f'Post updated successfully','success')
        return redirect(url_for('post', post_id=post['post_id']))
    elif request.method=='GET':
        form.Title.data= post['title']
        form.Content.data= post['content']
        form.Description.data= post['post_description']
    return render_template('Create_post.html', title='Update Post',form=form, legend='Update Post')


@app.route('/posts/<string:post_id>/delete',methods=["POST"])
def delete_post(post_id):
    cur = mysql.connection.cursor()
    cur.callproc("GETPOST_BY_ID",[post_id])
    post=cur.fetchone()
    cur.close()
    if post['username']!= session['username']:
        abort(403)
    cur = mysql.connection.cursor()
    cur.callproc("DELETEPOST_BY_ID",[post_id])
    mysql.connection.commit()
    cur.close()
    flash(f'Post deleted successfully','success')
    return redirect(url_for('home'))





# friend routes 

@app.route('/friends/new',methods=["GET", "POST"])
def new_friends():
    form=FriendForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.callproc("INSERT_INTO_FRIENDS",[session['username'], form.friend_username.data, form.friend_type.data])
        mysql.connection.commit()
        cur.close()
        flash(f' {form.friend_username.data} added successfully','success')
        return redirect(url_for('all_friends'))
    return render_template('Find_friend.html', title='Find Friends',form=form, legend='Find Friends')



@app.route('/allfriends',methods=["GET", "POST"])
def all_friends():
    info_of_friends=[]
    
    dt={}
    cur = mysql.connection.cursor()
    cur.callproc("GETFRIENDS_BY_USERNAME",[session['username']])
    friends=cur.fetchall()
    cur.close()
    l_friends=len(friends)
    #print('friends info',friends, l_friends)
    for f in friends:
        name=f['friend_id']
        friend_type=f['friend_type']
        dt['friend_type']=friend_type
        dt['friend_id']=name
        
        cur = mysql.connection.cursor()
        cur.callproc("GETFRIENDS_INFO_BY_USERNAME",[f['friend_id']])
        friend_info=cur.fetchone()
        cur.close()
        #print('dt then friend info', friend_info, dt)
        friend_info.update(dt)
        info_of_friends.append(friend_info)
    #     print(friend_info)
    # print(info_of_friends)

    return render_template('all_friends.html', title='ALL FRIENDS',friends=info_of_friends,l_friends=l_friends)


#Group routes

@app.route('/groups/new',methods=["GET", "POST"])
def new_groups():
    form=GroupForm()
    groups=[]  
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.callproc("MAKEGROUP",[form.group_id.data, form.group_name.data, form.group_topic.data, form.group_context_editor.data])
        cur.callproc("GROUPCREATE",[session['username'], form.group_id.data, datetime.now()])
        mysql.connection.commit()
        cur.close()
        flash(f' {form.group_name.data} added successfully','success')
        return redirect(url_for('new_groups'))
    cur = mysql.connection.cursor()
    cur.callproc("GETGROUP_BY_USERNAME",[session['username']])
    my_groups= cur.fetchall()
    cur.close()
    len_group=len(my_groups)
    #print('my groups:   ',len_group)   
    return render_template('Create_group.html', title='Create Group',form=form, legend='Create New Group',groups=my_groups, len_group=len_group)


@app.route('/join_group',methods=["GET", "POST"])
def join_group():
    form=JoinForm() 
    if form.validate_on_submit():
        cur = mysql.connection.cursor()

        cur.callproc("JOINGROUP",[session['username'], form.group_id.data, datetime.now(),])
        mysql.connection.commit()
        cur.close()
        flash(f' You have sucessfully joined {form.group_id.data}','success')
        return redirect(url_for('join_group'))
    cur = mysql.connection.cursor()
    cur.callproc("GETGROUP_INFO",[session['username']])
    join_groups= cur.fetchall()
    cur.close()
    len_group=len(join_groups)
    print("groups:  ", join_groups, len_group)
    return render_template('join_group.html', title='Join a Group',form=form, legend='Join An Existing Group',len_group=len_group, groups=join_groups)






#### admin routes

@app.route('/admin',methods=["GET", "POST"])
def admin():
    form=AdminForm()
    info=[]
    info_friends=[]
    info_posts=[]
    info_comments=[]
    info_groups=[]
    len_post=0
    len_comment=0
    len_friends= 0
    len_groups= 0
    
    cur = mysql.connection.cursor()
    cur.execute("select count(*) as count from User")
    total_users=cur.fetchone()
    cur.execute("select count(*) as count from Friends")
    total_friends=cur.fetchone()
    cur.execute("select count(*) as count from Posts")
    total_posts=cur.fetchone()
    cur.execute("select count(*) as count from Comment")
    total_comments=cur.fetchone()
    cur.execute("select count(*) as count from Groups")
    total_groups=cur.fetchone()
    cur.close()
    total_users= total_users['count']
    total_friends= total_friends['count']
    total_posts= total_posts['count']
    total_comments= total_comments['count']
    total_groups= total_groups['count']
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.callproc("GETUSER_ADMIN_BY_USERNAME",[form.search.data])
        user_info=cur.fetchone()
        cur.close()
        info.append(user_info)

        cur = mysql.connection.cursor()
        cur.callproc("GETFRIEND_ADMIN_BY_USERNAME",[form.search.data])
        friends=cur.fetchall()
        info_friends.append(friends)
        cur.close()


        cur = mysql.connection.cursor()
        cur.callproc("GETPOST_ADMIN_BY_USERNAME",[form.search.data])
        posts=cur.fetchall()
        info_posts.append(posts)
        cur.close()


        cur = mysql.connection.cursor()
        cur.callproc("GETCOMMENT_ADMIN_BY_USERNAME",[form.search.data])
        comments=cur.fetchall()
        info_comments.append(comments)
        cur.close()

        cur = mysql.connection.cursor()
        cur.callproc("GETGROUP_ADMIN_BY_USERNAME",[form.search.data])
        groups=cur.fetchall()
        info_groups.append(groups)
        cur.close()
        print('info list:  >>>>>>> ', info)
        print('friend list:  >>>>>> ', info_friends)
        print('post list:  >>>>>>> ', info_posts)
        print('comment list: >>>>>>>>  ', info_comments)
        print('group list: >>>>>>>>  ', info_groups)
        len_post=len(info_posts[0])
        len_comment= len(info_comments[0])
        len_friends= len(info_friends[0])
        len_groups= len(info_groups[0])

        flash(f' User found','success')
        # return redirect(url_for('admin'))

    return render_template('admin.html', title='Administrator', form=form,info=info, info_friends=info_friends,len_friends=len_friends,info_posts=info_posts,len_post=len_post,len_comment=len_comment,info_comments=info_comments,
                            ts=total_users,tf=total_friends, tp=total_posts, tc=total_comments, tg=total_groups,
                            len_c= len_comment, len_p=len_post, len_groups=len_groups, info_groups=info_groups)


# @app.route('/admin/results',methods=["GET","POST"])
# def admin_results():
#     form=AdminForm()
#     info=[]
#     if form.validate_on_submit():
#         cur = mysql.connection.cursor()
#         cur.callproc("GETUSER_ADMIN_BY_USERNAME",[form.search.data])
#         user_info=cur.fetchone()
#         cur.close()
#         info.append(user_info)
#         flash(f' User found','success')
#         print('results:', info)
#         return redirect(url_for('admin_results', info=info))
#     return render_template('admin2.html', title='Administrator', form=form,info=info)







if __name__=='__main__':
    app.run(debug=True)
