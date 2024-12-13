import tlc
from _typeshed import Incomplete
from tlc.core.schema import Schema as Schema
from tlcsaas.transaction import Transaction as Transaction
from typing import Generic, Protocol, TypeVar

class HasTransaction(Protocol):
    schema: Schema
    transaction_id: str
    url: tlc.Url
T = TypeVar('T', bound=HasTransaction)

class TransactionCloser(Generic[T]):
    resource: Incomplete
    transaction: Incomplete
    transaction_type: Incomplete
    def __init__(self, resource: T, transaction_type: str) -> None: ...
    def __enter__(self) -> T: ...
    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None: ...
