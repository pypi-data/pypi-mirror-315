CloudPayments Python Client Library (Asynchronous Fork)
======================================================

.. image:: https://img.shields.io/pypi/v/cloudpayments.svg
   :target: https://pypi.python.org/pypi/cloudpayments/
   :alt: Python Package Index

.. image:: https://img.shields.io/travis/car3ge/cloudpayments-python-client.svg
   :target: https://travis-ci.org/car3ge/cloudpayments-python-client
   :alt: Travis CI

Этот пакет — асинхронная версия клиента для платежного сервиса `CloudPayments <http://cloudpayments.ru/>`_. Он позволяет работать с `API CloudPayments <http://cloudpayments.ru/Docs/Api>`_ в асинхронном режиме с использованием библиотеки `aiohttp`.

Установка
=========

::

    pip install async-cloud-payments-fork

Требования
==========

Python 3.7+.

Использование
=============

.. code:: python

    from cloudpayments import CloudPayments

    client = CloudPayments('public_id', 'api_secret')
    await client.test()  # Важно использовать await для асинхронных методов

При создании клиента задаются аутентификационные параметры: Public ID и Api Secret. Оба этих значения можно получить в личном кабинете.

Обращение к API осуществляется через асинхронные методы клиента.


| **Тестовый метод** (`описание <https://cloudpayments.ru/wiki/integration/instrumenti/api#test>`__)

.. code:: python

    await client.test(request_id=None)

``request_id`` — идентификатор для `идемпотентного запроса <https://developers.cloudkassir.ru/#idempotentnost-api>`__.

В случае успеха возвращает строку с сообщением от сервиса.

(описание остальных методов остается без изменений)

Авторы
======

Разработано в `car3ge <https://github.com/car3ge>`_.
Асинхронная версия форк клиента CloudPayments для Python.
Пишите мне, если нужна консультация по работе с платежными системами: `sharashka.brk@gmail.com <sharashka.brk@gmail.com>`_.

Лицензия
========

MIT
