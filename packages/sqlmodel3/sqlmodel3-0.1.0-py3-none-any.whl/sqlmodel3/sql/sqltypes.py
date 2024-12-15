from typing import Any, cast

from sqlalchemy3 import types
from sqlalchemy3.engine.interfaces import Dialect


class AutoString(types.TypeDecorator):  # type: ignore
    impl = types.String
    cache_ok = True
    mysql_default_length = 255

    def load_dialect_impl(self, dialect: Dialect) -> "types.TypeEngine[Any]":
        impl = cast(types.String, self.impl)
        if impl.length is None and dialect.name == "mysql":
            return dialect.type_descriptor(types.String(self.mysql_default_length))
        return super().load_dialect_impl(dialect)
