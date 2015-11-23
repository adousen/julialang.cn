#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
from datetime import datetime
from werkzeug.utils import cached_property
from flask.ext.principal import Permission, UserNeed
from flask import url_for
from sqlalchemy import orm

from project import db

from contrib.utils import identicon
from contrib.utils import functions
from project.permissions import RoleNeeds, RolePerms, AccessNeeds, AccessPerms


class UserQuery(db.Query):
    # def __init__(self, obj, entities, session=None):
    #     self.obj = obj
    #     super(UserQuery, self).__init__(entities, session)


    # utils
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(userid):
        return User.query.filter_by(id=userid).first()

    @classmethod
    def is_email_exist(cls, email):
        user = User.query.filter_by(email=email).first()
        if user:
            return True
        else:
            return False

    @classmethod
    def is_username_exist(cls, username):
        user = User.query.filter_by(username=username).first()
        if user:
            return True
        else:
            return False

    @classmethod
    def is_nickname_exist(cls, nickname):
        user = User.query.filter_by(nickname=nickname).first()
        if user:
            return True
        else:
            return False


class User(db.Model):
    query_class = UserQuery

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(255), unique=True)
    # nickname = db.Column(db.NVARCHAR(255), unique=True)
    email = db.Column(db.VARCHAR(255), unique=True)
    password_hash = db.Column(db.VARCHAR(255), nullable=False)
    #role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    confirmed = db.Column(db.BOOLEAN)
    data_join = db.Column(db.DATETIME, default=datetime.now())  # auto_now_add
    last_login = db.Column(db.DATETIME, default=datetime.now())  # auto_now_add
    last_active = db.Column(db.DATETIME, default=datetime.now())  # auto_now_add
    active = db.Column(db.BOOLEAN, default=False)  # on line or off line
    locked = db.Column(db.BOOLEAN, default=False)
    deleted = db.Column(db.BOOLEAN, default=False)
    location = db.Column(db.NVARCHAR(255))
    about_me = db.Column(db.TEXT, nullable=True)
    avatar = db.Column(db.BLOB, nullable=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = kwargs.get('password', 'default_pwd')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = functions.encrypt_password(password)

    class Permissions(object):

        def __init__(self, obj):
            self.obj = obj

        @cached_property
        def edit(self):
            return Permission(UserNeed(self.obj.id)) or RolePerms.admin

        @cached_property
        def admin(self):
            return RolePerms.admin

    @cached_property
    def permissions(self):
        return self.Permissions(self)

    @cached_property
    def provides(self):
        # TODO: 从数据库初始化用户管理操作权限
        needs = [RoleNeeds.auth, UserNeed(self.id)]

        # TODO: 根据用户角色的group字段值的不同采取相应的权限加载策略
        if self.is_moderator:
            print "cur permission is: moderator"
            needs.append(RoleNeeds.moderator)
            needs.extend(AccessNeeds.Blog.allNeedsList)

        if self.is_admin:
            needs.append(RoleNeeds.admin)
            needs.extend(AccessNeeds.Blog.allNeedsList)

        return needs

    @property
    def is_moderator(self):
        # TODO：求权限列表中的最大值
        # 数据库中permissions字段类型是字符串
        return int(self.role.permissions) == 2

    @property
    def is_admin(self):
        return int(self.role.permissions) == 3

    @property
    def is_superuser(self):
        return int(self.role.permissions) == 4

    # # active method
    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception, msg:
            print('Error: Cannot save user, because ' + msg.message)
            db.session.rollback()
            return False
        return True


    def verify_password(self, password):
        return functions.check_password(password, self.password_hash)

    # flask-login-method
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    # ping-method before request
    def ping(self):
        self.last_active = datetime.now()
        self.save()

    # user confirm
    def confirm(self):
        self.confirmed = True
        self.save()
        return True

    def gravatar(self, size=10):
        if self.avatar is None or self.avatar == '':
            self.avatar = identicon.generate_avatar(self.id, size=10)
            self.save()

        return url_for('account.avatar', user_id=self.id, size=size)