from flask import request, Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, current_user, login_required
from galaxy.models.user import RegistrationForm, LoginForm, AccountForm, ResetPasswordRequestForm, ResetPasswordForm, User
from galaxy import db, bcrypt, mail
from flask_mail import Message
from PIL import Image
import secrets
import os


user = Blueprint('user', __name__)


@user.route('/register', methods=['GET', 'POST'])
def register():
    flash(message=f'暂不提供注册功能', category='warning')
    return redirect(url_for('main.home'))
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.home'))
    # form = RegistrationForm()
    # if form.validate_on_submit():
    #     hashed_password = bcrypt.generate_password_hash(form.password.data)
    #     u = User(username=form.username.data, email=form.email.data, password=hashed_password)
    #     db.session.add(u)
    #     db.session.commit()
    #     flash(message=f'Your account has been created! You are now able to log in', category='success')
    #     return redirect(url_for('user.login'))
    # return render_template('views/register.html', title='注册', form=form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u and bcrypt.check_password_hash(u.password, form.password.data):
            login_user(u, remember=form.remember.data)
            flash(message='登录成功', category='success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(message='Login Unsuccessful! Please check email and password.', category='danger')
    return render_template('views/login.html', title='注册', form=form)


@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@user.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    image_file = url_for('static', filename='profile_pics/{}'.format(current_user.image_file))
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('user.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('views/account.html', title='账户', form=form, image_file=image_file)


@user.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        send_email(u)
        flash('重置密码的邮件发送成功', 'info')
        return redirect(url_for('user.login'))
    return render_template('views/reset-password-request.html', title='Reset password', form=form)


@user.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    u = User.verify_reset_token(token)
    if u is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('user.reset_password_request'))
    if form.validate_on_submit():
        u.password = bcrypt.generate_password_hash(form.password.data)
        db.session.commit()
        flash('Your password has been reset!', 'success')
        return redirect(url_for('user.login'))
    return render_template('views/reset-password.html', title='Reset password', form=form)


def send_email(u):
    token = u.get_reset_token()
    msg = Message('重置你的密码',
                  sender='no-replay@demo.com',
                  recipients=[u.email])
    msg.body = f'''
     点击连接以重置你的密码{url_for('user.reset_password', token=token, _external=True)}
    '''
    msg.html = f'''
         点击连接以重置你的密码 
         <a href="{url_for('user.reset_password', token=token, _external=True)}">
{url_for('user.reset_password', token=token, _external=True)}</a> 
        '''
    mail.send(msg)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(size)
    i.save(picture_path)

    return picture_fn

