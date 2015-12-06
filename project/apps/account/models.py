#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
from datetime import datetime
from functools import partial

from werkzeug.utils import cached_property
from flask.ext.principal import Permission, UserNeed
from flask import url_for
from flask.ext.login import UserMixin

from contrib.utils import identicon
from contrib.utils import functions
from contrib.utils.functions import all_menber

from project import db
from project.permissions import RoleNeeds, RolePerms, CodePerms, ManageNeed


class ActiveRecordMixin(object):
    def __init__(self, *args, **kwargs):
        pass

    # ActiveRecord method
    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception, msg:
            print('Error: Cannot save %s object, because ' % self.__class__ + msg.message)
            db.session.rollback()
            return False
        return True


class UserLoginMixin(UserMixin):
    pass


class UserPermissionMixin(object):
    class Permissions(object):

        def __init__(self, obj):
            self.obj = obj

        def can(self, method):
            """判断是否允许被用户自己进行操作"""
            return Permission(UserNeed(self.obj.id))

    @cached_property
    def permissions(self):
        return self.Permissions(self)

    # Permission Provides
    @cached_property
    def provides(self):
        # 从数据库初始化用户管理操作权限
        needs = [RoleNeeds.auth, UserNeed(self.id)]
        needs.extend([UserNeed(self.id)])
        # 根据code_to_role表的权限分配加载
        records = CodeToRole.query.get_all_by_role_level(self.role.level)
        for record in records:
            needs.extend([partial(ManageNeed, record.method)(record.permission_code)])

        return needs

    @property
    def is_moderator(self):
        # TODO：求权限列表中的最大值
        # 数据库中permissions字段类型是字符串
        return int(self.role.level) == 3

    @property
    def is_admin(self):
        return int(self.role.level) == 2

    @property
    def is_superuser(self):
        return int(self.role.level) == 1


class UserQuery(db.Query):
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


class User(db.Model, ActiveRecordMixin, UserLoginMixin, UserPermissionMixin):
    query_class = UserQuery
    __tablename__ = 'user'

    id = db.Column(db.INT, primary_key=True)
    username = db.Column(db.NVARCHAR(255), unique=True)
    #nickname = db.Column(db.NVARCHAR(255), unique=True)
    email = db.Column(db.NVARCHAR(255), unique=True)
    password_hash = db.Column(db.NVARCHAR(255), nullable=False)
    role_id = db.Column(db.INT, db.ForeignKey('role.id'))
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

    def verify_password(self, password):
        return functions.check_password(password, self.password_hash)

    # Confirmation
    def confirm(self):
        self.confirmed = True
        self.save()
        return True

    def get_avatar(self, size=10):
        if self.avatar is None or self.avatar == '':
            self.avatar = identicon.generate_avatar(self.id, size=10)
            self.save()

        return url_for('account.avatar', user_id=self.id, size=size)

    # ping-method before request
    def ping(self):
        self.last_active = datetime.now()
        self.save()


class Role(db.Model, ActiveRecordMixin):
    __tablename__ = 'role'
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.NVARCHAR(255), unique=True)
    default = db.Column(db.BOOLEAN, default=False, index=True)
    group = db.Column(db.INT, default=1)   # 当角色有多个分组时使用，可用于未来扩展，默认为1
    level = db.Column(db.INT, default=1000)   # 角色的权限等级，值越小权限越大
    permissions = db.Column(db.TEXT, unique=False)  # deprecated
    users = db.relationship('User', backref='role')

    @staticmethod
    def init_data():
        """初始化roles表的角色表数据"""
        roles = (RolePerms.superuser, RolePerms.admin, RolePerms.moderator, RolePerms.auth)

        for r in roles:
            role = Role.query.filter_by(name=r.name).first()
            if role is None:
                role = Role(name=r.name)

            role.permissions = r.permissions
            role.group = r.group
            role.level = r.level
            role.default = r.default

            role.save()

    # @staticmethod
    # def get_role_by_permission(permission):
    #     return Roles.filter(Roles.c.permissions == permission).one()


class PermissionCode(db.Model, ActiveRecordMixin):
    __tablename__ = 'permission_code'
    id = db.Column(db.INT, primary_key=True)
    code = db.Column(db.TEXT, unique=False)  # 权限编码
    parent_code = db.Column(db.TEXT, default=0, unique=False)  # 父级权限编码
    name = db.Column(db.NVARCHAR(80), nullable=False)
    description = db.Column(db.TEXT)

    @staticmethod
    def init_data():
        """初始化Permission表数据"""

        default_pcode = 0

        # confirm if need init super code
        super_perm = PermissionCode.query.filter_by(name=u'超级权限').first()
        if super_perm is None:
            permission = PermissionCode(code="0", name=u'超级权限', parent_code=default_pcode)
            permission.save()

        for class_name, perm_class in all_menber(CodePerms).items():
            for key, item in all_menber(perm_class).items():
                perm = PermissionCode.query.filter_by(name=item.name).first()
                if perm is None:
                    if item.code % 100 == 0:
                        pcode = item.parent_code
                    else:
                        # pcode = (int(item.code / 100)) * 100
                        pcode = (item.code // 100) * 100

                    permission = PermissionCode(code=item.code, name=item.name, parent_code=pcode)
                    permission.save()


class CodeToRoleQuery(db.Query):
    # utils
    @staticmethod
    def get_all_by_role_level(level):
        return CodeToRole.query.filter_by(role_level=level).all()


class CodeToRole(db.Model, ActiveRecordMixin):
    query_class = CodeToRoleQuery
    __tablename__ = 'code_to_role'
    id = db.Column(db.Integer, primary_key=True)
    role_level = db.Column(db.INT)
    permission_code = db.Column(db.INT)
    method = db.Column(db.NVARCHAR(20))

    @staticmethod
    def init_data():
        def init_superuser():
            existed_super_level = CodeToRole.query.filter_by(role_level=1).first()
            if existed_super_level is None:
                for class_name, perm_class in all_menber(CodePerms).items():
                    for key, item in all_menber(perm_class).items():
                        CodeToRole(role_level=RolePerms.superuser.level, permission_code=item.code, method=item.method).save()

        def init_admin():
            existed_admin_level = CodeToRole.query.filter_by(role_level=2).first()
            if existed_admin_level is None:
                for class_name, perm_class in all_menber(CodePerms).items():
                    for key, item in all_menber(perm_class).items():
                        CodeToRole(role_level=RolePerms.admin.level,permission_code=item.code, method=item.method).save()

        def init_moderator():
            existed_moderator_level = CodeToRole.query.filter_by(role_level=3).first()
            if existed_moderator_level is None:
                for class_name, perm_class in all_menber(CodePerms).items():
                    for key, item in all_menber(perm_class).items():
                        if item.code > 140:
                            CodeToRole(role_level=RolePerms.moderator.level,permission_code=item.code, method=item.method).save()

        init_superuser()
        init_admin()
        init_moderator()


class CodeToUser(db.Model, ActiveRecordMixin):
    __tablename__ = 'code_to_user'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.INT)
    user_id = db.Column(db.INT)
