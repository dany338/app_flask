"""This module has everythings to setup Solr database."""
# -*- coding: utf-8 -*-
# !/usr/bin/env python
import pysolr

# Caching constants.
TAG = "(DATABASE)"

SOLR_TIMEOUT = 10
SOLR_HOST = "http://solr"
SOLR_PORT = ":8983"
# Index core:
SOLR_CORE = "/solr/core_sig_tools"
# URL solr
SOLR_PATH = SOLR_HOST + SOLR_PORT + SOLR_CORE

MAX_RESULT = 100


def inserts(collection):
    """Recieve an a collection of wms model."""
    # Solr instance.
    solr = pysolr.Solr(SOLR_PATH, timeout=SOLR_TIMEOUT)
    solr.add(collection)


def search(keywords):
    """Recive an a collection of wms model."""
    # Solr instance.
    try:
        solr = pysolr.Solr(SOLR_PATH, timeout=SOLR_TIMEOUT)
        res = solr.search(q='%s' % (keywords or '*'), rows=100)
        # res = solr.search(q='layertitle:*%s*' % (keywords))
        return list(res)
    except Exception as e:
        print e.message
        return []


def getRecord(code):
    """
    Return a fresh queryset of wms model.

    :param int code: id of wms
    :return:
    :rtype: ModelQuerySet
    """
    solr = pysolr.Solr(SOLR_PATH, timeout=SOLR_TIMEOUT)
    res = solr.search(q='code:' + code)
    if not res:
        raise Exception("WMS Does't exist in database")
    return list(res)


def getAllrecords():
    """
    Get all wms from database. If there isn't wms return a empty array.

    :return:    `WMS list`
                `empty` otherwise.
    :rtype: list.
    """
    solr = pysolr.Solr(SOLR_PATH, timeout=SOLR_TIMEOUT)
    res = solr.search("*:*")
    return list(res)


def removeAllrecords():
    """Remove all records."""
    print TAG, "Start to clean documents..."
    # Solr instance.
    solr = pysolr.Solr(SOLR_PATH, timeout=SOLR_TIMEOUT)
    res = solr.delete(q='*:*')
    print TAG, "Finish clean documents..."
    return list(res)
