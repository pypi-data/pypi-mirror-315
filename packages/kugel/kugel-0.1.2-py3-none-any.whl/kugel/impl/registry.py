"""
Data domain registry of resources and tables, independent of configuration file format.
This is Kugel's global state outside the SQLite database.
"""

from typing import Type

from pydantic import BaseModel

from .utils import fail

_DOMAINS = {}


def domain(name: str):
    def wrap(cls):
        add_domain(name, cls)
        return cls
    return wrap


def table(**kwargs):
    def wrap(cls):
        add_table(cls, **kwargs)
        return cls
    return wrap


class TableDef(BaseModel):
    """
    Capture a table definition from the @table decorator, example:
        @table(domain="kubernetes", name="pods", resource="pods")
    """
    cls: Type
    name: str
    domain: str
    resource: str


class Domain(BaseModel):
    """
    Capture a domain definition from the @domain decorator, example:
        @domain("kubernetes")
    """
    cls: Type
    tables: dict[str, TableDef] = {}


def add_domain(name: str, cls: Type):
    """Register a class to implement a data domain; this is called by the @domain decorator."""
    _DOMAINS[name] = Domain(cls=cls)


def get_domain(name: str) -> Domain:
    return _DOMAINS[name]


def add_table(cls, **kwargs):
    """Register a class to define a table; this is called by the @table decorator."""
    t = TableDef(cls=cls, **kwargs)
    if t.domain not in _DOMAINS:
        fail(f"Must create domain {t.domain} before table {t.domain}.{t.name}")
    _DOMAINS[t.domain].tables[t.name] = t