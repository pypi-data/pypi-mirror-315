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

import appier


class PaymentAPI(object):

    def generate_payment(
        self, amount, method="mb", currency="EUR", key=None, warning=None, cancel=None
    ):
        result = self.create_payment(amount, method=method, currency=currency, key=key)
        status = result.get("status", "error")
        if not status == "ok":
            raise appier.OperationalError("Problem creating payment")
        method = dict(result["method"])
        method["identifier"] = result["id"]
        method["amount"] = amount
        method["currency"] = currency
        method["warning"] = warning
        method["cancel"] = cancel
        self.set_payment(method)
        return method

    def list_payments(self, *args, **kwargs):
        url = self.base_url + "single"
        return self.get(url, *args, **kwargs)

    def create_payment(self, amount, method="mb", currency="EUR", key=None):
        url = self.base_url + "single"
        return self.post(
            url, data_j=dict(value=amount, method=method, currency=currency, key=key)
        )

    def get_payment(self, id):
        url = self.base_url + "single/%s" % id
        return self.get(url)

    def update_payment(self, currency=None, key=None):
        url = self.base_url + "single/%s" % id
        data_j = dict()
        if not currency == None:
            data_j["currency"] = currency
        if not key == None:
            data_j["key"] = key
        return self.post(url, data_j=data_j)

    def delete_payment(self, id):
        url = self.base_url + "single/%s" % id
        return self.delete(url)

    def warn_payment(self, id):
        self.logger.debug("Warning Payment (id := %s)" % id)
        payment = self.get_payment(id)
        if not payment:
            self.logger.warning("No payment found for identifier to warn")
            return
        warned = payment.get("warned", False)
        if warned:
            return
        payment["warned"] = True
        self.set_reference(payment)
        self.trigger("warned", payment)

    def cancel_mb(self, id, force=True):
        self.logger.debug("Canceling Payment (id := %s)" % id)
        payment = self.get_payment(id)
        if not payment:
            self.logger.warning("No payment found for identifier to cancel")
            return
        try:
            self.cancel_payment(id)
        except Exception:
            if not force:
                raise
            self.logger.warning("Problem while canceling payment, ignoring")
        self.delete_payment(id)
        self.del_payment(id)
        self.trigger("canceled", payment)

    def mark_payment(self, id):
        self.logger.debug("Marking payment (id := %s)" % id)
        payment = self.get_payment(id)
        if not payment:
            self.logger.warning("No payment found for identifier to mark")
            return
        self.trigger("paid", payment)
        self.trigger("marked", payment)
        self.del_payment(id)

    def notify_payment(self, data):
        type, status = data["type"], data["status"]
        if type == "capture" and status == "success":
            self.mark_payment(data["id"])
