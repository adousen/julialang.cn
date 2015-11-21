#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'adousen'
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
from wtforms import ValidationError

from models import User, Roles
# 技巧：引入类后，PyCharmh会给其小写的间接引用变量提供成员提示

class RegisterForm(Form):
    email = StringField(u'注册邮箱', validators=[DataRequired(u'邮箱不能为空'), Email(u'请输入正确的邮箱地址')])
    password = PasswordField(u'账号密码',
                             validators=[DataRequired(u'密码不能为空'), Length(min=6, message=u'密码不能低于6位')])
    repassword = PasswordField(u'确认密码', validators=[EqualTo('password', message=u'密码不一致')])
    submit = SubmitField(u'注册账号')

    def validate_email(self, field):
        if User.query.is_email_exist(field.data):
            raise ValidationError(u'邮箱已经存在')


class LoginForm(Form):
    email = StringField(u'邮箱账号', validators=[DataRequired(u'邮箱不能为空'), Email(u'请输入正确的邮箱地址')])
    password = PasswordField(u'账号密码',
                             validators=[DataRequired(u'密码不能为空'), Length(min=6, message=u'密码不能低于6位')])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class EditProfileForm(Form):
    nickname = StringField(u'昵称', validators=[Length(0, 64, message=u'昵称长度不能超过64位')])
    location = StringField(u'所在地', validators=[Length(0, 64, message=u'所在地长度不能超过64位')])
    about_me = TextAreaField(u'自我介绍', validators=[Length(0, 64, message=u'长度不能超过255位')])
    submit = SubmitField(u'提交')


class EditProfileAdminForm(Form):
    email = StringField(u'邮箱账号', validators=[Length(0, 64, message=u'昵称长度不能超过64位')])
    username = StringField(u'用户名', validators=[
        DataRequired(u'用户名不能为空'), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                        u'用户名只能是以字母开头， '
                                                        u'以及字母、数字、‘.’ 或者下划线的组合')])
    role = SelectField(u'用户组', coerce=int)
    nickname = StringField(u'昵称', validators=[Length(0, 64, message=u'昵称长度不能超过64位')])
    location = StringField(u'所在地', validators=[Length(0, 64, message=u'所在地长度不能超过64位')])
    about_me = TextAreaField(u'自我介绍', validators=[Length(0, 64, message=u'长度不能超过255位')])
    confirmed = BooleanField(u'已认证')
    locked = BooleanField(u'已冻结')
    deleted = BooleanField(u'已删除')
    submit = SubmitField(u'提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Roles.all()]
        self.user = user

    # 保证新值不与数据库已存在的值重复
    # 且如果字段的值没有变化就应跳过
    def validate_email(self, field):
        if field.data != self.user.email \
                and User.query.is_email_exist(field.data):
            raise ValidationError(u'邮箱已经存在')

    def validate_username(self, field):
        if field.data != self.user.username\
                and User.query.is_username_exist(field.data):
            raise ValidationError(u'用户名已经存在')

    def validate_nickname(self, field):
        if field.data != self.user.nickname\
                and User.query.is_nickname_exist(field.data):
            raise ValidationError(u'昵称已经存在')