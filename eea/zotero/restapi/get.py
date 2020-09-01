# -*- coding: utf-8 -*-
from eea.zotero.interfaces import IZoteroClientSettings
from plone import api
from plone.restapi.services import Service
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class ZoteroGet(Service):
    def __init__(self, context, request):
        super(ZoteroGet, self).__init__(context, request)

    def reply(self):
        return {
            "server": api.portal.get_registry_record("server", interface=IZoteroClientSettings, default=""),
            "password": api.portal.get_registry_record("password", interface=IZoteroClientSettings, default=""),
            "style": api.portal.get_registry_record("style", interface=IZoteroClientSettings, default=""),
        }
