#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Easypay API
# Copyright (c) 2008-2024 Hive Solutions Lda.
#
# This file is part of Hive Easypay API.
#
# Hive Easypay API is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Easypay API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Easypay API. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__copyright__ = "Copyright (c) 2008-2024 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import time
import uuid
import shelve
import threading
import traceback

import xml.dom.minidom
import xml.etree.ElementTree

import appier

from . import mb
from . import errors
from . import payment

LOOP_TIMEOUT = 60.0
""" The timeout to be used between tick intervals for
the scheduler to process the various pending documents
and requests for detailed information """

BASE_URL = "https://www.easypay.pt/_s/"
""" The default base URL to be used for a production
based environment, should be used carefully """

BASE_URL_TEST = "http://test.easypay.pt/_s/"
""" The base URL for the sandbox endpoint, this is used
for testing purposes only and the password is sent using
a non encrypted model (no protection provided) """

BASE_URL_V2 = "https://api.prod.easypay.pt/2.0/"
""" The base URL for API V2 for the production environment, this is the
URL that should be used for production purposes """

BASE_URL_TEST_V2 = "https://api.test.easypay.pt/2.0/"
""" The base URL for API V2 for the test environment, this is the URL
that should be used for testing purposes """


class Scheduler(threading.Thread):
    """
    Scheduler thread that is used to poll the remote Easypay
    server for the detailed information on the document and
    then notify the final API client about the new information.
    """

    def __init__(
        self,
        api,
        loop_timeout=LOOP_TIMEOUT,
        tick_docs=True,
        tick_references=True,
        tick_payments=True,
    ):
        threading.Thread.__init__(self)
        self.api = api
        self.loop_timeout = loop_timeout
        self.tick_docs = tick_docs
        self.tick_references = tick_references
        self.tick_payments = tick_payments
        self.daemon = True

    def run(self):
        self.running = True
        while self.running:
            try:
                self.tick()
            except Exception as exception:
                self.api.logger.critical("Unhandled Easypay exception raised")
                self.api.logger.error(exception)
                lines = traceback.format_exc().splitlines()
                for line in lines:
                    self.api.logger.warning(line)
            time.sleep(self.loop_timeout)

    def stop(self):
        self.running = False

    def tick(self):
        """
        Runs one tick operation, meaning that all the pending
        documents will be retrieved and a tentative will be made to
        retrieve the detailed information on them.

        It's during this tick operation that the warning and cancel
        operations are performed on the references.
        """

        if self.tick_docs:
            self._tick_docs()
        if self.tick_references:
            self._tick_references()
        if self.tick_payments:
            self._tick_payments()

    def _tick_docs(self):
        docs = self.api.list_docs()
        for doc in docs:
            try:
                identifier = doc["identifier"]
                details = self.api.details_mb(identifier)
                self.api.mark_mb(details)
            except Exception as exception:
                self.api.logger.critical(
                    "Problem handling document: '%s'" % doc.get("identifier", "unknown")
                )
                self.api.logger.error(exception)
                lines = traceback.format_exc().splitlines()
                for line in lines:
                    self.api.logger.warning(line)

    def _tick_references(self):
        references = self.api.list_references()
        references.sort(key=lambda v: v.get("cancel", 0) or 0, reverse=True)
        for reference in references:
            try:
                current = time.time()
                identifier = reference["identifier"]
                warning = reference.get("warning", None)
                cancel = reference.get("cancel", None)
                warned = reference.get("warned", False)
                if warning and current > warning and not warned:
                    self.api.warn_mb(identifier)
                if cancel and current > cancel:
                    self.api.cancel_mb(identifier)
            except Exception as exception:
                self.api.logger.critical(
                    "Problem handling reference: '%s'"
                    % reference.get("identifier", "unknown")
                )
                self.api.logger.error(exception)
                lines = traceback.format_exc().splitlines()
                for line in lines:
                    self.api.logger.warning(line)

    def _tick_payments(self):
        payments = self.api.list_payments()
        payments.sort(key=lambda v: v.get("cancel", 0) or 0, reverse=True)
        for payment in payments:
            try:
                current = time.time()
                identifier = payment["identifier"]
                warning = payment.get("warning", None)
                cancel = payment.get("cancel", None)
                warned = payment.get("warned", False)
                if warning and current > warning and not warned:
                    self.api.warn_mb(identifier)
                if cancel and current > cancel:
                    self.api.cancel_mb(identifier)
            except Exception as exception:
                self.api.logger.critical(
                    "Problem handling payment: '%s'"
                    % payment.get("identifier", "unknown")
                )
                self.api.logger.error(exception)
                lines = traceback.format_exc().splitlines()
                for line in lines:
                    self.api.logger.warning(line)


class API(appier.API, mb.MBAPI):
    """
    Top level entry point for the Easypay API services,
    should provide the abstract implementations for the
    services offered by Easypay.

    Concrete implementations of this API should provide
    other storage options that should include persistence.
    """

    def __init__(self, *args, **kwargs):
        appier.API.__init__(self, *args, **kwargs)
        self.production = appier.conf("EASYPAY_PRODUCTION", False, cast=bool)
        self.username = appier.conf("EASYPAY_USERNAME", None)
        self.password = appier.conf("EASYPAY_PASSWORD", None)
        self.cin = appier.conf("EASYPAY_CIN", None)
        self.entity = appier.conf("EASYPAY_ENTITY", None)
        self.production = kwargs.get("production", self.production)
        self.username = kwargs.get("username", self.username)
        self.password = kwargs.get("password", self.password)
        self.cin = kwargs.get("cin", self.cin)
        self.entity = kwargs.get("entity", self.entity)
        self.base_url = BASE_URL if self.production else BASE_URL_TEST
        self.counter = 0
        self.references = dict()
        self.docs = dict()
        self.lock = threading.RLock()
        self.scheduler = Scheduler(
            self, tick_docs=True, tick_references=True, tick_payments=False
        )

    @classmethod
    def cleanup(cls, *args, **kwargs):
        singleton = cls.singleton(*args, **kwargs)
        singleton.destroy()

    def destroy(self):
        appier.API.destroy(self)
        self.stop_scheduler()

    def start_scheduler(self):
        if self.scheduler.is_alive():
            return
        self.scheduler.start()

    def stop_scheduler(self):
        if not self.scheduler.is_alive():
            return
        self.scheduler.stop()

    def request(self, method, *args, **kwargs):
        result = method(*args, **kwargs)
        result = self.loads(result)
        status = result.get("ep_status", "err1")
        message = result.get("ep_message", "no message defined")
        if not status == "ok0":
            raise errors.APIError(message)
        return result

    def build(
        self,
        method,
        url,
        data=None,
        data_j=None,
        data_m=None,
        headers=None,
        params=None,
        mime=None,
        kwargs=None,
    ):
        appier.API.build(self, method, url, headers, kwargs)
        if self.cin:
            kwargs["ep_cin"] = self.cin
        if self.username:
            kwargs["ep_user"] = self.username

    def diagnostics(self):
        return dict(references=self.list_references(), docs=self.list_docs())

    def gen_reference(self, data, warning=None, cancel=None):
        cin = data["ep_cin"]
        username = data["ep_user"]
        entity = data["ep_entity"]
        reference = data["ep_reference"]
        value = data["ep_value"]
        identifier = data["t_key"]
        reference = dict(
            cin=cin,
            username=username,
            entity=entity,
            reference=reference,
            value=value,
            identifier=identifier,
            warning=warning,
            cancel=cancel,
            status="pending",
        )
        self.new_reference(reference)
        return reference

    def gen_doc(self, identifier, key):
        doc = dict(cin=self.cin, username=self.username, identifier=identifier, key=key)
        self.new_doc(doc)
        return doc

    def new_reference(self, reference):
        self.set_reference(reference)

    def set_reference(self, reference):
        identifier = reference["identifier"]
        self.references[identifier] = reference

    def del_reference(self, identifier):
        del self.references[identifier]

    def list_references(self):
        references = self.references.values()
        return appier.legacy.eager(references)

    def get_reference(self, identifier):
        return self.references.get(identifier, None)

    def new_doc(self, doc):
        identifier = doc["identifier"]
        self.docs[identifier] = doc

    def del_doc(self, identifier):
        del self.docs[identifier]

    def list_docs(self):
        docs = self.docs.values()
        return appier.legacy.eager(docs)

    def get_doc(self, identifier):
        return self.docs.get(identifier, None)

    def next(self):
        self.lock.acquire()
        try:
            self.counter += 1
            next = self.counter
        finally:
            self.lock.release()
        return next

    def generate(self):
        identifier = str(uuid.uuid4())
        return identifier

    def validate(self, cin=None, username=None):
        if cin and not cin == self.cin:
            raise errors.SecurityError("invalid cin")
        if username and not username == self.username:
            raise errors.SecurityError("invalid username")

    def loads(self, data):
        result = dict()
        document = xml.dom.minidom.parseString(data)
        base = document.childNodes[0]
        for node in base.childNodes:
            name = node.nodeName
            value = self._text(node)
            if value == None:
                continue
            result[name] = value
        return result

    def dumps(self, map, root="getautoMB_detail", encoding="utf-8"):
        root = xml.etree.ElementTree.Element(root)
        for name, value in map.items():
            value = value if type(value) in appier.legacy.STRINGS else str(value)
            child = xml.etree.ElementTree.SubElement(root, name)
            child.text = value
        result = xml.etree.ElementTree.tostring(root, encoding=encoding, method="xml")
        header = appier.legacy.bytes('<?xml version="1.0" encoding="%s"?>' % encoding)
        result = header + result
        return result

    def _text(self, node):
        if not node.childNodes:
            return None
        return node.childNodes[0].nodeValue


class ShelveAPI(API):
    """
    Shelve API based infra-structure, that provides a storage
    engine based for secondary storage persistence. This class
    should be used only as a fallback storage as the performance
    is considered poor, due to large overhead in persistence.
    """

    def __init__(self, *args, **kwargs):
        API.__init__(self, *args, **kwargs)
        self.path = appier.conf("EASYPAY_PATH", "easypay.shelve")
        self.path = kwargs.get("path", self.path)
        base_path = os.path.dirname(self.path)
        exists = not base_path or os.path.exists(base_path)
        if not exists:
            os.makedirs(base_path)
        self.shelve = shelve.open(self.path, protocol=2, writeback=True)

    def destroy(self):
        API.destroy(self)
        if self.shelve:
            self.shelve.close()
        self.shelve = None

    def set_reference(self, reference):
        identifier = reference["identifier"]
        self.lock.acquire()
        try:
            references = self.shelve.get("references", {})
            references[identifier] = reference
            self.shelve["references"] = references
            self.shelve.sync()
        finally:
            self.lock.release()

    def del_reference(self, identifier):
        self.lock.acquire()
        try:
            references = self.shelve.get("references", {})
            del references[identifier]
            self.shelve["references"] = references
            self.shelve.sync()
        finally:
            self.lock.release()

    def list_references(self):
        self.lock.acquire()
        try:
            references = self.shelve.get("references", {})
            references = references.values()
            references = appier.legacy.eager(references)
        finally:
            self.lock.release()
        return references

    def get_reference(self, identifier):
        self.lock.acquire()
        try:
            references = self.shelve.get("references", {})
            reference = references.get(identifier, None)
        finally:
            self.lock.release()
        return reference

    def new_doc(self, doc):
        identifier = doc["identifier"]
        self.lock.acquire()
        try:
            docs = self.shelve.get("docs", {})
            docs[identifier] = doc
            self.shelve["docs"] = docs
            self.shelve.sync()
        finally:
            self.lock.release()

    def del_doc(self, identifier):
        self.lock.acquire()
        try:
            docs = self.shelve.get("docs", {})
            del docs[identifier]
            self.shelve["docs"] = docs
            self.shelve.sync()
        finally:
            self.lock.release()

    def list_docs(self):
        self.lock.acquire()
        try:
            docs = self.shelve.get("docs", {})
            docs = docs.values()
            docs = appier.legacy.eager(docs)
        finally:
            self.lock.release()
        return docs

    def get_doc(self, identifier):
        self.lock.acquire()
        try:
            docs = self.shelve.get("docs", {})
            doc = docs.get(identifier, None)
        finally:
            self.lock.release()
        return doc

    def next(self):
        self.lock.acquire()
        try:
            counter = self.shelve.get("counter", 0)
            counter += 1
            next = counter
            self.shelve["counter"] = counter
            self.shelve.sync()
        finally:
            self.lock.release()
        return next


class APIv2(appier.API, payment.PaymentAPI):
    """
    Top level entry point for the Easypay API 2.0 services,
    should provide the abstract implementations for the
    services offered by Easypay using the 2.0 version of the API
    """

    def __init__(self, *args, **kwargs):
        appier.API.__init__(self, *args, **kwargs)
        self.production = appier.conf("EASYPAY_PRODUCTION", False, cast=bool)
        self.account_id = appier.conf("EASYPAY_ACCOUNT_ID", None)
        self.key = appier.conf("EASYPAY_KEY", None)
        self.production = kwargs.get("production", self.production)
        self.account_id = kwargs.get("account_id", self.account_id)
        self.key = kwargs.get("key", self.key)
        self.base_url = BASE_URL_V2 if self.production else BASE_URL_TEST_V2
        self.payments = dict()
        self.lock = threading.RLock()
        self.scheduler = Scheduler(
            self, tick_docs=False, tick_references=False, tick_payments=True
        )

    @classmethod
    def cleanup(cls, *args, **kwargs):
        singleton = cls.singleton(*args, **kwargs)
        singleton.destroy()

    def destroy(self):
        appier.API.destroy(self)
        self.stop_scheduler()

    def start_scheduler(self):
        if self.scheduler.is_alive():
            return
        self.scheduler.start()

    def stop_scheduler(self):
        if not self.scheduler.is_alive():
            return
        self.scheduler.stop()

    def build(
        self,
        method,
        url,
        data=None,
        data_j=None,
        data_m=None,
        headers=None,
        params=None,
        mime=None,
        kwargs=None,
    ):
        appier.API.build(self, method, url, headers, kwargs)
        if self.account_id:
            headers["AccountId"] = self.account_id
        if self.key:
            headers["ApiKey"] = self.key

    def diagnostics(self):
        return dict(payments=self.list_payments())

    def list_payments(self):
        payments = self.payments.values()
        return appier.legacy.eager(payments)


class ShelveAPIv2(APIv2):
    """
    Shelve API 2.0 based infra-structure, that provides a storage
    engine based for secondary storage persistence. This class
    should be used only as a fallback storage as the performance
    is considered poor, due to large overhead in persistence.
    """

    def __init__(self, *args, **kwargs):
        APIv2.__init__(self, *args, **kwargs)
        self.path = appier.conf("EASYPAY_PATH", "easypay.shelve")
        self.path = kwargs.get("path", self.path)
        base_path = os.path.dirname(self.path)
        exists = not base_path or os.path.exists(base_path)
        if not exists:
            os.makedirs(base_path)
        self.shelve = shelve.open(self.path, protocol=2, writeback=True)

    def destroy(self):
        APIv2.destroy(self)
        if self.shelve:
            self.shelve.close()
        self.shelve = None

    def set_payment(self, payment):
        identifier = payment["identifier"]
        self.lock.acquire()
        try:
            payments = self.shelve.get("payments", {})
            payments[identifier] = payment
            self.shelve["payments"] = payments
            self.shelve.sync()
        finally:
            self.lock.release()

    def del_payment(self, identifier):
        self.lock.acquire()
        try:
            payments = self.shelve.get("payments", {})
            del payments[identifier]
            self.shelve["payments"] = payments
            self.shelve.sync()
        finally:
            self.lock.release()

    def list_payments(self):
        self.lock.acquire()
        try:
            payments = self.shelve.get("payments", {})
            payments = payments.values()
            payments = appier.legacy.eager(payments)
        finally:
            self.lock.release()
        return payments

    def get_payment(self, identifier):
        self.lock.acquire()
        try:
            payments = self.shelve.get("payments", {})
            payment = payments.get(identifier, None)
        finally:
            self.lock.release()
        return payment
