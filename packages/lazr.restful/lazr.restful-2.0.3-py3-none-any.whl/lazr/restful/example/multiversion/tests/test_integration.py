# Copyright 2008 Canonical Ltd.  All rights reserved.

"""Test harness for doctests for lazr.restful multiversion example service."""

__all__ = []

import doctest
import os

from pkg_resources import resource_filename
from van.testing.layer import wsgi_intercept_layer, zcml_layer
from zope.component import getUtility

from lazr.restful.example.multiversion.root import (
    MultiversionWebServiceRootResource,
)
from lazr.restful.interfaces import IWebServiceConfiguration
from lazr.restful.simple import Publication
from lazr.restful.testing.webservice import WebServiceApplication

DOCTEST_FLAGS = (
    doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_NDIFF
)


class FunctionalLayer:
    zcml = os.path.abspath(
        resource_filename("lazr.restful.example.multiversion", "site.zcml")
    )


zcml_layer(FunctionalLayer)


class WSGILayer(FunctionalLayer):
    @classmethod
    def make_application(self):
        getUtility(IWebServiceConfiguration).hostname = "multiversion.dev"
        getUtility(IWebServiceConfiguration).port = None
        root = MultiversionWebServiceRootResource()
        return WebServiceApplication(root, Publication)


wsgi_intercept_layer(WSGILayer)


def load_tests(loader, tests, pattern):
    """See `zope.testing.testrunner`."""
    doctest_files = sorted(
        name
        for name in os.listdir(os.path.dirname(__file__))
        if name.endswith(".txt")
    )
    suite = doctest.DocFileSuite(*doctest_files, optionflags=DOCTEST_FLAGS)
    suite.layer = WSGILayer
    tests.addTest(suite)
    return tests
