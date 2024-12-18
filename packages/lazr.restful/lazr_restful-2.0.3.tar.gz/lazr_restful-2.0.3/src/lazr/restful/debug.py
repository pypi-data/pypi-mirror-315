# Copyright 2008 Canonical Ltd.  All rights reserved.

"""Module docstring goes here."""

__all__ = ["debug_proxy", "typename"]

from io import StringIO

import zope.proxy
from zope.security.checker import Checker, CheckerPublic, Proxy, getChecker


def typename(obj):
    """Return the typename of an object."""
    t = type(obj)
    if t.__module__ in {"__builtin__", "builtins"}:
        return t.__name__
    else:
        return "{}.{}".format(t.__module__, t.__name__)


def default_proxy_formatter(proxy):
    """Formatter that simply returns the proxy's type name."""
    return typename(proxy)


def get_permission_mapping(checker):
    """Return a list of (permission, list of protected names) for the checker.

    Permission used to check for attribute setting have (set) appended.
    """
    permission_to_names = {}
    for name, permission in checker.get_permissions.items():
        if permission is CheckerPublic:
            permission = "public"
        permission_to_names.setdefault(permission, []).append(name)
    for name, permission in checker.set_permissions.items():
        if permission is CheckerPublic:
            permission = "public"
        set_permission = "%s (set)" % permission
        permission_to_names.setdefault(set_permission, []).append(name)
    return sorted(
        (permission, sorted(names))
        for permission, names in permission_to_names.items()
    )


def security_proxy_formatter(proxy):
    """Return informative text about the checker used by the proxy."""
    checker = getChecker(proxy)
    output = ["{} (using {})".format(typename(proxy), typename(checker))]
    if type(checker) is Checker:
        for permission, names in get_permission_mapping(checker):
            output.append(
                "{}: {}".format(permission, ", ".join(sorted(names)))
            )
    return "\n    ".join(output)


proxy_formatters = {Proxy: security_proxy_formatter}


def debug_proxy(obj):
    """Return informative text about the proxies wrapping obj.

    Usually used like print(debug_proxy(obj)).
    """
    if not zope.proxy.isProxy(obj):
        return "%r doesn't have any proxies." % obj
    buf = StringIO()
    for proxy in zope.proxy.ProxyIterator(obj):
        if not zope.proxy.isProxy(proxy):
            break
        printer = proxy_formatters.get(type(proxy), default_proxy_formatter)
        print(printer(proxy), file=buf)
    return buf.getvalue()
