import pyarrow as pa
from _typeshed import Incomplete
from collections.abc import Iterable, Iterator
from tlc.core.url import Url as Url
from torch.utils.data import Dataset as Dataset
from torch.utils.data.sampler import Sampler
from typing import Any, Callable, Generator

def bytes2str(obj: bytes) -> str: ...
def str2bytes(s: str) -> bytes: ...
def take(iterator: Iterator, batch_size: int) -> list: ...
def batched_iterator(iterator: Iterable, batch_size: int) -> Iterator[list]: ...

class SubsetSequentialSampler(Sampler[int]):
    """Samples elements sequentially from a given list of indices."""
    indices: Incomplete
    def __init__(self, indices: list[int]) -> None: ...
    def __iter__(self) -> Iterator[int]: ...
    def __len__(self) -> int: ...

class RangeSampler(Sampler[int]):
    """Samples elements sequentially from a range"""
    end: Incomplete
    start: Incomplete
    step: Incomplete
    def __init__(self, end: int, start: int = 0, step: int = 1) -> None: ...
    def __iter__(self) -> Iterator[int]: ...
    def __len__(self) -> int: ...

class RepeatByWeightSampler(Sampler[int]):
    """Repeats elements based on their weight."""
    indices: Incomplete
    def __init__(self, weights: list[float], shuffle: bool = True) -> None: ...
    def __iter__(self) -> Iterator[int]: ...
    def __len__(self) -> int: ...

def without_transforms(dataset: Dataset) -> Generator[Callable | None, None, None]:
    """Ensures that, if the dataset is a Torchvision dataset, its transforms are temporarily removed.

    :param dataset: The dataset to temporarily remove transforms from.
    """
def relativize_with_max_depth(url: Url, owner: Url, max_depth: int) -> Url:
    """Relativize the given URL with respect to the given owner URL, up to a maximum depth.

    Deprecated: Use `Url.to_relative_with_max_depth` instead.
    """
def standardized_transforms(transforms: Callable[..., Any]) -> Callable[[Any], Any]:
    """Create a new transforms function which takes the whole sample as its only argument,
    rather than destructuring it.

    :param transforms: The transforms function to standardize.
    :return: The standardized transforms function.
    """
def get_column_from_pyarrow_table(table: pa.Table, name: str, combine_chunks: bool = True) -> pa.Array | pa.ChunkedArray:
    """Return a the specified column of the table as a pyarrow table.

    To get nested sub-columns, use dot notation. E.g. 'column.sub_column'. The values in the column will be
    the row-view of the table. A column which is a PIL image in its sample-view, for instance, will be returned as
    a column of strings.

    :param name: The name of the column to get.
    :param combine_chunks: Whether to combine the chunks of the returned column in the case that it is a
        ChunkedArray. Defaults to True.
    :returns: A pyarrow array containing the specified column.
    :raises KeyError: If the column does not exist in the table.
    """
