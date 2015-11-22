#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    account.views_main
    ~~~~~~~~~~~~~~~~~~

    注册、激活、登录、登出

    :copyright: (c) 2015 by adousen.
"""
import datetime
from flask import current_app, request, render_template, redirect, url_for, flash
from flask.ext.login import login_required, login_user, logout_user, current_user
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity

from .import account
from .models import User
from project import login_manager

login_manager.session_protection = 'strong'

login_manager.login_view = 'account.login'
login_manager.login_message = u'你没有权限访问该页面，请先登录'
# @login_manager.unauthorized_handler
# def unauthorized_callback():
#     flash(u'你没有权限访问该页面，请先登录')
#     return redirect(url_for('account.login'))


@login_manager.user_loader
def load_user(userid):
    return User.query.get_by_id(userid)


@account.before_app_request
def before_request():
    if current_user.is_authenticated():
        # 登记用户活动时间
        current_user.ping()

        # 过滤用户请求
        if not current_user.confirmed \
                and request.endpoint[:8] != 'account.' \
                and request.endpoint != 'static':
            return redirect(url_for('account.unconfirmed'))

@account.route('/register', methods=['GET', 'POST'])
def register():
    from .forms import RegisterForm
    form = RegisterForm()  # 在这里，flask-wtf默认地完成了与request.form的绑定
    if request.method == 'GET':
        return render_template('account/register.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User(email=email, password=password)
            user.save()
            user.nickname = u'友友[' + str.format("1%07d" % int(user.id)) + ']'

            if user.save():
                from contrib.mail import generate_confirmation_token
                token = generate_confirmation_token(user.id)

                from project import sendmail
                from flask import current_app
                if current_app.config['MAIL_TEST_ACCOUNT']:
                    print current_app.config['MAIL_TEST_ACCOUNT']
                    sendmail.send_email(current_app.config['MAIL_TEST_ACCOUNT'], u'请确认您的账号', 'account/mail/confirm', user=user, token=token)

                flash(u'一封确认邮件已发送到你的邮箱，请查收邮件并完成确认.')

            return redirect(url_for('account.register'))
        return render_template('account/register.html', form=form)

'''
用户账户激活
1.判断用户是否已登录
2.若未登录,则根据token对应的id获取user，若登陆则从current_user获取user
3.激活user
4.转到User登录状态
5.跳转到首页
'''
@account.route('/confirm/<token>')
def confirm(token):
    if current_user.is_authenticated:
        from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except BadSignature:
            flash(u'错误操作')
            return redirect(url_for('community.index'))

        user_id = data.get('confirm')
        user = User.query.get_by_id(user_id)

    else:
        user = current_user

    if user.confirmed:
        return redirect(url_for('community.index'))
    if user.confirm():
        flash(u'账号激活成功，谢谢!')
        login_user(user)
        identity_changed.send(current_app._get_current_object(),
                    identity=Identity(user.id))
    else:
        flash(u'激活链接非法或已过期。')
    return redirect(url_for('community.index'))


@account.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous() or current_user.confirmed:
        return redirect(url_for('community.index'))
    return render_template('account/unconfirmed.html')


@account.route('/confirm')
@login_required
def resend_confirmation():
    from contrib.mail import generate_confirmation_token
    token = generate_confirmation_token(current_user.id)

    # send email
    from project import sendmail
    from flask import current_app as app
    if app.config['MAIL_TEST_ACCOUNT']:
        print app.config['MAIL_TEST_ACCOUNT']
        sendmail.send_email(app.config['MAIL_TEST_ACCOUNT'], u'请确认您的账号', 'mail/confirm', user=current_user, token=token)

    flash(u'一封新的确认邮件已经发送到你的邮箱。')
    return redirect(url_for('community.index'))

'''
用户登录
1.获取用户email和password
2.判断email是否合法
3.判断email是否存在
4.判断password与email是否匹配
5.跳转到首页
'''

