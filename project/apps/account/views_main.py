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

            # if user.save():
            #     from contrib.mail import generate_confirmation_token
            #     token = generate_confirmation_token(user.id)
            #
            #     from project.application import sendmail
            #     from flask import current_app as app
            #     if app.config['FLASKY_ADMIN']:
            #         print app.config['FLASKY_ADMIN']+'111'
            #         sendmail.send_email(app.config['FLASKY_ADMIN'], u'请确认您的账号', 'mail/confirm', user=user, token=token)
            #
            #     flash(u'一封确认邮件已发送到你的邮箱，请查收邮件并完成确认.')
            #

            flash(u'注册成功.')
            return redirect(url_for('account.register'))
        return render_template('account/register.html', form=form)


'''
1.判断用户是否已登录
2.若未登录,则根据token对应的id获取user，若登陆则从current_user获取user
3.激活user
4.转到User登录状态
5.跳转到首页
'''

'''
1.获取用户email和password
2.判断email是否合法
3.判断email是否存在
4.判断password与email是否匹配
5.跳转到首页
'''

