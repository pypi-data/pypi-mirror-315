# Copyright 2008 Canonical Ltd.  All rights reserved.
#
"""A class for storing resources where they can be seen by a template."""

__all__ = ["JSONRequestCache"]

from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces import IApplicationRequest

from lazr.restful.interfaces import LAZR_WEBSERVICE_NS, IJSONRequestCache


@implementer(IJSONRequestCache)
@adapter(IApplicationRequest)
class JSONRequestCache:
    """Default implementation for `IJSONRequestCache`."""

    LAZR_OBJECT_JSON_CACHE = "%s.object-json-cache" % LAZR_WEBSERVICE_NS
    LAZR_LINK_JSON_CACHE = "%s.link-json-cache" % LAZR_WEBSERVICE_NS

    def __init__(self, request):
        """Initialize with a request."""
        self.objects = request.annotations.setdefault(
            self.LAZR_OBJECT_JSON_CACHE, {}
        )

        self.links = request.annotations.setdefault(
            self.LAZR_LINK_JSON_CACHE, {}
        )
