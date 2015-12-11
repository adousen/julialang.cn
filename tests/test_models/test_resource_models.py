#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    tests.test_models.test_resource
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    测试resource.models模块

    :copyright: (c) 2015 by adousen.
"""
from tests.base import BaseTestCase

from project.apps.resource.models import Resource, Category, TagToResource, ResourceTag


class CategoryModelTests(BaseTestCase):
    @staticmethod
    def init_record_to_table():
        category = Category()
        category.name = u'语言基础'
        category.is_recommended = True
        category.save()

    def test_save_new(self):
        CategoryModelTests.init_record_to_table()
        self.assertIsNotNone(Category.query.filter_by(name=u'语言基础').first())


class ResourceModelTests(BaseTestCase):
    def setUp(self):
        super(self.__class__, self).setUp()

    @staticmethod
    def init_record_to_table(category_id=1):
        """init a Resource record to database"""
        CategoryModelTests.init_record_to_table()

        res = Resource()
        res.author_id = 1
        res.title = u'test入门'
        res.subtitle = u'test入门教程'
        res.category_id = category_id
        res.content = u'test程序用于测试入门教程的内容'
        res.github_url = u'https://github.com/adousen/julialang.cn'
        res.save()

    def test_save_new(self):
        self.init_record_to_table()
        self.assertIsNotNone(Resource.query.filter_by(title=u'test入门').first())


class ResourceTagModelTests(BaseTestCase):
    @staticmethod
    def init_record_to_table():
        ResourceModelTests.init_record_to_table()
        tag = ResourceTag()
        tag.name = u'语言'
        tag.creator_id = 1
        tag.save()

    def test_save_new(self):
        ResourceTagModelTests.init_record_to_table()
        self.assertIsNotNone(ResourceTag.query.filter_by(name=u'语言').first())

    def test_get_a_resource_list_by_tag_id(self):
        TagToResourceModelTests.init_record_to_table()
        self.assertGreaterEqual(len(ResourceTag.query.filter_by(id=1).first().resources), 1)


class TagToResourceModelTests(BaseTestCase):
    @staticmethod
    def init_record_to_table():

        ResourceTagModelTests.init_record_to_table()
        tag_resource = TagToResource()
        tag_resource.item_id = 1
        tag_resource.tag_id = 1
        tag_resource.save()

    def test_save_new(self):
        TagToResourceModelTests.init_record_to_table()
        self.assertIsNotNone(TagToResource.query.filter_by(item_id=1).first())




