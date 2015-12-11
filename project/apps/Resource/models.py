#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from werkzeug.utils import cached_property
from flask.ext.principal import UserNeed, Permission

from project import db
from project.mixins import ActiveRecordMixin
from project.permissions import RoleNeeds, RolePerms, CodePerms, ManageNeed

from ..account.models import User


class ResourceQuery(db.Query):
    pass


class Resource(db.Model, ActiveRecordMixin):
    query_class = ResourceQuery
    __tablename__ = 'resource'
    id = db.Column(db.INT, primary_key=True)
    author_id = db.Column(db.INT, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.NVARCHAR(50), nullable=False)
    subtitle = db.Column(db.NVARCHAR(50))
    category_id = db.Column(db.INT, db.ForeignKey('resource_category.id'))
    content = db.Column(db.TEXT, nullable=True)
    image_url = db.Column(db.NVARCHAR(255))
    create_time = db.Column(db.DATETIME, default=datetime.now())
    website = db.Column(db.NVARCHAR(255))
    github_url = db.Column(db.NVARCHAR(255))
    cn_doc_url = db.Column(db.NVARCHAR(255))
    en_doc_url = db.Column(db.NVARCHAR(255))

    #tag_list


class Category(db.Model, ActiveRecordMixin):
    __tablename__ = 'resource_category'
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.NVARCHAR(50))
    is_recommended = db.Column(db.BOOLEAN, default=False)


class TagToResource(db.Model, ActiveRecordMixin):
    __tablename__ = 'tag_to_resource'
    item_id = db.Column(db.INT, db.ForeignKey('resource.id'), primary_key=True)
    tag_id = db.Column(db.INT, db.ForeignKey('resource_tag.id'), primary_key=True)
    # TODO: 要保证没有重复的记录


class ResourceTag(db.Model, ActiveRecordMixin):
    __tablename__ = 'resource_tag'
    """标签实体类"""
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.NVARCHAR(50))
    creator_id = db.Column(db.INT, db.ForeignKey('user.id'))
    description = db.Column(db.TEXT)
    resources = db.relationship('Resource', secondary=TagToResource.__table__, query_class=ResourceQuery)






