#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Permission
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    权限管理模块

    :copyright: (c) 2015 by adousen.
"""
from functools import partial, wraps
from flask.signals import Namespace
from flask.ext.principal import IdentityContext, Permission, AnonymousIdentity, RoleNeed, namedtuple


__all__ = ['RoleNeeds', 'RolePerms', 'AccessNeeds', 'CodePerms']

user_no_permission_signal = Namespace().signal('no-permission')


class IdentityContextArgumentsError(ValueError):
    """ 参数值错误 """


class IdentityContextForManage(IdentityContext):
    """ 根据调用者的权限，生成对数据库对象进行管理操作的上下文环境，
        可以用作装饰器。
    """
    def __init__(self, permission, model_class=None, http_exception=None):
        self.model_class = model_class
        self.params_id = None
        super(IdentityContextForManage, self).__init__(permission, http_exception)

    def can(self):
        """ Whether the identity has access to the permission,
            Presently the system is base on permission code.
        """
        if self.params_id is not None:
            if self.model_class is None:
                raise IdentityContextArgumentsError()

            obj = self.model_class.query.get_by_id(self.params_id)

            if self.identity.can(self.permission):
                return True
            else:
                # 目前不存在一个操作需要多个权限码的情况，因此只循环一次
                for need in self.permission.needs:
                    if need.method == 'all':
                        # TODO: 查询need的子权限码是否全在self.identity.provides的列表中
                        pass
                    else:
                        if obj.permissions.can(need.method):
                            return True
                    return False

        return self.identity.can(self.permission)

    def __call__(self, fn):
        @wraps(fn)
        def _decorated(*args, **kw):
            target_id = kw["id"]
            self.params_id = target_id
            with self:
                rv = fn(*args, **kw)
            return rv
        return _decorated


class MangePermission(Permission):
    """ 管理操作的权限许可
    """
    def require(self, model_class=None, http_exception=None):
        """Represents needs, any of which must be present to access a resource

        :param model_class: 权限验证函数所在的类
        :param http_exception: 权限验证失败后的错误响应代码
        """
        return IdentityContextForManage(self, model_class, http_exception)

# Needs ：定义基于操作码的系统权限
ManageNeed = namedtuple('Manage', ['method', 'value'])


class PermissionEntity(object):
    """ 基于操作码的权限实体，与数据库的PermissionCode模型对应
    """
    def __init__(self, module, method, code, parent_code, name, description=''):
        self.module = module
        self.method = method
        self.code = code
        self.parent_code = parent_code
        self.name = name
        self.description = description
        self.permission = MangePermission(partial(ManageNeed, method)(code))

    def require(self, model_class=None, http_exception=None):
        return self.permission.require(model_class, http_exception)


class CodePerms(object):
    class User(object):
        ALL = PermissionEntity(module='User', method='all', code=100, parent_code=100, name='管理用户')
        ADD = PermissionEntity(module='User', method='add', code=101, parent_code=100, name='添加用户')
        DELETE = PermissionEntity(module='User', method='delete', code=102, parent_code=100, name='删除用户')
        LOCK = PermissionEntity(module='User', method='lock', code=141, parent_code=100, name='锁定用户')
        EDIT = PermissionEntity(module='User', method='edit', code=171, parent_code=100, name='编辑用户信息')

    class Blog(object):
        ALL = PermissionEntity(module='Blog', method='all', code=300, parent_code=300, name='管理文章')
        LOCK = PermissionEntity(module='Blog', method='lock', code=341, parent_code=300, name='锁定文章')
        ADD = PermissionEntity(module='Blog', method='add', code=371, parent_code=300, name='添加文章')
        EDIT = PermissionEntity(module='Blog', method='edit', code=372, parent_code=300, name='编辑文章')
        DELETE = PermissionEntity(module='Blog', method='delete', code=373, parent_code=300, name='删除文章')


# Need：定义基于角色的系统权限
class RoleNeeds(object):
    """ 与系统中的各个角色相对应的权限字段（need）
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
    # Ordinarily never assign this role to anyone !
    null = MangePermission(RoleNeed('null'))

checkPerms = CodePerms()