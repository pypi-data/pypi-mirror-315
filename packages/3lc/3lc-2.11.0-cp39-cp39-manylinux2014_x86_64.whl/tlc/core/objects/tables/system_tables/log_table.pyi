import logging
from _typeshed import Incomplete
from tlc.core.object import Object as Object
from tlc.core.object_type_registry import ObjectTypeRegistry as ObjectTypeRegistry
from tlc.core.objects.table import Table as Table, TableRow as TableRow
from tlc.core.schema import DatetimeStringValue as DatetimeStringValue, Int32Value as Int32Value, MapElement as MapElement, Schema as Schema, StringValue as StringValue
from tlc.core.url import Scheme as Scheme, Url as Url
from tlc.core.url_adapters import ApiUrlAdapter as ApiUrlAdapter
from typing import Any, Callable

class LogTableHandler(logging.Handler):
    """Forwards log messages to the LogTable instance."""
    callback: Incomplete
    def __init__(self, callback: Callable[[logging.LogRecord], None]) -> None: ...
    def emit(self, record: logging.LogRecord) -> None: ...
    def set_formatter(self, formatter: logging.Formatter) -> None: ...

class _LogTableFilter(logging.Filter):
    """A specific filter to be used with the LogTable instance to exclude some log messages on the INFO level.

    The filter is intended to remove some object service log records that may otherwise overwhelm the LogTable.

    The LogTableFilter is initialized with a list of substrings. If any of these substrings are found in a log record
    with level=INFO, the filter will return False and the record will be suppressed, otherwise the logging will proceed
    as usual.
    Note that the filter will not suppress any log records that are not INFO.

    :param excludes: A list of substrings to be excluded from the log messages.
    """
    excludes: Incomplete
    def __init__(self, excludes: list[str]) -> None: ...
    def filter(self, record: logging.LogRecord) -> bool: ...

class LogTable(Table):
    """A table populated by the `logging` module, targeted for in-memory-only usage.

    A LogTable is a special Table that is populated by the logging system. It is not strictly immutable since it is
    continuously populated by the logging system. The LogTable will report fully defined when the schema is defined
    (like the base class) but will still evolve as logging events write new rows and bumps the `row_count`.

    Mostly the LogTable will be accessed through the singleton instance `LogTable.instance()`. This instance is created
    automatically when the module is loaded. The instance can be accessed by the URL `api://LogTable`.

    The LogTable global instance will filter some log messages that are generated by the object service.


    :param url: The URL of the table.
    :param init_parameters: The table initialization parameters.
    :param rotation_size: The number of rows to keep in memory before rotating the rows.
    :param loglevel: The initial logging level to use for the LogTable. Note that this may be changed later by external
        logging configuration.
    :param exclude: A list of substrings that if found in log records should filter out the log record.
    """
    log_table_instance: LogTable | None
    rotation_size: Incomplete
    exclude: Incomplete
    handler: Incomplete
    def __init__(self, url: Url | None = None, init_parameters: Any = None, rotation_size: int | None = None, loglevel: int | None = None, exclude: list[str] | None = None) -> None: ...
    @staticmethod
    def instance() -> LogTable:
        """
        Returns the singleton LogTable object
        """
    row_count: Incomplete
    def handle_log(self, record: logging.LogRecord) -> None: ...
    def write_to_url(self, force: bool = False) -> Url:
        """LogTable is an in-memory table not meant to be written to a URL.

        Override the base class to make it an no-op.
        """
    @property
    def counter(self) -> int: ...
