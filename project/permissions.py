#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'adousen'

__all__ = ['RoleNeeds', 'RolePerms', 'AccessNeeds', 'AccessPerms']

from functools import partial, wraps
from werkzeug.utils import cached_property
from flask import abort, g
from flask.ext.principal import Principal, Identity, IdentityContext, \
    Permission, AnonymousIdentity, identity_changed, identity_loaded, \
    UserNeed, RoleNeed, ActionNeed, PermissionDenied, Need, namedtuple


class IdentityContextArgumentsError(ValueError):
    """ 参数值错误 """


class IdentityContextForManage(IdentityContext):
    """ 根据调用者的权限，生成对数据库对象进行管理操作的上下文环境，
        可以用作装饰器。
    """
    def __init__(self, permission, cls=None, http_exception=None):
        self.cls = cls
        self.target_id = None
        super(IdentityContextForManage, self).__init__(permission, http_exception)

    def can(self):
        """Whether the identity has access to the permission
        """
        if self.target_id is not None:
            if self.cls is None:
                raise IdentityContextArgumentsError()

            obj = self.cls.query.get_by_id(self.target_id)

            # 循环测试
            retval = True
            for need in self.permission.needs:
                if need.method == "edit" and obj.permissions.edit:
                    retval = True and retval

                elif need.method == "delete" and obj.permissions.delete:
                    retval = True and retval

                elif need.method == "role":
                    if need.value == "admin" and obj.permissions.admin:  # need.group
                        retval = True and retval
                    else:
                        return False
                else:
                    return False

                # TODO: 继续添加其他管理操作
            return retval

        return self.identity.can(self.permission)

    def __call__(self, fn):
        @wraps(fn)
        def _decorated(*args, **kw):
            target_id = kw["id"]
            self.target_id = target_id
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


# Need：定义系统中的各个权限字段
# Permission：定义系统中的各个权限组
class RoleNeeds(object):
    """与系统中的各个角色相对应的权限字段（need）
    """

    auth = RoleNeed('auth')
    moderator = RoleNeed('moderator')
    admin = RoleNeed('admin')
    superuser = RoleNeed('superuser')


# Permissions：根据权限许可定义相应的系统角色
class RolePerms(object):
    """
    与系统中的各个角色相对应的权限组（permission）
    """
    auth = MangePermission(RoleNeeds.auth)
    auth.permissions = '1'
    auth.name = "Auth"
    auth.group = -1
    auth.default = True

    moderator = MangePermission(RoleNeeds.moderator)
    moderator.permissions = '2'
    moderator.name = "Moderator"
    moderator.group = -1
    moderator.default = False

    admin = MangePermission(RoleNeeds.admin)
    admin.permissions = '3'
    admin.name = "Admin"
    admin.group = -1
    admin.default = False

    superuser = MangePermission(RoleNeeds.superuser)
    superuser.permissions = '4'
    superuser.name = "Superuser"
    superuser.group = -1
    superuser.default = False

    # this is assigned when you want to block a permission to all
    # never assign this role to anyone !
    null = MangePermission(RoleNeed('null'))


ManageNeed = namedtuple('Manage', ['method', 'group'])

EditNeed = partial(ManageNeed, 'edit')
LockNeed = partial(ManageNeed, 'lock')
DeleteNeed = partial(ManageNeed, 'delete')
AddNeed = partial(ManageNeed, 'add')


# Needs ：定义基于操作的权限字段
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
    各系统操作对应的permission
    """
    class User(object):
        manage = MangePermission(*AccessNeeds.User.allNeedsList)
        manage.code = 200
        manage.name = u'管理用户'

        edit = MangePermission(AccessNeeds.User.editNeed)
        edit.code = 201
        edit.name = u'编辑用户信息'

        add = MangePermission(AccessNeeds.User.addNeed)
        add.code = 202
        add.name = u'添加用户'

        lock = MangePermission(AccessNeeds.User.lockNeed)
        lock.code = 203
        lock.name = u'锁定用户'

        delete = MangePermission(AccessNeeds.User.deleteNeed)
        delete.code = 204
        delete.name = u'删除用户'

    class Blog(object):
        manage = MangePermission(*AccessNeeds.Blog.allNeedsList)
        manage.code = 300
        manage.name = u'管理博客文章'

        add = MangePermission(AccessNeeds.Blog.editNeed)
        add.code = 301
        add.name = u'添加文章'

        edit = MangePermission(AccessNeeds.Blog.editNeed)
        edit.code = 302
        edit.name = u'编辑文章'

        lock = MangePermission(AccessNeeds.Blog.lockNeed)
        lock.code = 303
        lock.name = u'锁定文章'

        delete = MangePermission(AccessNeeds.Blog.deleteNeed)
        delete.code = 304
        delete.name = u'删除文章'


checkPerms = AccessPerms()