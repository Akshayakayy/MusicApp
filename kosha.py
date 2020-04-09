import sys
from datetime import datetime, timedelta
from flask import Flask,render_template,request,flash,redirect,url_for,session,logging,jsonify
from wtforms import Form,BooleanField,StringField,validators,PasswordField,TextAreaField,SubmitField
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SECRET_KEY']='Thisshouldwork'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///musicdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)


PublicPlaylist=db.Table('PublicPlayList',
    db.Column('user_id',db.Integer,db.ForeignKey('users.user_id')),
    db.Column('music_id',db.Integer,db.ForeignKey('links.music_id')),
)

PrivatePlaylist=db.Table('PrivatePlaylist',
    db.Column('user_id',db.Integer,db.ForeignKey('users.user_id')),
    db.Column('music_id',db.Integer,db.ForeignKey('links.music_id'))
)

class User(db.Model):
    __tablename__='users'
    user_id=db.Column(db.Integer,primary_key=True,nullable=False)
    username=db.Column(db.String(50),unique=True)
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(80))

class Music(db.Model):
    __tablename__='links'
    music_id=db.Column(db.Integer,primary_key=True,nullable=False)
    Song_Name=db.Column(db.String(50),unique=True)
    Genres=db.Column(db.String(50))
    Url_Path=db.Column(db.String(80))
    PublicListener=db.relationship('User',secondary=PublicPlaylist,backref=db.backref('PublicListensTo',lazy='dynamic'))
    PrivateListener=db.relationship('User',secondary=PrivatePlaylist,backref=db.backref('PrivateListensTo',lazy='dynamic'))

class Message(db.Model):
    __tablename__='Notifications'
    message_id=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    sender_id=db.Column(db.Integer,db.ForeignKey('users.user_id'))
    recipient_id=db.Column(db.Integer,db.ForeignKey('users.user_id'))
    body=db.Column(db.String(200))
    timestamp=db.Column(db.DateTime,index=True,default=datetime.utcnow)

class Follow(db.Model):
    __tablename__='follow'
    following_id=db.Column(db.Integer,primary_key=True,nullable=False)
    follower=db.Column(db.String(50),db.ForeignKey('users.username'))
    followed=db.Column(db.String(50),db.ForeignKey('users.username'))

class RegistrationForm(Form):
    UserName=StringField('UserName',[validators.Length(min=4,max=50)])
    Email=StringField('Email Address',[validators.Length(min=6,max=35)])
    Password=PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm',message='Passwords do not match,try again!')
    ])
    confirm=PasswordField('Confirm Password')

class LoginForm(Form):
    UserName=StringField('UserName',[validators.Length(min=4,max=50)])
    Password=PasswordField('Password',[
        validators.DataRequired(),
        validators.Length(min=2,max=80)
    ])

@app.route('/')
def KoshaPage():
    return render_template('welcome.html')

@app.route('/home')
def UserPage():
    return render_template('home.html')

@app.route('/profile',methods=['GET','POST'])
def myprofile():
    user=User.query.filter_by(username=session['username']).first()
    if request.method=='POST':
        return redirect(url_for('SearchPage',SearchedUser=request.form['search']))
    return render_template('profile.html',PrivateUser=user.PrivateListensTo,PublicUser=user.PublicListensTo)

@app.context_processor
def inject_notification():
    try:
        user=User.query.filter_by(username=session['username']).first()
        notificationlist=Message.query.filter_by(recipient_id=user.user_id).all()
    except:
        notificationlist=[]
    return dict(Notifications=notificationlist)

@app.route('/SearchResults/<SearchedUser>',methods=['GET','POST'])
def SearchPage(SearchedUser):
    if SearchedUser==session['username']:
        return redirect(url_for('myprofile'))
    else:
        try:
            querieduser=User.query.filter_by(username=SearchedUser).first()
            if request.method=='POST':
                if request.form['type']=='FOLLOW':
                    followingreq=Follow(follower=session['username'],followed=SearchedUser)
                    db.session.add(followingreq)
                    user=User.query.filter_by(username=session['username']).first()
                    msg=Message(sender_id=user.user_id,recipient_id=querieduser.user_id,body=session['username']+' has started following you.')
                    db.session.add(msg)
                    db.session.commit()
                else:
                    z=Follow.query.filter_by(follower=session['username'],followed=SearchedUser).delete()
                    db.session.commit()
            flag=0
            followings=Follow.query.filter_by(follower=session['username']).all()
            print(followings)
            if followings:
                for following in followings:
                    if following.followed == SearchedUser:
                        flag=1
                        print(flag)
            if flag==1:
                followbutton='hide'
                unfollowbutton='show'
            else:
                followbutton='show'
                unfollowbutton='hide'
                print(followbutton,unfollowbutton)
            return render_template('searchpage.html',SearchedUser=SearchedUser,SearchUser=querieduser.PublicListensTo,followstate=followbutton,unfollowstate=unfollowbutton)
        except:
            return '<h1>No such user</h1>'


@app.route('/discover')
def DisPage():
	return render_template('discover.html')

@app.route('/discover/<genre>',methods=['GET','POST'])
def genres(genre):
    musiclist=Music.query.filter_by(Genres=genre).all()
    if request.method=='POST':
        if session['logged_in']:
            user=User.query.filter_by(username=session['username']).first()
            music=Music.query.filter_by(Song_Name=request.form['name']).first()
            if request.form['type']=='Public':
                user.PublicListensTo.append(music)
                db.session.add(user)
                recipients=Follow.query.filter_by(followed=session['username']).all()
                for recipient in recipients:
                    rec=User.query.filter_by(username=recipient.follower).first()
                    msg=Message(sender_id=user.user_id,recipient_id=rec.user_id,body=session['username']+' has added the song '+music.Song_Name+' to the playlist!')
                    db.session.add(msg)

            if request.form['type']=='Private':
                user.PrivateListensTo.append(music)
                db.session.add(user)
            db.session.commit()

    return render_template(genre+'.html',Music=musiclist)


@app.route('/SignUp',methods=['GET','POST'])
def Register():
    RForm=RegistrationForm(request.form)
    if request.method == 'POST' and RForm.validate():
        new_user=User(username=RForm.UserName.data,email=RForm.Email.data,password=RForm.Password.data)
        db.session.add(new_user)
        db.session.commit()
        session['logged_in']=True
        session['username']=RForm.UserName.data
        return redirect(url_for('UserPage'))

    return render_template('register.html',form=RForm)

@app.route('/Login',methods=['GET','POST'])
def LoginPage():
    LForm=LoginForm(request.form)
    if request.method == 'POST' and LForm.validate():
        user=User.query.filter_by(username=LForm.UserName.data).first()
        if user:

            if user.password == LForm.Password.data:

                session['logged_in']=True
                session['username']=LForm.UserName.data
                return redirect(url_for('UserPage'))
            else:

                error='You typed the wrong username or password'
                return render_template('login.html',error=error,form=LForm)

        error='You typed the wrong username or password'
        return render_template('login.html',error=error,form=LForm)

    return render_template('login.html',form=LForm)

@app.route('/LogOut')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('LoginPage'))

if __name__ == '__main__':
    app.run(debug=True)
