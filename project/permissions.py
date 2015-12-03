#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'adousen'

__all__ = ['RoleNeeds', 'RolePerms', 'AccessNeeds', 'AccessPerms']

from functools import partial, wraps
from werkzeug.utils import cached_property
from flask import abort, g, current_app
from flask.signals import Namespace
from flask.ext.principal import Principal, Identity, IdentityContext, \
    Permission, AnonymousIdentity, identity_changed, identity_loaded, \
    UserNeed, RoleNeed, ActionNeed, PermissionDenied, Need, namedtuple

user_no_permission_signal = Namespace().signal('no-permission')


class IdentityContextArgumentsError(ValueError):
    """ 参数值错误 """


class IdentityContextForManage(IdentityContext):
    """ 根据调用者的权限，生成对数据库对象进行管理操作的上下文环境，
        可以用作装饰器。
    """
    def __init__(self, permission, cls=None, http_exception=None):
        self.cls = cls
        self.param_id = None
        super(IdentityContextForManage, self).__init__(permission, http_exception)

    def can(self):
        """Whether the identity has access to the permission
        """
        if self.param_id is not None:
            if self.cls is None:
                raise IdentityContextArgumentsError()

            obj = self.cls.query.get_by_id(self.param_id)

            # 循环测试
            ret_val = True
            for need in self.permission.needs:
                if need.method == "edit" and obj.permissions.edit:
                    ret_val = True and ret_val

                elif need.method == "delete" and obj.permissions.delete:
                    ret_val = True and ret_val

                elif need.method == "role":
                    if need.value == "admin" and obj.permissions.admin:  # need.group
                        ret_val = True and ret_val
                    else:
                        user_no_permission_signal.send(current_app._get_current_object())
                        return False
                else:
                    user_no_permission_signal.send(current_app._get_current_object())
                    return False

                # TODO: 继续添加其他管理操作
            return ret_val

        return self.identity.can(self.permission)

    def __call__(self, fn):
        @wraps(fn)
        def _decorated(*args, **kw):
            target_id = kw["id"]
            self.param_id = target_id
            with self:
                rv = fn(*args, **kw)
            return rv
        return _decorated


class MangePermission(Permission):
    """用于定义数据库对象管理操作相关的权限的类
    """
    def require(self, cls=None, http_exception=None):
        """Represents needs, any of which must be present to access a resource

        :param cls: 权限验证函数所在的类
        :param http_exception: 权限验证失败后的错误响应代码
        """
        return IdentityContextForManage(self, cls, http_exception)


# Need：定义基于角色的系统权限
class RoleNeeds(object):
    """与系统中的各个角色相对应的权限字段（need）
    """

    auth = RoleNeed('auth')
    moderator = RoleNeed('moderator')
    admin = RoleNeed('admin')
    superuser = RoleNeed('superuser')


# Permissions：根据相应的系统角色许可
class RolePerms(object):
    """
    与系统中的各个角色相对应的权限组（permission）
    """
    auth = MangePermission(RoleNeeds.auth)
    auth.permissions = ''
    auth.level = 1000
    auth.name = "Auth"
    auth.group = 1
    auth.default = True

    moderator = MangePermission(RoleNeeds.moderator)
    moderator.permissions = ''
    moderator.level = 3
    moderator.name = "Moderator"
    moderator.group = 1
    moderator.default = False

    admin = MangePermission(RoleNeeds.admin)
    admin.permissions = ''
    admin.level = 2
    admin.name = "Admin"
    admin.group = 1
    admin.default = False

    superuser = MangePermission(RoleNeeds.superuser)
    superuser.permissions = ''
    superuser.level = 1
    superuser.name = "Superuser"
    superuser.group = 1
    superuser.default = False

    # this is assigned when you want to block a permission to all
    # never assign this role to anyone !
    null = MangePermission(RoleNeed('null'))


# Needs ：定义基于操作的系统权限
ManageNeed = namedtuple('Manage', ['method', 'group'])

EditNeed = partial(ManageNeed, 'edit')
LockNeed = partial(ManageNeed, 'lock')
DeleteNeed = partial(ManageNeed, 'delete')
AddNeed = partial(ManageNeed, 'add')


# Permissions for more granular access control
class AccessNeeds(object):
    """
    与系统中的各种操作相对应的权限字段（need）
    """
    class User(object):
        editNeed = EditNeed('default')

        addNeed = AddNeed('admin')
        lockNeed = LockNeed('admin')
        deleteNeed = DeleteNeed('admin')

        allNeedsList = [editNeed, lockNeed, deleteNeed, addNeed]

    class Blog(object):
        addNeed = AddNeed('default')
        editNeed = EditNeed('default')
        lockNeed = LockNeed('default')
        deleteNeed = DeleteNeed('default')

        allNeedsList = [editNeed, deleteNeed, lockNeed]


class AccessPerms(object):
    """
    各模块操作对应的permission
    """
    class User(object):
        manage = MangePermission(*AccessNeeds.User.allNeedsList)
        manage.code = 100
        manage.parent_code = 100
        manage.name = u'管理用户'

        add = MangePermission(AccessNeeds.User.addNeed)
        add.code = 101
        add.parent_code = 100
        add.name = u'添加用户'

        delete = MangePermission(AccessNeeds.User.deleteNeed)
        delete.code = 102
        delete.parent_code = 100
        delete.name = u'删除用户'

        lock = MangePermission(AccessNeeds.User.lockNeed)
        lock.code = 141
        lock.parent_code = 100
        lock.name = u'锁定用户'

        edit = MangePermission(AccessNeeds.User.editNeed)
        edit.code = 171
        edit.parent_code = 100
        edit.name = u'编辑用户信息'


    class Blog(object):
        manage = MangePermission(*AccessNeeds.Blog.allNeedsList)
        manage.code = 300
        manage.parent_code = 300
        manage.name = u'管理文章'

        lock = MangePermission(AccessNeeds.Blog.lockNeed)
        lock.code = 341
        lock.parent_code = 300
        lock.name = u'锁定文章'

        add = MangePermission(AccessNeeds.Blog.addNeed)
        add.code = 371
        add.parent_code = 300
        add.name = u'添加文章'

        edit = MangePermission(AccessNeeds.Blog.editNeed)
        edit.code = 372
        edit.parent_code = 300
        edit.name = u'编辑文章'

        delete = MangePermission(AccessNeeds.Blog.deleteNeed)
        delete.code = 373
        delete.parent_code = 300
        delete.name = u'删除文章'


checkPerms = AccessPerms()