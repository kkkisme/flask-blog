from galaxy import db, login_manager
from flask_login import UserMixin
from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return "User('{}', '{}')".format(self.id, self.username)

    def get_reset_token(self, expires_in=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except KeyError:
            return None
        return User.query.get(user_id)


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(message='不能为空'), Length(min=2, max=20, message='长度必须为2-20之间')])
    email = StringField('Email',
                        validators=[DataRequired(message='不能为空'), Email(message='无效的邮箱地址')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=72, message='长度必须为6-72之间')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(message='不能为空'), EqualTo('password', message='密码不一致')])
    submit = SubmitField('Sign Up')

    @staticmethod
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('用户名已经被使用')

    @staticmethod
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('邮箱已经被使用')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    remember = BooleanField('Remember Me')
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(message='不能为空'), Length(min=2, max=20, message='长度必须为2-20之间')])
    email = StringField('Email',
                        validators=[DataRequired(message='不能为空'), Email(message='无效的邮箱地址')])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    @staticmethod
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    @staticmethod
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(message='不能为空'), Email(message='无效的邮箱地址')])
    submit = SubmitField('Reset')

    @staticmethod
    def validate_email(self, email):
        u = User.query.filter_by(email=email.data).first()
        if not u:
            raise ValidationError('此账户不存在')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=72, message='长度必须为6-72之间')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(message='不能为空'), EqualTo('password', message='密码不一致')])
    submit = SubmitField('Reset password')

